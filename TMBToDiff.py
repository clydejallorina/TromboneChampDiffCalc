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

TMB_TO_DIFF_VERSION = "1.2.0"
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

def lerp(a, b, t):
    # a = initial point
    # b = final point
    # t = time interval
    return a + ((b - a) * t)

def ease(a, b, t, exponent):
    return lerp(a, b, t ** exponent)

def turn_to_seconds_v2(notes:list, bpm:float) -> List[Note]:
    new_notes = []
    for note in notes:
        start_time = b2s(note[0], bpm)
        note_length = note[1] if note[1] > 0 else 0.015
        end_time = b2s(note[0] + note[1], bpm) if note[1] != 0 else b2s(note[0] + 0.015, bpm)
        new_note = Note(time_start=start_time, time_end=end_time, length=b2s(note_length, bpm), pitch_start=note[2], pitch_delta=note[3], pitch_end=note[4])
        new_notes.append(new_note)
    new_notes.sort(key=lambda x: x.time_start) # Sort the notes by start time to not have weird timing bugs in calculation, just in case
    return new_notes

def calculate_tap_tap_note_nerf(non_tap_note_ratio, average_note_length, stacatto_constant) -> float:
    return max(-(math.pow((0.70 * (average_note_length - stacatto_constant)), (1 / (8 * non_tap_note_ratio)))) + 1, 0.5)

def calculate_aim_tap_note_nerf(non_tap_note_ratio, average_note_length, stacatto_constant) -> float:
    return max(-(math.pow((0.45 * (average_note_length - stacatto_constant)), (1 / (7 * non_tap_note_ratio)))) + 1, 0.5)

def calc_combo_performance(notes:List[Note], index:int) -> float:
    LENGTH_WEIGHTS = [1, 0.65, 0.4225, 0.274625, 0.17850625, 0.1160290625, 0.075418890625, 0.04902227890625, 0.0318644812890625, 0.02071191283789063, 0.013462743344628911]
    important_notes = [
        n.length * LENGTH_WEIGHTS[i]
        for i, n in enumerate(notes[index:index+10])
        if notes[index+i].time_start - notes[index].time_end <= 4
    ]
    strain_multiplier = np.sqrt(sum(important_notes) * len(important_notes) + len(important_notes)) / 2.75
    return strain_multiplier

def calc_combo_performance_v2(notes:List[Note], index:int) -> float:
    # LENGTH_WEIGHTS = [1, 0.65, 0.4225, 0.274625, 0.17850625, 0.1160290625, 0.075418890625, 0.04902227890625, 0.0318644812890625, 0.02071191283789063, 0.013462743344628911]
    LENGTH_WEIGHTS = [1, 0.75, 0.5625, 0.4218, 0.3164, 0.2373, 0.1779, 0.1334, 0.1, 0.0751, 0.0563]
    important_notes = [
        n.length * LENGTH_WEIGHTS[i]
        for i, n in enumerate(notes[index:index+10])
    ]
    strain_multiplier = (np.cbrt((sum(important_notes) - 1) * len(important_notes) + len(important_notes)) / 1.25) + 0.05
    # logging.info("Sum: %f | Length: %d | Strain MP: %f", sum(important_notes), len(important_notes), strain_multiplier)
    return strain_multiplier

