import gensim
from numpy import divide, multiply, dot
from numpy.linalg import norm
import pandas as pd


google: gensim.models.KeyedVectors = gensim.models.KeyedVectors.load("goolge.bin", 'r')

def get_mean_vector(sentence: list[str],normalize):
    return google.get_mean_vector(sentence, pre_normalize= normalize)

def get_vector(word: str):
    return google.get_vector(word)

def conjoin_words(word_list: list[str]) -> str:
        conjoined: str = ""
        for i in range(0, len(word_list)-1):
            conjoined += word_list[i] + " "
        conjoined += word_list[len(word_list)-1]
        return conjoined

def get_all_sentences(path: str, id_col: str):
    sentence_list = []
    df: pd.DataFrame = pd.read_csv(path)
    running_list = []
    current_id = 1
    for _, row in df.iterrows():
        print(row[id_col])
        if (row[id_col] != current_id):
            sentence_list.append(conjoin_words(running_list))
            # print(conjoin_words(running_list))
            running_list.clear()
            current_id = row[id_col]
        if (row['PartOfSpeech'] != 'PROPN'):
            running_list.append(row['Word'].lower())
        else:
            running_list.append(row['Word'])
    sentence_list.append(conjoin_words(running_list))
    return sentence_list


def current_word_similarity(current_word: str, previous_words: list[str], normalize: bool):
    if not previous_words:
        return 'null'
    mean_vector_previous = get_mean_vector(previous_words, normalize)

    try:
        vector_current = get_vector(current_word)
    except:
        print('Word ', f'{current_word}', ' is not an element of the word bank ')
        print('defaulting to null')
        return 'null'
    
    return divide(dot(vector_current, mean_vector_previous), multiply(norm(vector_current),norm(mean_vector_previous)))
    

def compute_similarities(path: str, normalize: bool = False):
    result_list = []
    running_list = []
    current_sentence = 1
    df: pd.DataFrame = pd.read_csv(path)
    for _, row in df.iterrows():
        
        sentence = row['Passage']
        if sentence != current_sentence:
            running_list.clear()
            current_sentence = sentence

        current_word = row['WordNoPunctuation']
        current_word_class = row['WordClass']
        current_word_pos = row['PartOfSpeech']


        result_list.append(current_word_similarity(current_word, running_list, normalize))
        if current_word_class != 'Function':
            if current_word_pos != 'PROPN':
                running_list.append(current_word.lower())
                continue
            running_list.append(current_word)
    return result_list


def write_similarity(path: str):
    result_list = []

    result_unnormalized = compute_similarities(path)
    result_normalized = compute_similarities(path, normalize=True)
            
    df: pd.DataFrame = pd.read_csv(path)

    df['CosineSimilarity'] = result_unnormalized
    df['CosineSimilarity_Normalized'] = result_normalized

    df.to_csv(f'{path}_processed.csv', index=False)
    return result_list
    

