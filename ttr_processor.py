import json
import math
import os
import logging
import matplotlib
import argparse
import matplotlib.pyplot as plt
import zipfile
from dataclasses import dataclass, fields
from typing import List, Optional

# CURRENTLY BEING BUILT, NOWHERE NEAR PRODUCTION

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

def json_to_replay(file:str) -> Optional[Replay]:
    try:
        rep:dict = json.loads(file)
        fields_in_rep = [key for key in rep if key in fields(Replay)]
        filtered = {k : v for k, v in rep.items() if k in fields_in_rep}
        return Replay(**filtered)
    except:
        logging.error("Unable to parse replay, cannot load JSON.")
        return None

def read_ttr(filename:str) -> Optional[Replay]:
    if not filename.endswith(".ttr"):
        logging.warning("File is not a ttr file! Ignoring.")
        return None
    if not os.path.exists(filename):
        logging.error("File doesn't exist!")
        return None
    with zipfile.ZipFile(filename, "r") as zipped:
        namelist = zipped.namelist()
        if len(namelist) != 1:
            logging.error("This zip file is only supposed to contain a single file!")
            return None
        file = zipped.read(namelist[0])
        ttr = json_to_replay(file.read())
        if ttr == None:
            logging.error("Parsing failed for %s", filename)
        return ttr

def generate_graph(x, y, x_label="", y_label="", title=""):
    title = title.strip()
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel=x_label, ylabel=y_label, title=title)
    ax.grid()
    fig.set_size_inches(18.5, 10.5)
    fig.set_dpi(400)
    fig.tight_layout()
    try:
        logging.info(f"Generating graph: graphs/{title}.png")
        fig.savefig(f"graphs/{title}")
    except Exception as e:
        logging.error(f"Failed to generate graph: {e}")
    plt.close(fig)

def main():
    pass

if __name__ == "__main__":
    logging.basicConfig(filename="ttr.log", level=logging.INFO, encoding="utf-8", filemode="w")
    parser = argparse.ArgumentParser(description="Trombone Champ replay analysis tool")
    parser.add_argument("filename", metavar="filename", type=str, help="Target .ttr to analyze")
    args = parser.parse_args()
    tmb = read_ttr(args.filename)
    main()
