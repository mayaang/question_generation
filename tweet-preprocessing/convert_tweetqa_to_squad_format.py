#!/usr/bin/python3
from os.path import isfile
from re import match
import sys
from sys import exit
from io import open as iopen
from argparse import ArgumentParser
from json import load, loads, dumps, dump
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from collections import deque
from logging import basicConfig, getLogger, DEBUG, Formatter, FileHandler
import csv
import pickle

# TweetQA TEST JSON schema
TWEET_QA_TEST_SCHEMA = {
        "type":"array",
        "items":
        [
         {
                "type":"object",
                "required": ["Question", "Tweet","qid"],
                "properties":
                {
                        "Question": {"type" : "string"},
                        "Tweet": {"type" : "string"},
                        "qid": {"type" : "string"}
                }
         }
        ]
 }


# TweetQA JSON schema
TWEET_QA_SCHEMA = {
        "type":"array",
        "items":
        [
         {
                "type":"object",
                "required": ["Question", "Answer", "Tweet","qid"],
                "properties":
                {
                        "Question": {"type" : "string"},
                        "Answer": {"type" : "array"},
                        "Tweet": {"type" : "string"},
                        "qid": {"type" : "string"}
                }
         }
        ]
 }

TWEET_QA_QUESTION_KEY = "Question"
TWEET_QA_ANSWER_KEY = "Answer"
TWEET_QA_TWEET_KEY = "Tweet"
TWEET_QA_QID_KEY = "qid"

# SQUAD JSON schema
SQUAD_SCHEMA = {
        "type:": "object",
        "required":["version","data"],
        "properties":
        {
            "version":{"type":"string"},
            "data":{

"type":"array",
"items":
[
    {
    "type":"object",
    "required": ["title", "paragraphs"],
    "properties":
    {
        "title": {"type" : "string"},
        "paragraphs":
        {
            "type" : "array",
            "items":
            [
                {
                "type": "object",
                "required": ["qas", "context", "slang"],
                "properties":
                {
                    "qas":
                    {
                        "type":"array",
                        "items":
                        [
                            {
                            "type": "object",
                            "required": ["question", "id","answers"],
                            "properties":
                            {
                                "question": {"type":"string"},
                                "id": {"type":"string"},
                                "answers":
                                {
                                    "type":"array",
                                    "items":
                                    [
                                        {
                                        "type":"object",
                                        "required": ["text", "answer_start"],
                                        "properties":
                                        {
                                            "text": {"type":"string"},
                                            "answer_start": {"type":"integer"}
                                        }
                                        }
                                    ]
                                },
                                "is_impossible": {"type":"boolean"}
                            }
                            }
                        ]
                    }
                }
                }
            ],
            "context": {"type" : "string"},
            "slang": {"type" : "array"}
        }
    }
    }
]
}
}
}


tagged_notranslate = dict()

basicConfig(level=DEBUG)
logger = getLogger(__name__)
LOG_FILE_NAME='convert_to_squad.log'

def configure_logging(logname):
    handler = FileHandler(logname)
    handler.setLevel(DEBUG)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def convert_and_write_to_file(tweet_json, name, urban, urban_low, debug, filename):
    '''
    for every given json from the Tweet QA dataset, convert it to squad format
    add slang found in the tweet as of the urban dictionary and add a new variable
    containing the slang words which were found in the tweets for every tweet
    write the newly formatted Tweet QA data to a file
    '''
    tweet_sq = convert_to_squad(tweet_json, urban, urban_low, filename)
    if debug:
        logger.debug("------------------------------------------------")
        logger.debug("------------------------------------------------")
        logger.debug("------------------------------------------------")
        logger.debug("------------------------------------------------")
        logger.debug(dumps(tweet_sq, indent=4))
        logger.debug("------------------------------------------------")
        logger.debug("------------------------------------------------")
        logger.debug("------------------------------------------------")
        logger.debug("------------------------------------------------")
        logger.debug("------------------------------------------------")

    with iopen('tweet_' + name + '_squad_automatic.json', 'w') as fp:
        dump(tweet_sq, fp)


