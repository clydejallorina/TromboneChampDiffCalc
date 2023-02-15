import json
import math
import os
import logging
import argparse
from dataclasses import dataclass
from time import time
from typing import Optional, List
import numpy as np
from enum import Enum
from hashlib import sha256
import requests as r
import matplotlib.pyplot as plt

TMB_TO_DIFF_VERSION = "1.0.2"
GENERATE_GRAPHS = True
class NoteData(Enum):
    TIME_START = 0
    TIME_END = 1
    PITCH_START = 2
    PITCH_DELTA = 3
    PITCH_END = 4
    
@dataclass
class Note:
    time_start: float
    time_end: float
    length: float
    pitch_start: float
    pitch_end: float
    pitch_delta: float

@dataclass
class TMBChart:
    # Most of these wouldn"t be used in the actual calculations
    # Just keeping it here for future reference in parsing custom TMBs
    name: str
    short_name: str
    track_ref: str
    year: int
    author: str
    genre: str
    description: str
    difficulty: int
    saved_note_spacing: int
    endpoint: int
    timesig: int
    tempo: int # bpm
    lyrics: list
    notes: list # list of 5-tuples
    skip_save: bool
    is_wip: bool

    def __str__(self) -> str:
        return f"{self.name} ({self.difficulty})"

    def __repr__(self) -> str:
        return f"TMBChart({self.name})"
    
def json_to_tmb(json_string:str):
    try:
        tmb_file = json.loads(json_string)
    except Exception as e:
        logging.error("Parsing failed!")
        return None
    return TMBChart(
        name=tmb_file["name"],
        short_name=tmb_file["shortName"],
        track_ref=tmb_file["trackRef"],
        year=tmb_file["year"],
        author=tmb_file["author"],
        genre=tmb_file["genre"],
        description=tmb_file["description"],
        difficulty=tmb_file["difficulty"],
        saved_note_spacing=tmb_file["savednotespacing"],
        endpoint=tmb_file["endpoint"],
        timesig=tmb_file["timesig"],
        tempo=tmb_file["tempo"],
        lyrics=tmb_file["lyrics"] if "lyrics" in tmb_file else "",
        notes=tmb_file["notes"],
        skip_save=tmb_file["skip_save"] if "skip_save" in tmb_file else False,
        is_wip=tmb_file["is_wip"] if "is_wip" in tmb_file else False,
    )

def read_tmb(filename:str) -> Optional[TMBChart]:
    if not filename.endswith(".tmb"):
        logging.warning("File is not a tmb file! Ignoring.")
        return None
    if not os.path.exists(filename):
        logging.error("File doesn't exist!")
        return None
    with open(filename, encoding="utf-8") as file:
        tmb = json_to_tmb(file.read())
        if tmb == None:
            logging.error("Parsing failed for %s", filename)
            return None
        return tmb

def b2s(time:float, bpm:int) -> float:
    # Shorthand for beat to seconds
    return (time / bpm) * 60

def turn_to_seconds_v2(notes:list, bpm:float) -> List[Note]:
    new_notes = []
    for note in notes:
        start_time = b2s(note[0], bpm)
        note_length = note[1] if note[1] > 0 else 0.01
        end_time = b2s(note[0] + note[1], bpm) if note[1] != 0 else b2s(note[0] + 0.01, bpm)
        new_note = Note(time_start=start_time, time_end=end_time, length=b2s(note_length, bpm), pitch_start=note[2], pitch_delta=note[3], pitch_end=note[4])
        new_notes.append(new_note)
    new_notes.sort(key=lambda x: x.time_start) # Sort the notes by start time to not have weird timing bugs in calculation, just in case
    return new_notes

def calc_combo_performance(notes:List[Note], index:int) -> float:
    LENGTH_WEIGHTS = [1, 0.65, 0.4225, 0.274625, 0.17850625, 0.1160290625, 0.075418890625, 0.04902227890625, 0.0318644812890625, 0.02071191283789063, 0.013462743344628911]
    important_notes = [
        n.length * LENGTH_WEIGHTS[i]
        for i, n in enumerate(notes[index:index+10])
        if notes[index+i].time_start - notes[index].time_end <= 4
    ]
    strain_multiplier = np.sqrt(sum(important_notes) * len(important_notes) + len(important_notes)) / 2.75
    return strain_multiplier

