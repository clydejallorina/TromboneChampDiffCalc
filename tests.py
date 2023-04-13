from TMBToDiff import *
import os
import logging
import time
import unicodedata
import csv

if __name__ == "__main__":
    LOGGER_FORMAT = "[%(asctime)s] %(message)s"
    FOLDER = "RatedTmbs/"
    logging.basicConfig(filename="tests.log", level=logging.INFO, encoding="utf-8", filemode="w", format=LOGGER_FORMAT)
    start_time = time.time()
    with open("tests.csv", "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Song Name", "Speed", "Map Diff", "Computed Diff", "Tap Rating", "Aim Rating", "TT Rating"])
        print("+-----------------------------+-------+----------+---------------+--------------+------------+-------------+")
        print("|          Song Name          | Speed | Map Diff | Computed Diff |  Tap Rating  | Aim Rating |  TT Rating  |")
        print("+-----------------------------+-------+----------+---------------+--------------+------------+-------------+")
        for tmb_file in os.listdir(FOLDER):
            if not tmb_file.endswith(".tmb"):
                continue
            speeds = [0.5,0.75,1.0,1.25,1.5,2.0]
            for speed in speeds:
                tmb = read_tmb(f"{FOLDER}{tmb_file}")
                song_name = unicodedata.normalize("NFKC", tmb.short_name)
                map_diff = tmb.difficulty
                diff_calc = calc_diff(tmb, speed)
                tt_rating = calc_tt(diff_calc[0])
                max_score, game_max_score = calc_max_score(tmb)
                # log_leaderboard(FOLDER + tmb_file, tt_rating, max_score)
                print(f"|{song_name[:29]:^29s}| {speed:.3f} | {map_diff:^8d} | {diff_calc[0]:13f} | {diff_calc[2]:12f} | {diff_calc[1]:10f} | {tt_rating:11f} |")
                writer.writerow([song_name, speed, map_diff, diff_calc[0], diff_calc[2], diff_calc[1], tt_rating])
        print("+-----------------------------+-------+----------+---------------+--------------+------------+-------------+")
    end_time = time.time()
    print(f"Report generated at {time.asctime(time.gmtime())}")
    print(f"Generated in {end_time - start_time:f} seconds")
    