def validate_tweet_qa_json_schema(tweet_json, schema,  name):
    # validate the Tweet QS JSON file
    try:
        validate(tweet_json, schema)
    except ValidationError as e:
        logger.error("SEVERE! invalid json input for file %s" %(name))
        logger.error("ValidationError: ", exc_info=True)
        exit(1)

def find_slang(urban, tweet):
    slang = []
    for i in tweet.split():
        if i in urban and i not in slang:
            slang.append(i)
    return slang

def slangify_test_json(tweet_json, name, urban, urban_low):
    questions = []
    q = {}
    if isinstance(tweet_json, list):
        for item in tweet_json:
            if isinstance(item, dict):
                context = item[TWEET_QA_TWEET_KEY]
                slang = find_slang(urban_low, context.lower())
                q["Question"] = item[TWEET_QA_QUESTION_KEY]
                q["Tweet"] = context
                q['Slang'] = slang
                q["qid"] = item[TWEET_QA_QID_KEY]
                questions.append(q)
                slang = []
                q = {}
            else:
                logger.error("Something went wrong with the tweet qa json file %s", args.tweet_test)
                exit(1)
    else:
        logger.error("Something went wrong with the tweet qa json file %s", args.tweet_test)
        exit(1)

    with iopen('tweet_' + name + '_slang_automatic.json', 'w') as fp:
        dump(questions, fp)

def strip_punctuation(word):
    return word.lower().strip().replace(".","").replace("!","").replace(",","").replace(":","").replace(";","").replace("?","")


def write_reference_questions(tweet_json, name, filename):
    if isinstance(tweet_json, list):
        questions = []
        for item in tweet_json:
            if isinstance(item, dict):
                questions.append(item[TWEET_QA_QUESTION_KEY])
            else:
                logger.error("Something went wrong with the tweet qa json file %s", filename)
                exit(1)
    else:
        logger.error("Something went wrong with the tweet qa json file %s", filename)
        exit(1)

    # small fast fix
    questions.pop()
    with iopen('tweet_' + name + '_automatic_reference.txt', 'w') as fp:
        for item in questions:
            fp.write("%s\n" % item)



def convert_to_squad(tweet_json, urban, urban_low, filename):
    tweet_test_sq = {}

    tweet_test_sq["version"] = "v2.0"
    data = []

    if  isinstance(tweet_json, list):
        paragraphs = []
        d = {}
        qas = []
        ps = []
        p = {}
        q = {}
        answers = []
        is_imp = False
        count  = 1
        context = ""
        slang = []
        uff = 0
        for item in tweet_json:
            if isinstance(item, dict):
                if context != item[TWEET_QA_TWEET_KEY]:
                    if context != "":
                        count += 1
                        d["title"] = "title" + str(count)
                        p["qas"] = qas
                        p["context"] = context
                        #slang = find_slang(urban, context)
                        slang = find_slang(urban_low, context.lower())
                        p["slang"] = slang
                        slang = []
                        qas = []
                        ps.append(p)
                        p = {}
                        d["paragraphs"] = ps
                        ps = []
                        data.append(d)
                        d = {}
                context = item[TWEET_QA_TWEET_KEY]
                q["question"] = item[TWEET_QA_QUESTION_KEY]
                q["id"] = item[TWEET_QA_QID_KEY]
                ans = item[TWEET_QA_ANSWER_KEY]
                for a in ans:
                    answer = {}
                    answer_start = context.lower().strip().find(strip_punctuation(a))
                    if answer_start == -1:
                        for word in a.split():
                            if word not in ["a", "an", "the"]:
                                answer_start = context.lower().strip().find(strip_punctuation(word))
                        if answer_start == -1:
                            is_imp = True
                    answer["text"] = a
                    answer["answer_start"] = answer_start
                    answers.append(answer)
                q["answers"] = answers
                q["is_impossible"] = is_imp
                qas.append(q)
                q = {}
                is_imp = False
                answers = []
            else:
                logger.error("Something went wrong with the tweet qa json file %s", filename)
                exit(1)
    else:
        logger.error("Something went wrong with the tweet qa json file %s", filename)
        exit(1)
    tweet_test_sq["data"] = data

    # validate the SQUAD JSON file
    try:
        validate(tweet_test_sq, SQUAD_SCHEMA)
    except ValidationError as e:
        logger.error("SEVERE! new constructed Squad json is invalid")
        logger.error("ValidationError: ", exc_info=True)
        exit(1)

    return tweet_test_sq


