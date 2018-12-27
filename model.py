import pandas as pd
import nltk
import itertools
import re


def analyze(tweet):

    sentilex = pd.read_csv('sentilex/SentiLex-flex.csv', names=['flex', 'radical', 'pos', 'gn', 'tg', 'pol', 'anot'])
    twitlex = pd.read_csv('twitlex/twitlex.csv')

    # Pre process
    twords = nltk.word_tokenize(tweet)
    # To lower case
    words = list(map(lambda word: word.lower(), twords))

    # 3 Analyze haha, hehehe
    vog = r'[aáãâàéeiíoóõúu]'
    laugh = r'(h'+vog+'+){2}'
    laugh = re.compile(laugh, re.UNICODE)

    # 4 Contabilizar pontos com dicionarios
    tpol = 0
    for word in words:
        tpol += 1 if re.search(laugh, word) else 0
        pol = sentilex.loc[sentilex['flex'] == word]
        if pol.empty:
            # Remove consecutive duplicated chars
            word = ''.join(ch for ch, _ in itertools.groupby(word))
            pol = sentilex.loc[sentilex['flex'] == word]
        if pol.empty:
            pol = twitlex.loc[twitlex['termo'] == word]
        if not pol.empty:
            # Verify negation to invert polarity
            w_not = any([re.fullmatch(r'n([aã]*o+)?', w) for w  in words[max(words.index(word) - 2, 0):words.index(word)]])
            tpol += pol['pol'].values[0] * (-1 if w_not else 1)

    return tpol
