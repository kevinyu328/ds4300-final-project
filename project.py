import pandas as pd
from msvcrt import getch
from textblob import TextBlob

bigram = pd.read_csv('bigram_small.csv')

# sentence = ""
# finished = False

# while finished != True:
#     key = ord(getch())
#     realkey = chr(key)

#     if key != 0:
#         # press enter, program stop
#         if key == 13:
#             finished = True
#             break
#         # press backspace
#         elif key == 8:
#             sentence = sentence[:-1]
#         # press space
#         elif key == 32:
#             print("Sentence: " + sentence)


sentence = input()
words = sentence.split()

last_word = words[-1]


def sentence_sentiment(line):
    res = TextBlob(line)
    if res.sentiment.polarity >= 0:
        return "Positive"
    else:
        return "Negative"


res_sentiment = sentence_sentiment(sentence)

res_df = bigram[bigram["word1"] == last_word].sort_values(
    by=['Total'], axis=0, ascending=False)

recommend_3 = []

for index, row in res_df.iterrows():
    if row['Positive'] >= row['Negative'] and res_sentiment == 'Positive' or row['Negative'] > row['Positive'] and res_sentiment == 'Negative':
        recommend_3.append(row['word2'])
        if len(recommend_3) == 3:
            print(recommend_3)
            break
