import json
import math
import os
import logging
import argparse
from dataclasses import dataclass
from time import time
from typing import Optional
import numpy as np

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

    def __str__(self) -> str:
        return f"{self.name} ({self.difficulty})"

    def __repr__(self) -> str:
        return f"TMBChart({self.name})"

def read_tmb(filename:str) -> Optional[TMBChart]:
    if not filename.endswith(".tmb"):
        logging.warning("File is not a tmb file! Ignoring.")
        return None
    if not os.path.exists(filename):
        logging.error("File doesn't exist!")
        return None
    with open(filename, encoding="utf-8") as file:
        tmb_file = json.load(file)
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
            lyrics=tmb_file["lyrics"],
            notes=tmb_file["notes"],
        )

def b2s(time:float, bpm:int) -> float:
    # Shorthand for beat to seconds
    return round((time / bpm) * 60, 4)

def stitch_notes(notes:list, bpm:int) -> list:
    # Stitch sliders into single objects
    stitched_notes = []
    min_pitch = min(notes[0][2], notes[0][4])
    max_pitch = max(notes[0][2], notes[0][4])
    # FORMAT: [start time, end time, start pitch, delta, end pitch]
    to_be_stitched = [b2s(notes[0][0], bpm), b2s(notes[0][0] + notes[0][1], bpm), notes[0][2], abs(notes[0][3]), notes[0][4]]
    for idx in range(1, len(notes)):
        min_pitch = min(min_pitch, notes[idx][2], notes[idx][4])
        max_pitch = max(max_pitch, notes[idx][2], notes[idx][4])
        if notes[idx][0] != notes[idx-1][0] + notes[idx-1][1] or notes[idx][2] != notes[idx-1][4]:
            # Doesn't need to be stitched, start of new note
            stitched_notes.append(to_be_stitched)
            to_be_stitched = [b2s(notes[idx][0], bpm), b2s(notes[idx][0] + notes[idx][1], bpm), notes[idx][2], abs(notes[idx][3]), notes[idx][4]]
        else:
            # Needs to be stitched, update details
            to_be_stitched[1] = b2s(notes[idx][0] + notes[idx][1], bpm) # Set end time to the new one
            to_be_stitched[3] += abs(notes[idx][3]) # Add cumulative delta for slider
            to_be_stitched[4] = notes[idx][4] # Update end pitch to the new one
    stitched_notes.append(to_be_stitched)
    return stitched_notes

def turn_to_seconds(notes:list, bpm:int) -> list:
    new_notes = []
    for note in notes:
        new_notes.append([b2s(note[0], bpm), b2s(note[0] + note[1], bpm)] + note[2:])
    return new_notes

def speed_strain(delta_time:float) -> float:
    return np.sqrt((-delta_time + 5) / 5)

def aim_strain(delta_time:float, distance:float) -> float:
    return (distance / 165) * (np.cbrt(-delta_time / 5) + 1)

def cap_result(uncapped:float) -> float:
    return 2.5 * np.sqrt(uncapped)

def calc_diff(tmb:TMBChart) -> float:
    start_time = time()
    taps = stitch_notes(tmb.notes, tmb.tempo)
    converted = turn_to_seconds(tmb.notes, tmb.tempo)
    bpm_multiplier = 1.25 / (1 + math.pow(math.e, -0.03 * (tmb.tempo - 150)))
    
    # Calculate aim rating
    aim_performance = [] # List containing the estimated aim performance for the note
    for idx, note in enumerate(converted):
        i = idx - 1
        strain = 0
        dist = 0
        while i > 0 and note[0] - converted[i][0] <= 5.0:
            dist += abs(converted[i][3]) + abs(converted[i-1][4] - converted[i][2]) # Slider delta + Note delta
            strain += aim_strain(note[0] - converted[i][1], dist)
            i -= 1
        aim_performance.append(strain)
    aim_performance.sort()
    top_aim_strains = aim_performance[-10:]
    aim_average = np.mean(aim_performance)
    aim_std = np.std(aim_performance) * 2 # standard deviation
    culled_aim = [x for x in aim_performance if x <= aim_average + aim_std]
    logging.info("Top Aim Strains for %s:\n%s", tmb.name, str(top_aim_strains))
    logging.info("Culled %d data points for aim, %d points remain",
                 len(aim_performance) - len(culled_aim),
                 len(culled_aim))
    aim_rating = np.average(culled_aim, weights=[2 - (abs(point - aim_average) / aim_std) for point in culled_aim])
    
    # Calculate speed rating
    speed_performance = []
    for idx, note in enumerate(taps):
        i = idx - 1
        strain = 0
        while i >= 0 and note[0] - taps[i][0] <= 5.0:
            strain += speed_strain(note[0] - taps[i][1])
            i -= 1
        speed_performance.append(strain)
    speed_performance.sort()
    top_speed_strains = speed_performance[-10:]
    speed_average = np.mean(speed_performance)
    speed_std = np.std(speed_performance) * 1.5 # standard deviation
    culled_speed = [x for x in speed_performance if x <= speed_average + speed_std]
    logging.info("Top Speed Strains for %s:\n%s", tmb.name, str(top_speed_strains))
    logging.info("Culled %d data points for speed, %d points remain",
                 len(speed_performance) - len(culled_speed),
                 len(culled_speed))
    speed_rating = np.average(culled_speed) * bpm_multiplier
    end_time = time()
    logging.info("Speed Rating: %f | Aim Rating: %f", speed_rating, aim_rating)
    logging.info("Calculation took %f seconds\n", end_time - start_time)
    
    return cap_result(np.average([aim_rating, speed_rating], weights=[1,5])) * bpm_multiplier

def process_tmb(filename:str) -> float:
    return calc_diff(read_tmb(filename))

if __name__ == "__main__":
    logging.basicConfig(filename="run.log", level=logging.INFO, encoding="utf-8", filemode="w")
    parser = argparse.ArgumentParser(description="Difficulty calculation tool")
    parser.add_argument("filename", metavar="filename", type=str, help="Target .tmb to analyze")
    args = parser.parse_args()
    tmb = read_tmb(args.filename)
    print(f"{tmb}: {round(calc_diff(tmb), 3)}")
