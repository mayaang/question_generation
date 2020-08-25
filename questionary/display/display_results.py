from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from argparse import ArgumentParser
from json import load, loads, dumps, dump
from os.path import isfile
from io import open as iopen

def create_barplot(result, x_t, y_t, title, text):
    x_labels = ['1', '2', '3', '4', '5'] 
    y_values = [result.count(1), result.count(2), result.count(3), result.count(4),result.count(5)] 
    
    font = {'family' : 'Times New Roman',
        'weight' : 'bold',
        'size'   : 18}
    plt.rc('font', **font)
    figure(num=None, figsize=(12, 6))
    y_pos=np.arange(len(x_labels))
    plt.bar(y_pos, y_values, width=0.5, color = 'c', label='legend title')
    plt.xticks(y_pos, x_labels)
    plt.legend(loc='best')
    plt.ylabel(y_t)
    plt.xlabel(x_t)
    plt.title(title)
    plt.savefig( text + "_" + title.replace(' ','_').replace('/', '-') + '.png', dpi=300)


def read_json(filename):
    with iopen(filename, 'r') as fp:
        data = load(fp)
    return data


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("eval_data")
    parser.add_argument("text_data")

    args = parser.parse_args()
    if not isfile(args.eval_data):
        print("please check your TweetQA test json file")
        sys.exit(1)

    text = args.text_data

    data = read_json(args.eval_data)

    length = 0
    count = 0
    results = {}
    results['question'] = []
    results['fluency'] = []
    results['answer'] = []
    results['relevance'] = []
    results['grammar'] = []
    results['readibility'] = []
    results['syntax'] = []
    results['redundancy'] = []
    results['quality'] = []
    results['slangcount'] = 0
    for item in data:
        for el in item['ques_eval']:
            if 'question' in el.keys():
                count += 1
                eva = el['evaluation']
                length += len(el['question'])
                results['fluency'].append(eva['fluency']) 
                results['answer'].append(eva['answer']) 
                results['relevance'].append(eva['relevance']) 
                results['grammar'].append(eva['grammar']) 
                results['readibility'].append(eva['readibility'])
                results['syntax'].append(eva['syntax']) 
                results['redundancy'].append(eva['redundancy']) 
                results['quality'].append(eva['quality']) 
                results['slangcount'] += eva['slangcount']



    create_barplot(results['fluency'], "possible answers", "fluency", "Fluency/Nativeness of the generated question", text)
    create_barplot(results['answer'], "possible answers", "answer", "Generated question contains the answer", text)
    create_barplot(results['relevance'], "possible answers", "relevance", "How relevant is the generated question to the " + text, text)
    create_barplot(results['grammar'], "possible answers", "grammar", "Grammaticality of the generated question", text)

    create_barplot(results['readibility'], "possible answers", "readibility", "Readibility of the generated question", text)
    create_barplot(results['syntax'], "possible answers", "syntax", "Syntax of the generated question", text)
    create_barplot(results['redundancy'], "possible answers", "redundancy", "Redundancy of the generated question", text)
    create_barplot(results['quality'], "possible answers", "quality", "Overall quality of the generated question", text)

    print('average length for chararcters in a question')

    print(length/count)
    print('count of slang terms for the ' + str(count) + " questions")
    print(results['slangcount'])


