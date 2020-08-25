This github repo is a fork of https://github.com/patil-suraj/question_generation. It was utilized in a student project on the go.

## Main

1. In order to be able to reproduce the results the first thing to do it to clone the repository

`git clone https://github.com/mayaang/question_generation.git`
`cd question_generation`

2. Download the urban dictionary from https://www.kaggle.com/therohk/urban-dictionary-words-dataset/datachro

3. `mv urbandict-word-defs.csv tweet-preprocessing`
4. `cd tweet-preprocessing`
Step 5 converts the TweetQA dataset into SQUAD format so it can be used by the pipelines provided by https://github.com/patil-suraj/question_generation
5. `python3 convert_tweetqa_to_squad_format.py urbandict-word-defs.csv train.json dev.json test.json  --debug` or use the tweet-preprocess Jupyter notebook
6. `mv tweet_dev_squad_automatic.json ../data/tweet_multitask/`
7. `mv tweet_test_slang_automatic.json ../data/tweet_multitask/`
8. `mv tweet_train_squad_automatic.json ../data/tweet_multitask/`
9. `mv tweet_dev_automatic_reference.txt ../data/tweet_multitask/`
10. open tweet_question_generation Jupyter Notebook and run for automatically generated TweetQA data in SQUAD format
11. open tweet_question_generation_corrected_data Jupyter Notebook and run for manually edited TweetQA data in SQUAD format


## Testing form scratch using rap lyrics from Metro Lyrics.

1. `cd lyrics`
2. `python3 prepare_lyrics.py urbandict-word-defs.csv english_cleaned_lyrics_edit.csv`
3. Run the original_tweet_question_generation_e2e_lyrics.ipynb Notebook, to get the generated questions for the four settings:
	a. question-generation pipeline pretrained T5 small model
	b. question-generation pipeline pretrained T5 base model
	c. e2e pipeline pretrained T5 small model
	d. e2e pipeline pretrained T5 base model
4.
	a. If you want to evaluate the questions yourself please run:

`ipython manual_evaluation.py  eval_data/lyrics_question-generation-pipeline-t5-small-modell.json qg qg-p-t5-small`
`ipython manual_evaluation.py  eval_data/lyrics_question-generation-pipeline-t5-base-modell.json qg qg-p-t5-base`
`ipython manual_evaluation.py  eval_data/lyrics_e2e-pipeline-t5-small-modell.json e2e e2e-p-t5-small`
`ipython manual_evaluation.py  eval_data/lyrics_e2e-pipeline-t5-base-modell.json e2e e2e-p-t5-base`



## Training on manual corrected TweetQA dataset in SQUAD format

1. the python notebook is tweet_qestion_generation_corrected_data.ipynb

# Evaluation

## Automatic evaluation

### nlg-eval

the evaluation is incorporated in every notebook according to the task

### bleurt

the evaluation can be performed using the notebook bleurt_manual.ipynb

## Manual Evaluation
all the relevant scripts and data are to be found in the questionary folder of the repo

## Manual evaluation of the results from the best performing model

T5 base from question generation pipeline

`ipython manual_evaluation.py  eval_data/hypothesis_t5-base-fine-tuned-qg-hl_tweet_manual.txt h qg-t5-base-manual-eval`

## Displaying results for manually evaluated tweets:
`python3 display_results.py tweet_manual_evaluation_hypothesis_base-qg-manual.json tweet`

## Displaying results for manually evaluated lyrics:

`python3 display_results.py lyrics_manual_evaluation_qg-p-t5-base.json lyric`
`python3 display_results.py lyrics_manual_evaluation_qg-p-t5-small.json lyric`
`python3 display_results.py lyrics_manual_evaluation_e2e-p-t5-small.json lyric`
`python3 display_results.py lyrics_manual_evaluation_e2e-p-t5-base.json lyric`
