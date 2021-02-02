#!/usr/bin/python3

import json
import sys
import re

ssc_metadata_tags = [
    "VERSION", "TITLE", "SUBTITLE", "ARTIST", "TITLETRANSLIT",
    "SUBTITLETRANSLIT", "ARTISTTRANSLIT", "GENRE", "ORIGIN", "CREDIT",
    "BANNER", "BACKGROUND", "PREVIEWVID", "CDTITLE", "MUSIC","OFFSET",
    "SAMPLESTART", "SAMPLELENGTH", "SELECTABLE", "SONGTYPE","SONGCATEGORY",
    "VOLUME", "BPMS", "TIMESIGNATURES", "TICKCOUNTS","COMBOS", "SPEEDS",
    "SCROLLS", "LABELS", "BGCHANGES", "FGCHANGES", "DISPLAYBPM", "STOPS"
]

chart_metadata_tags = [
    "NOTEDATA", "CHARTNAME", "STEPSTYPE", "DESCRIPTION", "DIFFICULTY", "METER",
    "RADARVALUES", "CREDIT", "OFFSET", "BPMS", "STOPS", "DELAYS", "WARPS",
    "TIMESIGNATURES", "TICKCOUNTS", "COMBOS", "SPEEDS", "SCROLLS", "FAKES",
    "LABELS", "NOTES"
]

if (len(sys.argv) - 1) > 0:
    sscpath = sys.argv[1]
else:
    print("Please enter the path to the SSC file you'd like to parse.")
    exit()

with open(sscpath, "r") as sscfile:
    sscdata = sscfile.read()

def remove_comments(sscdata):
    pattern = r"(?:\/\*(?:[\s\S]*?)\*\/)|(?:([\s])+\/\/(?:.*)$)"
    filtered = re.sub(pattern, "", sscdata, flags=re.MULTILINE)
    return filtered

def songdata_to_dict(sscdata):
    sscdict = {}
    num_charts = 0
    all_the_other_data = {}
    for line in sscdata.splitlines():
        if line.startswith("#"):
            variable = line[1:].split(":")
            variable[1] = variable[1][:-1]
            if variable[0] == "NOTEDATA":
                num_charts += 1
                sscdict["num_charts"] = num_charts
                sscdict[num_charts] = {}
                sscdict[num_charts][variable[0]] = variable[1]
            elif variable[0] in ssc_metadata_tags:
                sscdict[variable[0]] = variable[1]
            elif variable[0] in chart_metadata_tags:
                try:
                    sscdict[num_charts][variable[0]] = variable[1]
                except KeyError as e:
                    print(f"KeyError: {e}")
                    print(variable[0])
            else:
                print(f"Unrecognized tag {variable[0]}")
    return sscdict

sscdata = remove_comments(sscdata)
sscdata = songdata_to_dict(sscdata)

print(f"""-----
Song: {sscdata["TITLE"]}
Artist: {sscdata["ARTIST"]}
Number of charts: {sscdata["num_charts"]}
-----""")

filename = sys.argv[1].split(".")[0]

try:
    with open(f"{filename}.json", "w") as f:
        json.dump(sscdata, f, indent=2)
except OSError as e:
    print(f"Error saving JSON data:\n{e}")

print("Saved JSON data!")