if __name__ == '__main__':
    # convert TWEET QA json dataset into the format taken by SQUAD v1.1 dataset
    # python3 convert_tweetqa_to_squad_format.py urbandict-word-defs.csv train.json dev.json test.json  --debug
    parser = ArgumentParser()
    # provide the file containing the urban dictionary. it should be in csv format
    # containing the columns word_id,word,up_votes,down_votes,author,definition
    parser.add_argument("urban_dict")
    # provide the file containing the train data from the TweetQS dataset in json format
    parser.add_argument("tweet_train")
    # provide the file containing the dev data from the TweetQS dataset in json format
    parser.add_argument("tweet_dev")
    # provide the file containing the test data from the TweetQA dataset in json format
    parser.add_argument("tweet_test")

    # whether or not to write debug json files
    parser.add_argument("--debug", action='store_true')


    args = parser.parse_args()
    configure_logging(LOG_FILE_NAME)


    if not isfile(args.urban_dict):
        print("please check your urban dictionary file")
        logger.error("please check your urban dictionary file")
        sys.exit(1)

    if not isfile(args.tweet_test):
        print("please check your TweetQA test json file")
        logger.error("please check your TweetQA test file")
        sys.exit(1)

    if not isfile(args.tweet_train):
        print("please check your TweetQA train json file")
        logger.error("please check your TweetQA train file")
        sys.exit(1)

    if not isfile(args.tweet_dev):
        print("please check your TweetQA dev json file")
        logger.error("please check your TweetQA dev file")
        sys.exit(1)


    urban = []
    urban_low = []
    with iopen(args.urban_dict, 'r') as f:
        csv_reader = csv.DictReader(f, delimiter=',')
        for lines in csv_reader:
            word = lines['word']
            urban.append(word)
            urban_low.append(word.lower())
    with iopen("urban.txt", "wb") as fp:
        pickle.dump(urban,fp)

    with iopen("urban_low.txt", "wb") as fp:
        pickle.dump(urban_low,fp)

  # for faster processing
#    with iopen("urban.txt", "rb") as fp:
#        urban = pickle.load(fp)

#    with iopen("urban_low.txt", "rb") as fp:
#        urban_low = pickle.load(fp)

    with iopen(args.tweet_test, 'r') as fp:
        tweet_test = load(fp)

    with iopen(args.tweet_train, 'r') as fp:
        tweet_train = load(fp)

    with iopen(args.tweet_dev, 'r') as fp:
        tweet_dev = load(fp)


    validate_tweet_qa_json_schema(tweet_train, TWEET_QA_SCHEMA, args.tweet_train)
    validate_tweet_qa_json_schema(tweet_dev, TWEET_QA_SCHEMA, args.tweet_dev)
    validate_tweet_qa_json_schema(tweet_test, TWEET_QA_TEST_SCHEMA, args.tweet_test)



    logger.debug("------------------------------------------------")
    logger.debug("------------------------------------------------")
    logger.debug(args.tweet_train)
    logger.debug("------------------------------------------------")
    logger.debug("------------------------------------------------")
    convert_and_write_to_file(tweet_train, 'train', urban, urban_low, args.debug, args.tweet_train)
    logger.debug("------------------------------------------------")
    logger.debug("------------------------------------------------")
    logger.debug(args.tweet_dev)
    logger.debug("------------------------------------------------")
    logger.debug("------------------------------------------------")

    convert_and_write_to_file(tweet_dev, 'dev', urban, urban_low, args.debug, args.tweet_dev)
    write_reference_questions(tweet_dev, 'dev', args.tweet_dev)
    logger.debug("------------------------------------------------")
    logger.debug("------------------------------------------------")
    logger.debug(args.tweet_test)
    logger.debug("------------------------------------------------")
    logger.debug("------------------------------------------------")
    slangify_test_json(tweet_test, 'test', urban, urban_low)
