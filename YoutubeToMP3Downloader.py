#!/usr/bin/python3

'''
Usage: youtube_downloader.py [-h] [-v] [-u URL] [-d DIRECTORY]

Description

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbose output
  -u URL, --url URL     The YouTube URL to download as MP3
  -d DIRECTORY, --directory DIRECTORY
                        The destination directory for the output file
'''

import argparse
import logging
import sys
from pytube import YouTube
import os

parser = argparse.ArgumentParser(description='This tool is made to download the MP3 audio stream from a YouTube video.')

parser.add_argument('-v', '--verbose',   action='store_true', help='Enable verbose output', default=False)
parser.add_argument('-u', '--url',       action='store', type=str, help='The YouTube URL to download as MP3')
parser.add_argument('-d', '--directory', action='store', type=str, help='The destination directory for the output file')

if len(sys.argv) < 3:
    parser.print_help()
    exit(1)

args = parser.parse_args()

level = logging.DEBUG if args.verbose else logging.INFO
logging.basicConfig(level=level, format='[%(asctime)s.%(msecs)03d]  %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logging.debug("Verbose mode enabled")

if args.url is None:
	parser.print_help()
	exit(1)

yt = YouTube(str(args.url))
video = yt.streams.filter(only_audio=True).first()

if args.directory is not None:
	destination = args.directory
	logging.debug("Destination folder set to " + str(destination))
else:
	destination = '.'
	logging.debug("Destination folder set to .")

out_file = video.download(output_path=destination)
base,ext = os.path.splitext(out_file)
new_file = base+'.mp3'
os.rename(out_file, new_file)

logging.info(str(yt.title) + " has been successfully downloaded in mp3 format")
