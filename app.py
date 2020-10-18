import math
import string
from flask import Flask
from flask import request

app = Flask(__name__)


common_contractions = {
    "we'll": ['we', 'will'],
    "don't": ['do', 'not']
    # ...clearly a lot more will need to be added.
}


@app.route('/')
def hello():
    '''The base handler exists to confirm that the server is running.'''

    return "welcome to flask"


@app.route('/score', methods=['POST'])
def score():
    '''Computes a similarity score for the two POSTed strings (doc_a, doc_b)

    The handler iterates over a set of algorithms that provide a
    weighted assessment of similarity between 0 and 1. It returns the
    average of the results.
    '''

    doc_a = request.form['doc_a']
    doc_b = request.form['doc_b']
    word_list_a = make_normalized_word_list(doc_a)
    word_list_b = make_normalized_word_list(doc_b)
    frequency_table_a = make_frequency_table(word_list_a)
    frequency_table_b = make_frequency_table(word_list_b)

    # A list of scoring functions and their needed arguments.
    scoring_functions = [
        [scaled_vector_angle, frequency_table_a, frequency_table_b],
        [jaccard, word_list_a, word_list_b],
        [silly_score, word_list_a, word_list_b]
    ]

    score_sum = 0.0
    for func in scoring_functions:
        score = func[0](*func[1:])
        score_sum += score

    avg_score = round(score_sum/len(scoring_functions), 2)
    return {"score": f'{avg_score}'}


def make_normalized_word_list(text):
    '''For the given text, convert it to lowercase, remove punctuation,
    and split on whitespace.
    '''
    normalized_word_list = []
    text = text.translate({ord(i): None for i in string.punctuation})
    text = text.lower()
    for word in text.split():
        contractions = common_contractions.get(word)
        if contractions is not None:
            for contraction_piece in contractions:
                normalized_word_list.append(contraction_piece)
        else:
            normalized_word_list.append(word)
    return normalized_word_list


def make_frequency_table(word_list):
    '''Makes a dictionary mapping words to their frequncy in the given list'''

    frequency_table = {}
    for word in word_list:
        if frequency_table.get(word) is None:
            frequency_table[word] = 1
        else:
            frequency_table[word] += 1
    return frequency_table


def silly_score(word_list_a, word_list_b):
    '''A very naive scoring algorithm

    Compare the two lists of words first forwards, then backwards.
    count the matches and divide by the avg length of the given lists.
    '''

    match = 0
    avg_len = (len(word_list_a)+len(word_list_b))/2
    if avg_len == 0:
        return 0
    word_list_a_reversed = word_list_a.copy()
    word_list_b_reversed = word_list_b.copy()
    word_list_a_reversed.reverse()
    word_list_b_reversed.reverse()
    word_lists = [
        [word_list_a, word_list_b],
        [word_list_a_reversed, word_list_b_reversed]]
    for word_list in word_lists:
        zipped_list = zip(word_list[0], word_list[1])
        for pair in zipped_list:
            if pair[0] == pair[1]:
                match += 1
    result = match/avg_len
    if result > 1:
        result = 1

    return result


def jaccard(word_list_a, word_list_b):
    '''Calculates a similarity score using the jaccard algorithm
    https://towardsdatascience.com/the-best-document-similarity-algorithm-in-2020-a-beginners-guide-a01b9ef8cf05'''

    union = set(word_list_a + word_list_b)
    intersection = set(word_list_a).intersection(set(word_list_b))
    return len(intersection)/len(union)


def dot_product(d1, d2):
    '''Computes a matrix multiplication of the two dictionaries'''

    the_sum = 0.0
    for key in d1:
        if key in d2:
            the_sum += (d1[key] * d2[key])
    return the_sum


def scaled_vector_angle(d1, d2):
    '''Calculates a similarity score between 0 and 1 by measuring the
    angle between two vectors created from the word frequency dictionaries.
    See https://www.geeksforgeeks.org/measuring-the-document-similarity-in-python/?ref=lbp'''

    numerator = dot_product(d1, d2)
    denominator = math.sqrt(dot_product(d1, d1)*dot_product(d2, d2))
    pi_over_2 = math.pi/2
    return 1 - math.acos(numerator/denominator)/pi_over_2


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
