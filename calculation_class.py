import gensim
import numpy
import csv
from collections import deque
import spacy


#TODO Auto detection of positions and indexes

"""

   This class calculates the cosine similarity between words and the words previous to them.
   A word is included in calculation depending on its part of speech, and whether it is a function or a content words.


"""
class Calculations:
    
    nlp = spacy.load("en_core_web_trf")
    special_cases = {"cannot": [{"ORTH": "cannot"}]}
    nlp.tokenizer.add_special_case("cannot", special_cases["cannot"])

    word_set: set = set()
    google: gensim.models.KeyedVectors = gensim.models.KeyedVectors.load("pre_trained_data/goolge.bin", 'r')
    similarities: deque[str] = deque()
    part_of_speech: deque[str] = deque()
    pos_deque: deque = deque()
    line_num: int = 0
    # glove: gensim.models.KeyedVectors = gensim.models.KeyedVectors.load("pre_trained_data/glove.bin", 'r')

    # Takes in a deque of words and conjoins them
    def conjoin_words(self, word_queue: deque[str]) -> str:

        conjoined: str = ""
        while (word_queue):
            conjoined += word_queue.popleft() + " "
        print(conjoined)
        return conjoined
    
    def write_pos(self, read_path: str, write_path: str, pos_idx:int, collumn_name : list[str]):
        with open(write_path, 'w', newline='') as results:
            with open(read_path, mode ='r') as reference:
                csv_reader = csv.reader(reference)
                csv_writer = csv.writer(results)

                csv_writer.writerow(collumn_name)

                next(csv_reader)
                for line in csv_reader:
                    print(line)
                    #We only change the similarity value and not other parts of the original file thus the below
                    line[pos_idx] = self.pos_deque.popleft()
                    csv_writer.writerow(line)
        
    # Takes in a file, and records the part of speech of each word
    def get_pos(self, read_path: str,  word_position: str, sentence_idx: int):
        # debug = open('debug.txt', 'w')
        with open(read_path, mode ='r') as reference:
            csv_reader = csv.reader(reference)
            next(csv_reader)

            sentence_deque: deque = deque()
            current_sentence = str(1)
            print("-->" + str(sentence_idx))
            for line in csv_reader:
                target: str = line[word_position]
                if (current_sentence != line[sentence_idx]):
                    entire_sentence: str = self.conjoin_words(sentence_deque)
                    tokenized_sentence = self.nlp(entire_sentence)
                    for token in tokenized_sentence:

                        # debug.write('\n')
                        if (token.pos_ != "PUNCT"): self.pos_deque.append(token.pos_)
                        # debug.write(str(token))
                        # debug.write('\n')
                        # debug.write(token.pos_)
                        # debug.write('\n')
                    sentence_deque.clear()
                    current_sentence = line[sentence_idx] 
                sentence_deque.append(target)   
            
            #whatever is left at the end is also tokenized
            entire_sentence: str = self.conjoin_words(sentence_deque)
            tokenized_sentence = self.nlp(entire_sentence)
            for token in tokenized_sentence:
                self.pos_deque.append(token.pos_)
                print(token)
                print(token.pos_)
            sentence_deque.clear()
            current_sentence = line[sentence_idx] 
            
            # We add all words in a sentence in a dequeue
            # When we reach the end we conjoin the words and tokenize it
            # add the part of speech of each token to a dequeue

    # Takes in a file, and writes the similarity of a word with similarity calculated in compute similarities written to the output file. Everything else remains the same.
    def write_similarity(self, read_path: str, write_path: str, similarity_idx: int, collumn_name : list[str]):
        with open(write_path, 'w', newline='') as results:
            with open(read_path, mode ='r') as reference:
                csv_reader = csv.reader(reference)
                csv_writer = csv.writer(results)

                csv_writer.writerow(collumn_name)
                next(csv_reader)
                for line in csv_reader:
                    #We only change the similarity value and not other parts of the original file thus the below
                    line[similarity_idx] = self.similarities.popleft()
                    csv_writer.writerow(line)

    # Takes in a file and computes the similarity of a word with its preceding word and stores the in a queue. Nothing is written without calling write_similarity.
    def compute_similarities(self, sentence_idx: int, word_idx: int, word_class_idx: int, pos_idx: int, file_path: str):
        # debug = open("debug.txt", 'w')
        with open(file_path, mode ='r') as corpus: 
            corpus = csv.reader(corpus)

            next(corpus)

            self.line_num = corpus.line_num

            word_queue: deque = deque()

            current_sentence = str(2)
        
            for line in corpus:
                if (current_sentence != line[sentence_idx]):
                    word_queue.clear()
                    current_sentence = line[sentence_idx]
                
                if (line[pos_idx] == 'PROPN'):
                    target: str = line[word_idx].strip('.,')
                    print(target)
                else:
                    target: str = line[word_idx].lower().strip('.,')
                
                
                if (word_queue and self.google.__contains__(target)):
                    target_vector = self.google.get_vector(target)
                    dot_product_sum: numpy.float64 = 0.0
                    sum_vector: numpy.ndarray = numpy.zeros(300)
                    for previous_word in word_queue:
                        previous_word_vector = self.google.get_vector(previous_word)
                        try:
                            dot_product_sum += numpy.dot(previous_word_vector, target_vector)
                            sum_vector += previous_word_vector
                        except: 
                            print("error --> " + previous_word + " is not a key ")
                    numerator: numpy.float64 = dot_product_sum
                    denominator: numpy.float64 = numpy.linalg.norm(sum_vector) * numpy.linalg.norm(target_vector)
                    if (denominator == 0):
                        result = 'null'
                    else:
                        result = numerator/denominator
                    
                    self.similarities.append(str(result))
                    
                else: 
                    self.similarities.append('null')

                if (line[word_class_idx] == 'Content' and self.google.__contains__(target)):
                    word_queue.append(target)

    