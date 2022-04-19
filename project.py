from py2neo import GraphService
from textblob import TextBlob
import tkinter as tk

NEO4J_SERVER_LINK = 'http://localhost:7474/db/data/'
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = 'neo4jj'
WORD_LABEL = 'word'
RELATIONSHIP_POS_LABEL = 'pos_count'
RELATIONSHIP_NEG_LABEL = 'neg_count'

gs = GraphService(NEO4J_SERVER_LINK,
                  user=NEO4J_USERNAME, password=NEO4J_PASSWORD)
graph = gs.default_graph

window = tk.Tk()
suggestions = tk.Label(master=window, text='')


def get_counts_word(word):
    """
    Gets the postive, negative, counts for the given word

    """
    node = graph.run("MATCH (n {word: '" + word + "'})return n")
    node = graph.run("MATCH (n {{{}: '{}'}})return n".format(WORD_LABEL, word))
    for x in node:
        for y in x:
            return (y['pos_count'], y['neg_count'])


# def get_sentiment_sentence(sentence):
#     """
#     Calculates Sentiment of Sentence by averaging for each word: Positive / Total , then the average for
#     all words in sentence is the sentiment.

#     """
#     average_sentiment_words = []
#     for x in sentence.split():
#         word_tup = get_counts_word(x.lower())
#         if word_tup is None:
#             print(x + ' is not in the graph')
#         else:
#             word_positive = float(
#                 word_tup[0]) / (float(word_tup[0]) + float(word_tup[1]))
#             print(word_positive)
#             average_sentiment_words.append(word_positive)
#     return sum(average_sentiment_words) / len(average_sentiment_words)


def get_sentiment_sentence(line):
    res = TextBlob(line)
    if res.sentiment.polarity >= 0:
        return "Positive"
    else:
        return "Negative"


def get_next_words(last_word, is_positive):
    """
    Given the last word and whether the sentence is positive, predicts the next word.

    """
    predictions = []
    display_text = ''

    if is_positive == 1:
        most_positive = 0
        most_positive_word = ''

        node = graph.run(
            "MATCH (n {{{}:'{}'}}) - [r] -> (x) return x order by r.{} desc limit 3".format(WORD_LABEL, last_word, RELATIONSHIP_POS_LABEL))
        for x in node:
            for y in x:
                predictions.append(y['word'])
    else:
        node = graph.run(
            "MATCH (n {{{}:'{}'}}) - [r] -> (x) return x order by r.{} desc limit 3".format(WORD_LABEL, last_word, RELATIONSHIP_NEG_LABEL))
        for x in node:
            for y in x:
                predictions.append(y['word'])
    for p in predictions:
        display_text += p + ', '
    suggestions["text"] = display_text[:-
                                       2] if display_text else 'No suggestions available'

    return predictions


def parse_input(*args):
    input = v1.get()
    words = input.split()

    if get_sentiment_sentence(input) == 'Positive' and len(words) > 0:
        get_next_words(words[-1], 1)
    elif len(words) > 0:
        get_next_words(words[-1], 0)


v1 = tk.StringVar()
label = tk.Label(text="Enter your sentence here:")
entry = tk.Entry(window, textvariable=v1)
v1.trace_add("write", parse_input)

label.pack()
entry.pack()
suggestions.pack()

window.mainloop()