def calc_aim_rating_v2(notes:List[Note], bpm:float, song_name:str) -> float:
    SLIDER_BREAK_CONSTANT = 34.375
    MAXIMUM_TIME_CONSTANT = b2s(0.2, bpm)
    ENDURANCE_STRAIN_LIMIT = 500
    endurance_multiplier = 0.85
    aim_performance = []
    for current_idx, current_note in enumerate(notes):
        slider_strain = 0
        speed_strain = 0
        direction_switch_bonus = 1
        combo_penalty = calc_combo_performance(notes, current_idx)
        prev_dir = 0 # -1 = DOWN, 0 = NOT MOVING, 1 = UP
        important_notes = [note for i, note in enumerate(notes[current_idx:current_idx+60]) if note.time_start - current_note.time_end <= 5]
        
        for i, note in enumerate(important_notes):
            speed = 0
            slider_speed = (abs(note.pitch_delta) / note.length) * 1
            curr_dir = np.sign(note.pitch_delta)
            prev_note = None
            prev_note_delta = None
            
            if current_idx + i > 0:
                prev_note = notes[current_idx + i - 1]
            
            if prev_note != None and note.time_start != prev_note.time_end and prev_note.pitch_delta == 0:
                # If not a slider, do these calculations
                prev_note_delta = note.pitch_start - prev_note.pitch_end
                curr_dir = np.sign(prev_note_delta)
                dist = abs(prev_note_delta)
                t = note.time_start - prev_note.time_end
                speed = dist / abs(max([t, MAXIMUM_TIME_CONSTANT]))
            elif note.pitch_delta <= SLIDER_BREAK_CONSTANT:
                # Apply cheesable slider nerf
                slider_speed /= ((SLIDER_BREAK_CONSTANT * combo_penalty * 2) - note.pitch_delta) / SLIDER_BREAK_CONSTANT
            
            # Apply direction switch buff
            if curr_dir != 0 and prev_dir == -curr_dir:
                if prev_note_delta != None:
                    delta_multiplier = (0.1 / (1 + math.pow(math.e, -0.05 * (prev_note_delta - 130)))) + 1
                else:
                    delta_multiplier = (0.2 / (1 + math.pow(math.e, -0.05 * (note.pitch_delta - 40)))) + 1
                direction_switch_bonus *= delta_multiplier
            if direction_switch_bonus > 1.5: # hard cap it to 2
                direction_switch_bonus = 1.5
            
            weight = math.pow(0.94, i-1)
            slider_strain += abs(slider_speed) * weight * direction_switch_bonus
            speed_strain += speed * weight * direction_switch_bonus
            prev_dir = curr_dir
        
        strain_sum = speed_strain + slider_strain
        endurance_strain = lambda x: (math.pow(x, 1 / 2.5) / 50000) + 1
        if endurance_multiplier >= 1 and strain_sum <= ENDURANCE_STRAIN_LIMIT:
            endurance_multiplier /= (1 - (endurance_strain(ENDURANCE_STRAIN_LIMIT) - endurance_strain(strain_sum)))
        else:
            endurance_multiplier *= endurance_strain(strain_sum)
        
        # Apply combo penalties for the note
        if combo_penalty < 1.25:
            slider_strain *= combo_penalty * 1.15
            speed_strain *= combo_penalty * 1.3
        
        slider_strain *= endurance_multiplier
        speed_strain *= endurance_multiplier
        
        slider_strain = np.sqrt(slider_strain * len(important_notes)) / 85
        speed_strain = np.sqrt(speed_strain * len(important_notes)) / 90
        
        aim_performance.append(slider_strain + speed_strain)
    x = [note.time_start for note in notes]
    generate_graph(x, aim_performance, "Time (s)", "Aim Performance", f"{song_name} - Aim")
    return np.average(aim_performance)

