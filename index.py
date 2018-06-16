
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

import nltk # Interesting, if you run this with python instead of python3, it can't find nltk.
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist
from nltk.corpus import wordnet as wn
from collections import Counter

import re
from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
app = Flask(__name__)

df = pd.read_csv('KingLear.csv', index_col=0, encoding='latin-1')


@app.route("/")
def hello():
    # return str(df.head(20)['name'])
    return render_template('index.html', taco = 'dog') # Note: must import this

print(df.head())

@app.route('/linesByScene')
def linesPerScene():
    scenes = [line[:3] for line in df["LineNos"]]
    unique_scenes = set(scenes)
    df['scene'] = pd.Series(scenes, index=df.index)
    # print(df.tail())
    gb = df.groupby(['scene', 'Speakers']).count() # Multiple groupby is such a great feature
    # print(gb)
    #
    # for g in gb:
    #     print(g)
    return gb.to_json(orient="split")

# linesPerScene()


@app.route('/totalLines')
def total():
    total = df.groupby("Speakers").count()
    print(total)
    return total.to_json(orient="split")

# total()

@app.route('/scenes')
def scenes():
    # char = request.args.get('char')
    char = 'CORDELIA'
    scenes = [line[:3] for line in df["LineNos"]]
    df['scene'] = pd.Series(scenes, index=df.index)

    # Kind of annoying I'm having to split these up -- I'm sure I don't have to...:
    inScene = df[df['Speakers'] == char].groupby('scene')['scene']
    inSceneCounts = df[df['Speakers'] == char].groupby('scene')['scene'].count()
    for s in inScene:
        print(s)

# scenes()

# Grabs all the text spoken by one speaker in an nltk.Text object:
# It's unfortunate we get stuck with all these apostrophes...but whatever:
@app.route('/speakerText')
def speakerText():
    char = 'CORDELIA'
    speech = df[df['Speakers'] == char]
    raw = ''
    for l in speech['Lines']:
        raw += l + '\n'

    toks = word_tokenize(raw)
    text = nltk.Text(toks)

    print(text)
    return(str(toks))















# Playing with NLTK:
def freqPlay(text):
    fdist = FreqDist(text)
    # print(fdist.most_common(250))

    commons = fdist.most_common(250)
    res = ''

    for c in commons:
        res = res + ' ' + c[0]

    toks = word_tokenize(res)

    tags = nltk.pos_tag(toks)

    # Gets most common nouns used in the play:
    # print(tags)
    print([t for t in tags if t[1] == 'NN'])


    # print(fdist['strange'])

    # print(fdist.hapaxes())

def onePlay(play):
    raw_text = ''
    for line in df['Lines']:
        raw_text += line + '\n'

    tokens = word_tokenize(raw_text)
    text = nltk.Text(tokens)
    print(text.concordance('beast'))
    print('\n')

    print(text.similar('love'))

    text.collocations()

    richness = len(set(text)) / len(text)
    print(richness)

    print(text.count('happy'))

    freqPlay(text)



onePlay('KingLear')







    # sim = wn.synsets('blood')[0].path_similarity(wn.synsets('dog')[0]) # This is how they implement the path similarity idea I had.
    # print(sim)
    # Can also do wn.path_similarity(w1, w2)


    # text.collocations()
    # text.dispersion_plot(['blood'])
    #
    # richness = len(set(text)) / len(text)
    # print(richness)
    #
    # print(text.count('strange'))
    #

    # freqPlay(text)
    # tagPlay(tokens)





def tagPlay(tokens):
    tagged_text = nltk.pos_tag(tokens)
    print(tagged_text[:50])
    counts = Counter(tag for word,tag in tagged_text)
    print(counts)

    # Thanks SO:
    total = sum(counts.values())
    normals = dict((word, float(count)/total) for word,count in counts.items())
    print(normals)






if __name__ == "__main__":
    app.run()




# Ay
