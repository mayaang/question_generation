This github repo is a fork of https://github.com/patil-suraj/question_generation. It was utilized in a student project on the go.

1. In order to be able to reproduce the results the first thing to do it to clone the repository

`git clone https://github.com/mayaang/question_generation.git`
`cd question_generation`

2. Download the urban dictionary from https://www.kaggle.com/therohk/urban-dictionary-words-dataset/datachro

3. `mv urbandict-word-defs.csv tweet-preprocessing`
4. `cd tweet-preprocessing`
Step 5 converts the TweetQA dataset into SQUAD format so it can be used by the pipelines provided by https://github.com/patil-suraj/question_generation
5. `python3 convert_tweetqa_to_squad_format.py urbandict-word-defs.csv train.json dev.json test.json  --debug`
6. `mv tweet_dev_squad_automatic.json ../data/tweet_multitask/`
7. `mv tweet_test_slang_automatic.json ../data/tweet_multitask/`
8. `mv tweet_train_squad_automatic.json ../data/tweet_multitask/`
9. `mv tweet_dev_automatic_reference.txt ../data/tweet_multitask/`
10. open tweet_question_generation Jupyter Notebook and run
