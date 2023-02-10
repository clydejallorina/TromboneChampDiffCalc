import json
import math
import os
import logging
import matplotlib
import argparse
from dataclasses import dataclass
from typing import List, Optional

# CURRENTLY BEING BUILT, NOWHERE NEAR PRODUCTION

@dataclass
class FrameData:
    pass

@dataclass
class Replay:
    username:str
    starttime:int
    endtime:int
    uuid:str
    input:str
    song:str
    samplerate:int
    scrollspeed:float
    pluginbuilddate:int
    gameversion:str
    songhash:str
    finalscore:int
    maxcombo:int
    finalnotetallies:List[int]
    framedata:List[List[int]]
    notedata:List[List[int]]
    tootdata:List[List[int]]
    servertime:Optional[float]
    hmac:Optional[str]

def json_to_replay(file:str) -> Replay:
    pass

def read_ttr(filename:str) -> Optional[Replay]:
    if not filename.endswith(".ttr"):
        logging.warning("File is not a ttr file! Ignoring.")
        return None
    if not os.path.exists(filename):
        logging.error("File doesn't exist!")
        return None
    with open(filename, encoding="utf-8") as file:
        ttr = json_to_replay(file.read())
        if ttr == None:
            logging.error("Parsing failed for %s", filename)
        return ttr

def generate_figure():
    pass

def main():
    pass

if __name__ == "__main__":
    logging.basicConfig(filename="ttr.log", level=logging.INFO, encoding="utf-8", filemode="w")
    parser = argparse.ArgumentParser(description="Trombone Champ replay analysis tool")
    parser.add_argument("filename", metavar="filename", type=str, help="Target .ttr to analyze")
    args = parser.parse_args()
    tmb = read_ttr(args.filename)
    main()
