from TMBToDiff import *
import os
import logging
import time

if __name__ == "__main__":
    LOGGER_FORMAT = "[%(asctime)s] %(message)s"
    logging.basicConfig(filename="tests.log", level=logging.INFO, encoding="utf-8", filemode="w", format=LOGGER_FORMAT)
    start_time = time.time()
    print("+-----------------------------+----------+---------------+--------------+------------+-------------+")
    print("|          Song Name          | Map Diff | Computed Diff | Speed Rating | Aim Rating |  TT Rating  |")
    print("+-----------------------------+----------+---------------+--------------+------------+-------------+")
    for tmb_file in os.listdir("tmbs/"):
        if not tmb_file.endswith(".tmb"):
            continue
        tmb = read_tmb(f"tmbs/{tmb_file}")
        song_name = tmb.short_name[:]
        map_diff = tmb.difficulty
        diff_calc = calc_diff(tmb)
        tt_rating = calc_tt(tmb, diff_calc[0], diff_calc[1])
        print(f"|{song_name[:29]:^29s}| {map_diff:^8d} | {diff_calc[0]:13f} | {diff_calc[1]:12f} | {diff_calc[2]:10f} | {tt_rating:11f} |")
    print("+-----------------------------+----------+---------------+--------------+------------+-------------+")
    end_time = time.time()
    print(f"Report generated at {time.asctime(time.gmtime())}")
    print(f"Generated in {end_time - start_time:f} seconds")
    