#!/usr/bin/python3
# python3 prepare_lyrics.py urbandict-word-defs.csv english_cleaned_lyrics.csv
from os.path import isfile
import sys
from io import open as iopen
from argparse import ArgumentParser
from json import load, loads, dumps, dump
import csv
import pickle


tagged_notranslate = dict()

LYRICS_COUNT = 56

def write_json_file(lyrics, name):
    with iopen('lyrics_' + name + '_slang_automatic.json', 'w') as fp:
        dump(lyrics, fp)


def find_slang(urban, tweet):
    slang = []
    for i in tweet.split():
        if i in urban and i not in slang:
            slang.append(i)
    return slang


def write_lyrics_text(lyrics, name):
    with iopen('lyrics_' + name + '_automatic_reference.txt', 'w') as fp:
        for item in lyrics:
            fp.write("%s\n" % item)

if __name__ == '__main__':
    # convert lyrics from csv to a list and json for further processing
    # python3 prepare_lyrics.py urbandict-word-defs.csv english_cleaned_lyrics.csv
    parser = ArgumentParser()
    # provide the file containing the urban dictionary. it should be in csv format
    # containing the columns word_id,word,up_votes,down_votes,author,definition
    parser.add_argument("urban_dict")
    # containing the columns word_id,word,up_votes,down_votes,author,definition
    parser.add_argument("lyrics")

    args = parser.parse_args()

    if not isfile(args.urban_dict):
        print("please check your urban dictionary file")
        sys.exit(1)

    if not isfile(args.lyrics):
        print("please check your lyrics csv file")
        sys.exit(1)

    with iopen("urban.txt", "rb") as fp:
        urban = pickle.load(fp)

    with iopen("urban_low.txt", "rb") as fp:
        urban_low = pickle.load(fp)


    lyrics = []
    lyrics_json = {}
    with iopen(args.lyrics, 'r') as f:
        csv_reader = csv.DictReader(f, delimiter=',')
        lyrics_json["version"] = "v1.0"
        data = []
        count = 0
        songs = []
        for lines in csv_reader:
            d = {}
            if count == LYRICS_COUNT:
                break
            count += 1
            artist = lines['artist']
            song = lines['song']
            text = lines['lyrics']

            d['artist'] = artist
            d['song'] = song
            d['text'] = text
            slang = find_slang(urban_low, text.lower())
            d['slang'] = slang 
            if lines['song'] in songs:
                print('DOUBLE: ' + lines['song'])
                continue
            songs.append(lines['song'])
            data.append(d)
            lyrics.append(text)

        lyrics_json['data'] = data
        print("the songs are: " )
        print(songs)
        print(len(songs))

    #urban = []
    #urban_low = []
    #with iopen(args.urban_dict, 'r') as f:
    #    csv_reader = csv.DictReader(f, delimiter=',')
    #    for lines in csv_reader:
    #        word = lines['word']
    #        urban.append(word)
    #        urban_low.append(word.lower())
 
   #with iopen("urban.txt", "wb") as fp:
     #   pickle.dump(urban,fp)

    #with iopen("urban_low.txt", "wb") as fp:
    #    pickle.dump(urban_low,fp)

  # for faster processing

    write_lyrics_text(lyrics, 'english')
    write_json_file(lyrics_json, 'english')