def calc_tap_rating_v2(notes:List[Note], song_name:str) -> float:
    endurance_multiplier = 0.85
    tap_performance = []
    for current_idx, current_note in enumerate(notes):
        tap_strain = 0
        strain_value = 1
        important_notes = [note for note in notes[current_idx+1:current_idx+101] if note.time_start - current_note.time_end <= 8]
        
        for i, note in enumerate(important_notes, start=1):
            prev_note = None
            if current_idx + i > 0:
                prev_note = notes[current_idx + i - 1]
            if prev_note != None and note.time_start > prev_note.time_end and prev_note.pitch_delta == 0:
                tap_strain += strain_value
                time_delta = note.time_start - prev_note.time_end
                strain_value += abs(0.55 - time_delta)

        endurance_curve = lambda x: (math.pow(x, 1 / 2.5) / 18000) + 1
        decay_curve = lambda x: (math.pow(x - 0.9, 1 / 2.5) / 900) + 1
        if endurance_multiplier >= 1:
            endurance_multiplier /= decay_curve(endurance_multiplier)
        endurance_multiplier *= endurance_curve(tap_strain)
        tap_strain = np.sqrt(tap_strain / 6.2) * endurance_multiplier
        tap_performance.append(tap_strain)
    
    x = [note.time_start for note in notes]
    generate_graph(x, tap_performance, "Time (s)", "Tap Performance", f"{song_name} - Tap")
    return np.average(tap_performance)

def calc_diff(tmb:Optional[TMBChart]) -> list:
    if tmb == None:
        logging.error("TMB Chart is None, returning 0")
        return [0,0,0]
    start_time = time()
    converted = turn_to_seconds_v2(tmb.notes, tmb.tempo)
    track_length = converted[-1].time_end - converted[0].time_start
    logging.info("Processing: %s", tmb.name)
    logging.info("Song Length: %f", track_length)
    
    aim_rating = calc_aim_rating_v2(converted, tmb.tempo, tmb.short_name)
    tap_rating = calc_tap_rating_v2(converted, tmb.short_name)
    
    star_rating = np.average([aim_rating, tap_rating], weights=[2,1])
    end_time = time()
    logging.info("Processing took %f seconds", end_time - start_time)
    return [star_rating, aim_rating, tap_rating]

def calc_tt(star_rating:float) -> float:
    # Star Rating to TT Conversion Graph: https://www.desmos.com/calculator/padi1etn1w
    if star_rating <= 0:
        return 0
    if star_rating >= 3.40791:
        return 11.1538 - (17.2552 * star_rating) + (9.3328 * (star_rating ** 2)) + (0.0903 * (star_rating ** 3))
    return (0.85 * (star_rating ** 3)) + (9 * star_rating)

def calc_score_tt(base_tt:float, player_score:float, max_score:float) -> float:
    # Code derived from https://www.desmos.com/calculator/z6li8qz2ai
    percentage = player_score / max_score
    if percentage < 0:
        return 0
    if percentage < 0.3:
        return (0.026 * percentage) * base_tt
    if percentage < 0.5:
        return ((0.9 * (percentage ** 3)) - (0.055 * percentage)) * base_tt
    if percentage <= 0.8:
        return ((3.2 * (percentage ** 5.2)) - (0.00351035 * percentage)) * base_tt
    return ((3 * (percentage ** 5.6)) + (0.165545 * percentage)) * base_tt

def process_tmb(filename:str) -> float:
    return calc_diff(read_tmb(filename))

def calc_max_score(tmb:TMBChart) -> list:
    # Code derived from https://github.com/emmett-shark/HighscoreAccuracy/blob/main/Utils.cs
    game_max_score = 0
    max_score = 0
    for idx, note in enumerate(tmb.notes):
        champ_bonus = np.float32(1.5) if idx > 23 else 0
        real_coefficient = np.float32((min(idx, 10) + champ_bonus) * np.float32(0.1)) + np.float32(1)
        max_score += np.floor(np.floor(np.float32(note[1]) * np.float32(10) * np.float32(100) * real_coefficient) * np.float32(10))
        game_max_score += np.floor(np.floor(note[1] * np.float32(10) * np.float32(100) * np.float32(1.3)) * np.float32(10))
    return [max_score, game_max_score]

