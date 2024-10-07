
DIR = 'data/'

SENTENCES = 'sentences.txt'

def save_sentence(sentence):
    with open(DIR+SENTENCES, 'a') as f:
        f.write(sentence+'\n')

def load_sentences():
    with open(DIR+SENTENCES, 'r') as f:
        sentences = f.readlines()
    return sentences