def calc_aim_rating_v2(notes:List[Note], bpm:float, song_name:str) -> float:
    SLIDER_BREAK_CONSTANT = 34.375
    MAXIMUM_TIME_CONSTANT = b2s(0.05, bpm)
    endurance_multiplier = 0.85
    aim_performance = []
    
    logging.info("BPM: %f", bpm)
    
    for current_idx, current_note in enumerate(notes):
        slider_strain = 0
        speed_strain = 0
        direction_switch_bonus = 1
        combo_multiplier = calc_combo_performance_v2(notes, current_idx)
        prev_dir = 0 # -1 = DOWN, 0 = NOT MOVING, 1 = UP
        important_notes = [note for note in notes[current_idx:current_idx+50] if note.time_start - current_note.time_end <= 5]
        
        for i, note in enumerate(important_notes):
            speed = 0
            slider_speed = abs(note.pitch_delta * 1.25) / note.length 
            curr_dir = np.sign(note.pitch_delta)
            prev_note = None
            prev_note_delta = None
            
            if current_idx + i > 0:
                prev_note = notes[current_idx + i - 1]
            
            if prev_note != None and note.time_start != prev_note.time_end and prev_note.pitch_delta == 0:
                # If not a slider, do these calculations
                prev_note_delta = note.pitch_start - prev_note.pitch_end
                curr_dir = np.sign(prev_note_delta)
                dist = abs(prev_note_delta * 1.25)
                t = note.time_start - prev_note.time_end
                speed = dist / abs(max([t, MAXIMUM_TIME_CONSTANT]))
                if note.pitch_delta <= SLIDER_BREAK_CONSTANT:
                    # Apply cheesable slider nerf
                    slider_speed /= ((SLIDER_BREAK_CONSTANT * 4) - note.pitch_delta) / SLIDER_BREAK_CONSTANT
            
            # Apply direction switch buff
            if curr_dir != 0 and prev_dir == -curr_dir:
                if prev_note_delta != None:
                    delta_multiplier = (0.1 / (1 + math.pow(math.e, -0.05 * (prev_note_delta - 130)))) + 1
                else:
                    delta_multiplier = (0.2 / (1 + math.pow(math.e, -0.05 * (note.pitch_delta - 40)))) + 1
                direction_switch_bonus *= delta_multiplier
            
            weight = math.pow(0.9325, i-1)
            slider_strain += abs(slider_speed) * weight * direction_switch_bonus
            speed_strain += speed * weight * direction_switch_bonus * 0.5
            prev_dir = curr_dir
        
        strain_sum = speed_strain + slider_strain
        endurance_curve = lambda x: (math.pow(x, 1 / 2.5) / 13000) + 1
        decay_curve = lambda x: (math.pow(x - 0.9, 1 / 2.5) / 800) + 1
        if endurance_multiplier >= 1:
            endurance_multiplier /= decay_curve(endurance_multiplier)
        endurance_multiplier *= endurance_curve(strain_sum)
        
        # Apply combo penalties for the note
        # if combo_penalty < 1.25:
        #     slider_strain *= combo_penalty * 1.15
        #     speed_strain *= combo_penalty * 1.3
        
        slider_strain *= combo_multiplier
        speed_strain *= combo_multiplier
        slider_strain *= endurance_multiplier
        speed_strain *= endurance_multiplier
        
        slider_strain = np.sqrt(slider_strain * len(important_notes)) / 110
        speed_strain = np.sqrt(speed_strain * len(important_notes)) / 80
        
        total_strain = slider_strain + speed_strain
        aim_performance.append(total_strain)
        
    x = [note.time_start for note in notes]
    generate_graph(x, aim_performance, "Time (s)", "Aim Performance", f"{song_name} - Aim")
    return np.average(aim_performance)