def get_letter_from_score(score:int, game_max_score:int):
    percentage = score / game_max_score
    if percentage > np.float32(1):
        return "S"
    if percentage > np.float32(0.8):
        return "A"
    if percentage > np.float32(0.6):
        return "B"
    if percentage > np.float32(0.4):
        return "C"
    if percentage > np.float32(0.2):
        return "D"
    return "F"

def log_leaderboard(filename:str, base_tt:float, max_score:float):
    # Get leaderboard from TootTally servers
    with open(filename, "r", encoding="utf-8") as file:
        file_hash = sha256(file.read().encode("utf-8")).hexdigest()
    req = r.get(f"https://toottally.com/api/hashcheck/custom/?songHash={file_hash}")
    if req.status_code != 200:
        logging.info("Cannot find chart on TootTally servers, stopping.")
        return
    song_id = req.text
    lb_req = r.get(f"https://toottally.com/api/songs/{song_id}/leaderboard/")
    if lb_req.status_code != 200:
        logging.info("Cannot obtain leaderboard data, stopping.")
    lb = lb_req.json()
    results = lb["results"]
    leaderboard  = f"Found {lb['count']} scores in the leaderboard right now\n"
    leaderboard += "+---------+-----------------------+---------------+-------------------+\n"
    leaderboard += "| Ranking |      Player Name      |     Score     |     TT Rating     |\n"
    leaderboard += "+---------+-----------------------+---------------+-------------------+\n"
    for i, result in enumerate(results, start=1):
        player = result["player"]
        tt = calc_score_tt(base_tt, int(result["score"]), max_score)
        leaderboard += f"|{i:^9d}|{player:^23s}|{result['score']:^15d}|{tt:19f}|\n"
    leaderboard += "+---------+-----------------------+---------------+-------------------+\n"
        
    logging.info(leaderboard)
    
def generate_graph(x, y, x_label="", y_label="", title=""):
    if not GENERATE_GRAPHS:
        return
    title = title.strip()
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel=x_label, ylabel=y_label, title=title)
    ax.grid()
    fig.set_size_inches(18.5, 10.5)
    fig.set_dpi(400)
    try:
        logging.info(f"Generating graph: graphs/{title}.png")
        fig.savefig(f"graphs/{title}")
    except Exception as e:
        logging.error(f"Failed to generate graph: {e}")
    plt.close(fig)

if __name__ == "__main__":
    logging.basicConfig(filename="run.log", level=logging.INFO, encoding="utf-8", filemode="w")
    parser = argparse.ArgumentParser(description="Difficulty calculation tool")
    parser.add_argument("filename", metavar="filename", type=str, help="Target .tmb to analyze")
    args = parser.parse_args()
    tmb = read_tmb(args.filename)
    diff, aim, spd = calc_diff(tmb)
    max_score, game_max_score = calc_max_score(tmb)
    base_tt = calc_tt(diff)
    print(f"{tmb}: {round(diff, 3)} [Aim: {round(aim, 3)}|Speed: {round(spd, 3)}]")
    print(f"Game Max Score: {game_max_score} | Max Score: {max_score} | Base TT: {base_tt}")
    
    # Get leaderboard from TootTally servers
    with open(args.filename, "r") as file:
        file_hash = sha256(file.read().encode("utf-8")).hexdigest()
    req = r.get(f"https://toottally.com/api/hashcheck/custom/?songHash={file_hash}")
    if req.status_code != 200:
        print("Cannot find on TootTally servers, stopping.")
    else:
        song_id = req.text
        lb_req = r.get(f"https://toottally.com/api/songs/{song_id}/leaderboard/")
        if lb_req.status_code != 200:
            print("Cannot obtain leaderboard data, stopping.")
        else:
            lb = lb_req.json()
            print(f"Found {lb['count']} scores in the leaderboard right now")
            results = lb["results"]
            for result in results:
                tt = calc_score_tt(base_tt, int(result["score"]), max_score)
                print(f"{result['player']}: {round((result['score'] / game_max_score) * 100, 2)}% - {round(tt, 4)}tt")
