from TMBToDiff import *
import os
import sys
import logging

if __name__ == "__main__":
    LOGGER_FORMAT = "[%(asctime)s] %(message)s"
    logging.basicConfig(filename="tests.log", level=logging.INFO, encoding="utf-8", filemode="w", format=LOGGER_FORMAT)
    for tmb_file in os.listdir("tmbs/"):
        if not tmb_file.endswith(".tmb"):
            continue
        tmb = read_tmb(f"tmbs/{tmb_file}")
        print(f"{tmb}: {calc_diff(tmb)}")
        