def calc_tap_rating_v2(notes:List[Note], bpm:float, song_name:str) -> float:
    endurance_multiplier = 0.85
    tap_performance = []
    MINIMUM_TIME_CONST = 1/120 #Because centipete would break the algo :skull:
    
    for current_idx, current_note in enumerate(notes):
        strain_sum = 0
        combo_multiplier = calc_combo_performance_v2(notes, current_idx)
        important_notes = [note for note in notes[current_idx+1:current_idx+50] if note.time_start - current_note.time_end <= 8]
        
        for i, note in enumerate(important_notes, start=1):
            prev_note = None
            if current_idx + i > 0:
                prev_note = notes[current_idx + i - 1]
            if prev_note != None and note.time_start > prev_note.time_end and prev_note.pitch_delta == 0:
                time_delta = note.time_start - prev_note.time_end
                if time_delta < MINIMUM_TIME_CONST:
                    time_delta = MINIMUM_TIME_CONST
                weight = math.pow(0.9375, i-1)
                strain_sum += (10/math.pow(time_delta,1.25)) * weight

        endurance_curve = lambda x: (math.pow(x, 1 / 2.5) / 11000) + 1
        decay_curve = lambda x: (math.pow(x - 0.9, 1 / 2.5) / 800) + 1
        if endurance_multiplier >= 1:
            endurance_multiplier /= decay_curve(endurance_multiplier)
        endurance_multiplier *= endurance_curve(strain_sum)
        strain_sum *= endurance_multiplier
        strain_sum = np.sqrt(strain_sum * len(important_notes)) / 70
        tap_performance.append(strain_sum)
    
    x = [note.time_start for note in notes]
    generate_graph(x, tap_performance, "Time (s)", "Tap Performance", f"{song_name} - Tap")
    return np.average(tap_performance)

def calc_diff(tmb:Optional[TMBChart], speed:float=1) -> list:
    if tmb == None:
        logging.error("TMB Chart is None, returning 0")
        return [0,0,0]
    start_time = time()
    previous_tempo = tmb.tempo
    tmb.tempo *= speed
    converted = turn_to_seconds_v2(tmb.notes, tmb.tempo)
    track_length = converted[-1].time_end - converted[0].time_start
    logging.info("Processing: %s", tmb.name)
    logging.info("Song Length: %f", track_length)
    logging.info("Speed: %f (%f BPM -> %f BPM)", speed, previous_tempo, tmb.tempo)
    
    aim_rating = calc_aim_rating_v2(converted, tmb.tempo, tmb.short_name + f"[{speed:.2f}x]")
    tap_rating = calc_tap_rating_v2(converted, tmb.tempo, tmb.short_name + f"[{speed:.2f}x]")
    
    star_rating = np.average([aim_rating, tap_rating], weights=[3,2])
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
    # Code derived from https://www.desmos.com/calculator/zpxry46d5f
    percentage = player_score / max_score
    if percentage < 0:
        return 0
    if percentage < 0.3:
        return (0.026 * percentage) * base_tt
    if percentage < 0.5:
        return ((0.9 * (percentage ** 3)) - (0.055 * percentage)) * base_tt
    if percentage <= 0.9:
        return ((3 * (percentage ** 5.6)) + (0.165545 * percentage)) * base_tt
    return ((0.4 * math.pow(math.e, 28.1 * (percentage - 0.9))) + 1.4470081) * base_tt

def process_tmb(filename:str) -> float:
    return calc_diff(read_tmb(filename))

def calc_max_score(tmb:TMBChart) -> list:
    # Code derived from https://github.com/emmett-shark/HighscoreAccuracy/blob/main/Utils.cs
    game_max_score = 0
    max_score = 0
    for idx, note in enumerate(tmb.notes):
        note_length = np.float32(0.015) if note[1] == 0 else note[1]
        champ_bonus = np.float32(1.5) if idx > 23 else 0
        real_coefficient = np.float32((min(idx, 10) + champ_bonus) * np.float32(0.1)) + np.float32(1)
        max_score += np.floor(np.floor(np.float32(note_length) * np.float32(10) * np.float32(100) * real_coefficient) * np.float32(10))
        game_max_score += np.floor(np.floor(np.float32(note_length) * np.float32(10) * np.float32(100) * np.float32(1.3)) * np.float32(10))
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

