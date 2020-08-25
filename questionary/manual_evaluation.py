import questionary
import sys
from io import open
from argparse import ArgumentParser
from json import load, loads, dumps, dump

# ipython manual_evaluation.py  eval_data/lyrics_question-generation-pipeline-t5-small-modell.json qg qg-p-t5-small
# ipython manual_evaluation.py  eval_data/lyrics_question-generation-pipeline-t5-small-modell.json e2e e2e-p-t5-small
# ipython manual_evaluation.py  eval_data/hypothesis_t5-base-fine-tuned-qg-hl_tweet_manual.txt h base-qg-manual

parser = ArgumentParser()

parser.add_argument("eval_data")
parser.add_argument("eval_format")
parser.add_argument("eval_name")
args = parser.parse_args()

if args.eval_format == 'h':
    with open(args.eval_data, 'r') as fp:
        eval_data = fp.readlines()
else:
    with open(args.eval_data, 'r') as fp:
        eval_data = load(fp)


def write_json_file(dirname, answers, name):
    with open(dirname + 'lyrics_manual_evaluation_' + name + '.json', 'w') as fp:
        dump(answers, fp)

def evaluate_data():
    e = {}
    try:

        fluent = int(questionary.select(
            "Do you find this generated question fluent? Could the question have been produced by a native speaker?",
                choices=[
                '5',
                '4',
                '3',
                '2',
                '1',
                ]).ask())
        e['fluency'] = fluent
        contain_a = int(questionary.select(
            "Does this generated question contain the answer?",
                choices=[
                '1',
                '2',
                '3',
                '4',
                '5',
                ]).ask())
        e['answer'] = contain_a
        relevant = int(questionary.select(
                "How relevant is the generated question to the given lyric?",
                choices=[
                '5',
                '4',
                '3',
                '2',
                '1',
                ]).ask())
        e['relevance'] = relevant
        grammar = int(questionary.select(
                "Is the generated question grammatically correct, without taking into account the correctness of the information?",
                choices=[
                '5',
                '4',
                '3',
                '2',
                '1',
                ]).ask())
        e['grammar'] = grammar
        readable = int(questionary.select(
                "Is the generated question easily read?",
                choices=[
                '5',
                '4',
                '3',
                '2',
                '1',
                ]).ask())
        e['readibility'] = readable
        syntax = int(questionary.select(
                "Is the syntax of the generated question correct? ",
                choices=[
                '5',
                '4',
                '3',
                '2',
                '1',
                ]).ask())
        e['syntax'] = syntax
        intelligible = int(questionary.select(
                "How intelligible is the generated question? ",
                choices=[
                '5',
                '4',
                '3',
                '2',
                '1',
                ]).ask())
        e['intelligible'] = intelligible
        redundant = int(questionary.select(
                "Is there any redundancy in the generated question?",
                choices=[
                '1',
                '2',
                '3',
                '4',
                '5',
                ]).ask())
        e['redundancy'] = redundant
        quality = int(questionary.select(
                "How is the overall quality of the generated question? Is the question meaningful?",
                choices=[
                '5',
                '4',
                '3',
                '2',
                '1',
                ]).ask())
        e['quality'] = quality
        slang = questionary.confirm("Are there any slang words in the generated question?").ask()
        e['slang'] = slang
        slangcount = int(questionary.text("How many slang words are in the generated question?").ask())
        e['slangcount'] = slangcount
    except ValueError:
        print("trying hard arent we")
        e['error'] = ''
    return e

eval_answers = []
err_count = 0
for i in eval_data:
    
    if args.eval_format == 'e2e':
        print('Lyrics: ' + i['lyrics'])
        print('-------------------------------------')
        if 'error' in i.keys():
            err_count += 1
            continue
        task = i['task']
        l = {}
        l['lyrics'] = i['lyrics']
        qs = []
        for elem in task:

            print('Question: ' + elem)
            print('-------------------------------------')
            e = evaluate_data()
            q = {}
            q['question'] = elem
            q['evaluation'] = e
            qs.append(q)
            e = {}
    elif args.eval_format == 'qg':

        print('Lyrics: ' + i['lyrics'])

        print('-------------------------------------')
        if 'error' in i.keys():
            err_count += 1
            continue
        task = i['task']
        l = {}
        l['lyrics'] = i['lyrics']
        qs = []
        for elem in task:
            print('Question: ' + elem['question'])
            print('-------------------') 
            e = evaluate_data()
            q = {}
            q['question'] = elem['question']
            q['evaluation'] = e
            qs.append(q)
            e = {}
    elif args.eval_format == 'h':
        qs = []
        l = {}
        print('Question: ' + i)
        print('-------------------------------------')
        e = evaluate_data()
        q = {}
        q['question'] = i
        q['evaluation'] = e
        qs.append(q)
        e = {}
    else:
        print("undefined format. exiting")
        sys.exit(0)

    l['ques_eval'] = qs
    eval_answers.append(l)

write_json_file('',eval_answers,"evaluation"+args.eval_name)

print("Overall error count for not evaluated lyrics: " + str(err_count))

