#!/usr/bin/env python3

import datetime
import json
import os
import sys

import srt

def parse_to_timedelta(time_str):
    t = datetime.datetime.strptime(time_str, "%H:%M:%S,%f")
    return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

def gen_srt_subtitles(in_f):
    json_subs = json.load(in_f)

    for e in json_subs["file_captions"]:
        number = e["number"]
        start_time = parse_to_timedelta(e["startTime"])
        stop_time = parse_to_timedelta(e["stopTime"])
        text = e["text"]

        yield srt.Subtitle(number, start_time, stop_time, text)

def main():
    for fpath in sys.argv[1:]:
        if not fpath.endswith(".json"):
            print("skipping", fpath)
            continue

        path, _ = os.path.splitext(fpath)
        output_fpath = path + ".srt"
        if os.path.exists(output_fpath):
            print("skip output to existing", output_fpath)
            continue

        print(fpath, "-->", output_fpath)
        with open(fpath) as in_f, open(output_fpath, "w") as out_f:
            out_s = srt.compose(gen_srt_subtitles(in_f))
            out_f.write(out_s)

if __name__ == "__main__":
    main()