def calc_tt_with_speed(speed_diffs:List[float], replay_speed:float, score:int, max_score:int):
    speeds = [0.5,0.75,1.0,1.25,1.5,1.75,2.0]
    star_rating = 1
    if replay_speed in speeds:
        star_rating = speed_diffs[speeds.index(replay_speed)]
    else:
        b_index = next(x[0] for x in enumerate(speeds) if x[1] > float(replay_speed))
        a_index = b_index - 1
        a = float(speed_diffs[a_index])
        b = float(speed_diffs[b_index])
        percentage = 1 - ((speeds[b_index] - float(replay_speed)) / (speeds[b_index] - speeds[a_index]))
        star_rating = lerp(a, b, percentage)
    base_tt = calc_tt(star_rating)
    return calc_score_tt(base_tt, int(score), max_score)

def log_leaderboard(filename:str, speed_diffs:List[float], max_score:float):
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
    leaderboard  = f"Found {lb['count']} scores in the leaderboard right now (Max Score: {max_score})\n"
    leaderboard += "+---------+-----------------------+-------+---------------+-------------------+\n"
    leaderboard += "| Ranking |      Player Name      | Speed |     Score     |     TT Rating     |\n"
    leaderboard += "+---------+-----------------------+-------+---------------+-------------------+\n"
    for i, result in enumerate(results, start=1):
        player = result["player"]
        score = int(result["score"])
        replay_speed = float(result["replay_speed"])
        tt = calc_tt_with_speed(speed_diffs, replay_speed, score, max_score)
        leaderboard += f"|{i:^9d}|{player:^23s}| {replay_speed:^.2f}x |{result['score']:^15d}|{tt:19f}|\n"
    leaderboard += "+---------+-----------------------+-------+---------------+-------------------+\n"
        
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
        fig.savefig(f"graphs/{title.replace('.', '').replace('?', '')}")
    except Exception as e:
        logging.error(f"Failed to generate graph: {e}")
    plt.close(fig)

if __name__ == "__main__":
    logging.basicConfig(filename="run.log", level=logging.INFO, encoding="utf-8", filemode="w")
    parser = argparse.ArgumentParser(description="Difficulty calculation tool")
    parser.add_argument("filename", metavar="filename", type=str, help="Target .tmb to analyze")
    # parser.add_argument("lb", metavar="lb", type=bool, help="Enable leaderboard calculations")
    speeds = [0.5,0.75,1.0,1.25,1.5,1.75,2.0]
    speed_diffs = []
    args = parser.parse_args()
    for speed in speeds:
        tmb = read_tmb(args.filename)
        diff, aim, spd = calc_diff(tmb, speed)
        max_score, game_max_score = calc_max_score(tmb)
        speed_diffs.append(diff)
        base_tt = calc_tt(diff)
        print(f"{tmb}[{speed:.2f}x]: {round(diff, 3)} [Aim: {round(aim, 3)}|Speed: {round(spd, 3)}]")
        print(f"Game Max Score: {game_max_score} | Max Score: {max_score} | Base TT: {base_tt}")
    
    # Get leaderboard from TootTally servers
    # if args.lb:
    with open(args.filename, "r") as file:
        file_hash = sha256(file.read().encode("utf-8")).hexdigest()
    req = r.get(f"https://toottally.com/api/hashcheck/custom/?songHash={file_hash}")
    if req.status_code != 200:
        print("Cannot find on TootTally servers, stopping.")
    else:
        song_id = req.text
        print(f"Searching leaderboard for https://toottally.com/song/{song_id}")
        lb_req = r.get(f"https://toottally.com/api/songs/{song_id}/leaderboard/")
        if lb_req.status_code != 200:
            print("Cannot obtain leaderboard data, stopping.")
        else:
            lb = lb_req.json()
            print(f"Found {lb['count']} scores in the leaderboard right now")
            results = lb["results"]
            for result in results:
                replay_speed = result["replay_speed"]
                tt = calc_tt_with_speed(speed_diffs, replay_speed, int(result["score"]), max_score)
                print(f"{result['player']} [{replay_speed:.2f}x]: {round((result['score'] / max_score) * 100, 2)}% - {round(tt, 4)}tt")
