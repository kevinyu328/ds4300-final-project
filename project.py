from py2neo import GraphService
from textblob import TextBlob
import tkinter as tk

# URL of your NEO4j server
NEO4J_SERVER_LINK = 'http://localhost:7474/db/data/'
# username used to login to your NEO4j
NEO4J_USERNAME = 'neo4j'
# password used to login to your NEO4j
NEO4J_PASSWORD = 'neo4jj'
# label used for the word1/word2 field for each node in NEO4j
WORD_LABEL = 'word'
# label used for the positive field in each relationship
RELATIONSHIP_POS_LABEL = 'pos_count'
# label used for the negative field in each relationship
RELATIONSHIP_NEG_LABEL = 'neg_count'

gs = GraphService(NEO4J_SERVER_LINK,
                  user=NEO4J_USERNAME, password=NEO4J_PASSWORD)
graph = gs.default_graph

window = tk.Tk()
window.title('NLP with Neo4J')
window.geometry('900x400')
suggestions = tk.Label(master=window, text='')
sentiment = tk.Label(master=window, text='')


def get_counts_word(word):
    """
    Gets the postive, negative, counts for the given word

    """
    node = graph.run("MATCH (n {word: '" + word + "'})return n")
    node = graph.run("MATCH (n {{{}: '{}'}})return n".format(WORD_LABEL, word))
    for x in node:
        for y in x:
            return (y['pos_count'], y['neg_count'])


def get_sentiment_sentence(line):
    res = TextBlob(line)
    sentiment["text"] = str(res.sentiment.polarity)[:5]
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
sentimentLabel = tk.Label(text="Current sentiment:")
sentimentHelpLabel = tk.Label(wraplength=650, justify="center",
                              text="""*Note: sentiment values are between -1 and 1. Values less than 0 denote a negative sentiment and values greater than or equal to 0 denote a positive sentiment. The closer the value is to -1, the a more negative sentiment is and the closer the value is to 1, the more positive the sentiment. """)
entry = tk.Entry(window, textvariable=v1, width=50)
v1.trace_add("write", parse_input)

label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
suggestions.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
sentimentLabel.place(relx=0.45, rely=0.65, anchor=tk.CENTER)
sentiment.place(relx=0.55, rely=0.65, anchor=tk.CENTER)
sentimentHelpLabel.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

window.mainloop()
