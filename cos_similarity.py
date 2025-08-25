import json
import os

import gensim
import numpy
import pandas as pd


class driver:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "config.json")
        with open(config_path, encoding='utf-8') as json_data:
            self.config = json.load(json_data)
        self.google = gensim.models.KeyedVectors.load_word2vec_format(
                                        self.config['GOOGLE_NEWS_VECTOR_DATA_FILE_PATH'], 
                                        binary=True,
                                    )

    def get_mean_vector(self,
                        sentence: list[str],
                        normalize: bool):
        """
        Obtains the mean of vector representations of a list of words
        """
        return self.google.get_mean_vector(sentence,
                                        pre_normalize = normalize)

    def get_vector(self, word: str):
        """
        Obtains the vector representations of a list of a word
        """
        return self.google.get_vector(word)

    def conjoin_words(self, word_list: list[str]) -> str:
        """
        Conjoins a list of words into a full string with spaces between consecutive words
        """
        conjoined: str = ""
        for i in range(0, len(word_list)-1):
            conjoined += word_list[i] + " "
        conjoined += word_list[len(word_list)-1]
        return conjoined


    def get_all_sentences(self, path: str, id_col: str):
        """
        Returns a list of all sentences in the csv file
        """
        sentence_list = []
        df: pd.DataFrame = pd.read_csv(path)
        running_list = []
        current_id = 1
        for _, row in df.iterrows():
            print(row[id_col])
            if (row[id_col] != current_id):
                sentence_list.append(self.conjoin_words(running_list))
                # print(conjoin_words(running_list))
                running_list.clear()
                current_id = row[id_col]
            if (row['PartOfSpeech'] != 'PROPN'):
                running_list.append(row['Word'].lower())
            else:
                running_list.append(row['Word'])
        sentence_list.append(self.conjoin_words(running_list))
        return sentence_list


    def current_word_similarity(self, 
                                current_word: str,
                                previous_words: list[str],
                                normalize: bool) -> numpy.float64 | str:
        """
        Returns the cosine similarity of the current word with the mean vector of the
        previous words
        """

        if not previous_words:
            return 'null'
        mean_vector_previous = self.get_mean_vector(previous_words, normalize)
        try:
            vector_current = self.get_vector(current_word)
        except Exception as e:
            print('Word ', f'{current_word}', ' is not an element of the word bank ')
            print('defaulting to null')
            return 'null'

        return numpy.divide(numpy.dot(vector_current, mean_vector_previous),
                        numpy.multiply(numpy.linalg.norm(vector_current),
                        numpy.linalg.norm(mean_vector_previous)))

    def compute_similarities(self,
                             path: str,
                             normalize: bool = False) -> list[numpy.float64]:
        """
        Returns a list of the cosine similarities of the words in the file given by path
        """
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


            result_list.append(self.current_word_similarity(current_word, running_list, normalize))
            if current_word_class != 'Function':
                if current_word_pos != 'PROPN':
                    running_list.append(current_word.lower())
                    continue
                running_list.append(current_word)
        return result_list


    def write_similarity(self):
        """
        Writes the cosine similarity of each word with the list of 
        words preceding it
        """
        os.makedirs("output_files", exist_ok = True)

        for name in self.config['INPUT_FILE_NAMES']:
            real_path = os.path.join("input_files", f"{name}.csv")
            result_unnormalized = self.compute_similarities(real_path)
            result_normalized = self.compute_similarities(real_path, normalize = True)         
            df: pd.DataFrame = pd.read_csv(real_path)

            df['CosineSimilarity'] = result_unnormalized
            df['CosineSimilarity_Normalized'] = result_normalized

            df.to_csv(f'output_files/{name}_processed.csv', index=False)
    

if __name__ == "__main__":
    driver_t = driver()
    driver_t.write_similarity()