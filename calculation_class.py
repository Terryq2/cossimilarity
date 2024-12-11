import gensim
import numpy
import csv
from collections import deque
import spacy


#TODO Ideas of a constructor, do get pos and compute similarity upon initialization 
#TODO Auto detection of positions and indexes
class Calculations:

    nlp = spacy.load("en_core_web_trf")

    word_set: set = set()
    google: gensim.models.KeyedVectors = gensim.models.KeyedVectors.load("pre_trained_data/goolge.bin", 'r')
    similarities: deque[str] = deque()
    part_of_speech: deque[str] = deque()
    line_num: int = 0
    # glove: gensim.models.KeyedVectors = gensim.models.KeyedVectors.load("pre_trained_data/glove.bin", 'r')

    # Takes in a deque of words and conjoins them
    def conjoin_words(word_queue: deque[str]) -> str:
        conjoined: str
        conjoined += word_queue.popleft()
        return conjoined
        
    # Takes in a file, and records the part of speech of each word
    def get_pos(self, read_path: str,  word_position: str, pos_idx: int, sentence_idx: int, collumn_name : list[str]):
        with open(read_path, mode ='r') as reference:
            csv_reader = csv.reader(reference)
            
            word_queue: deque = deque()
            current_sentence = str(1)
            next(csv_reader)
            # We add all words in a sentence in a dequeue
            # When we reach the end we conjoin the words and tokenize it
            # add the part of speech of eachb token to a dequeue

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

    # Takes in a file and computes the similarity of a word with its preceding word and stores in a queue. Nothing is written without calling write_similarity.
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
                    target: str = line[word_idx].lower().strip('.,')
                    word_queue.clear()
                    current_sentence = line[sentence_idx]
                
                if (line[pos_idx] == 'PNOUN'):
                    target: str = line[word_idx].strip('.,')
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

    