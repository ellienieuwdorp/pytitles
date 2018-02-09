#!/usr/bin/env python

import getpass
import argparse
import os
import gzip
import sys
import urllib.request

from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File

__author__ = "Luuk Nieuwdorp"
__version__ = "0.1.0"
__license__ = "MIT"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to the file you want to download subtitles for", type=str)

    args = parser.parse_args()

    if os.path.exists(args.file):
        f = File(os.path.abspath(args.file))
        path, file = os.path.split(args.file)
        path_full_nofile = os.path.abspath(path)
        path_file = file
        path_file_noext = os.path.splitext(args.file)[0]
    else:
        sys.exit("File does not exist")

    ost = OpenSubtitles()

    username = input("Please input your OpenSubtitles.org username: ")
    password = getpass.getpass("Please input your OpenSubtitles.org password: ")
    print("Logging in, please wait...")
    ost.login(username, password)
    print("Successfully logged in!")

    hash = f.get_hash()
    size = f.size

    print("Scouring the web for subtitles, please wait...")
    data = ost.search_subtitles([{'sublanguageid': 'en', 'moviehash': hash, 'moviebytesize': size}])
    data = ost.search_subtitles([{'sublanguageid': 'eng', 'moviehash': hash, 'moviebytesize': size}])
    bestdic = None

    highestsum = 0
    for dict in data:
        sumvotes = int(dict.get('SubSumVotes'))
        if sumvotes > highestsum:
            sumvotes = highestsum
            bestdic = dict

    print("Subtitle found with", bestdic.get('SubSumVotes'), "upvotes.")
    print("Downloading subtitles, please wait...")
    urllib.request.urlretrieve(bestdic.get('SubDownloadLink'), path_full_nofile + "/" + path_file_noext + ".srt.gz")
    print("Subtitle downloaded!")
    print("Unzipping subtitle, please wait...")
    inF = gzip.open(path_full_nofile + "/" + path_file_noext + ".srt.gz", "rb")
    outF = open(path_full_nofile + "/" + path_file_noext + ".srt", "wb")
    outF.write(inF.read())
    inF.close()
    outF.close()
    os.remove(path_full_nofile + "/" + path_file_noext + ".srt.gz")
    print("Done!")


if __name__ == "__main__":
    main()
