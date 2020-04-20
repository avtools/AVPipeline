from pytube import YouTube
import argparse
from pathlib import Path
import os
import csv


def argument_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input_csv', nargs='+',
                        help='A CSV file containing links to youtube links of audios to be extracted')
    parser.add_argument('--output-path', default="audio_samples", help='')
    return parser.parse_args()


def on_complete(stream, filehandle):
    print(stream)
    print("done")
    return None


def parse_csv(input_csv):
    with open(input_csv, 'r') as input_file:
        Dict = csv.DictReader(input_file)
        return list(Dict)


if __name__ == "__main__":
    args = argument_parser()
    download_path = args.output_path
    video_list = parse_csv(args.input_csv[1])
    print(download_path)
    for x in video_list:
        youtube_link = x["URL"]
        new_name = download_path + "/" + x["Rename"] + ".mp4"
        print(youtube_link)
        yt = YouTube(youtube_link, on_complete_callback=on_complete)
        audio = yt.streams.get_audio_only().download(download_path)
        os.rename(audio, new_name)
