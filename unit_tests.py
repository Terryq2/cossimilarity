# def isNoEntry(entry: str):
#     return entry == '' or entry == 'NA' or entry == 'WordNotInVocabulary' or entry.isspace()
  
# class comparison_check(unittest.TestCase):
#     google: gensim.models.KeyedVectors = gensim.models.KeyedVectors.load("pre_trained_data/goolge.bin", 'r')

#     line_num_reference: int = 0
#     line_num_candidate: int = 0

#     list_reference: list[list[str]] = [[]]
#     list_candidate: list[list[str]] = [[]]


#     def setUp(self):
#         # Open the reference file, set up line num, set up list of its lines
#         with open('corpus.csv', 'r') as reference:

#             reader_reference = csv.reader(reference)

#             for line in reader_reference:

#                 self.list_reference.append(line)

#             self.line_num_reference = reader_reference.line_num

#         # Open the candidate file, set up line num, set up list of its lines
#         with open('result_L2.csv', 'r') as candidate:

#             reader_candidate = csv.reader(candidate)

#             for line in reader_candidate:

#                 self.list_candidate.append(line)

#             self.line_num_candidate = reader_candidate.line_num
    

# def test_line_number(self):
#     self.assertEqual(self.line_num_reference,self.line_num_candidate)

# def test_type_check(self):
#     for i in range(2, self.line_num_reference):
        
#         if(not isNoEntry(self.list_reference[i][13])):
#             self.assertTrue(self.list_candidate[i][13] != 'null')

    
#     @parameterized.expand([
#         (5, 3, 7, 8)
#     ])
#     def test_correctness(self, word_idx : int, sentence_idx: int, class_idx: int, similarity_idx : int):
#         #to_lower == true if we want to check correctness for all lower case similarity calculations
#         to_lower: bool = True
#         word_queue: deque = deque()
#         current_sentence = str(2)
#         for i in range(1, self.line_num_candidate):
#             if (current_sentence != self.list_candidate[i][sentence_idx]):
#                 word_queue.clear()
#                 current_sentence = self.list_candidate[i][sentence_idx]

            
#             if (to_lower):
#                 target: str = self.list_candidate[i][word_idx].lower()
#             else:
#                 target: str = self.list_candidate[i][word_idx]
            
            
#             if (word_queue and self.list_candidate[i][similarity_idx] != 'null'):
#                 sum_vector: numpy.ndarray = numpy.zeros(300, dtype=numpy.float64)
#                 for word in word_queue:
#                     try:
#                         sum_vector += self.google.get_vector(word)
#                     except: 
#                         pass

#                 numerator: numpy.float64 = numpy.dot(sum_vector, self.google.get_vector(target))
#                 denominator: numpy.float64 = numpy.linalg.norm(sum_vector) * numpy.linalg.norm(self.google.get_vector(target))
#                 result: numpy.float64 = numerator/denominator

#                 self.assertAlmostEqual(result, numpy.float64(self.list_candidate[i][similarity_idx]),6)
                    
#             if (self.list_candidate[i][class_idx] == 'Content'):
#                 word_queue.append(target)

    

# def test_precision(self):
#     num_correct_to_six_decimal_place: int = 0 
#     num_correct_to_one_decimal_place: int = 0
#     num_error_to_six_decimal_place: int = 0
    
#     cumulative_erros: float = 0.0
#     num_of_total_erros: int = 0
#     no_entry_error: int = 0
    


#     for i in range(2, self.line_num_reference):

#         if(isNoEntry(self.list_reference[i][13])):
#             try:
#                 self.assertTrue(self.list_candidate[i][13] == 'null')
#                 continue
#             except: 
#                 no_entry_error += 1
#                 continue
            
        
#         try: 
#             self.assertAlmostEqual(float(self.list_reference[i][13]),float(self.list_candidate[i][13]),1)
#             num_correct_to_one_decimal_place += 1
#         except:
#             difference = numpy.abs(float(self.list_reference[i][13])-float(self.list_candidate[i][13]))

#             cumulative_erros += difference
#             num_of_total_erros += 1

#         try:
#             self.assertAlmostEqual(float(self.list_reference[i][13]),float(self.list_candidate[i][13]),6)
#             num_correct_to_six_decimal_place +=1
            
            
#         except:
#             print(i)
#             difference = numpy.abs(float(self.list_reference[i][13])-float(self.list_candidate[i][13]))
#             cumulative_erros += difference

#             num_of_total_erros += 1
#             num_error_to_six_decimal_place += 1

    
#     message = [
#     f"Average error introduced --> {cumulative_erros / num_of_total_erros}",
#     f"Cumulative error introduced --> {cumulative_erros}",
#     f"There are --> {num_correct_to_one_decimal_place} <-- entries of similarity that are the same when rounded to the first decimal place",
#     f'There are --> {num_correct_to_six_decimal_place} <-- entries of similarity which are the same when rounded to the sixth decimal place',
#     f'There are --> {num_error_to_six_decimal_place} <-- entries of similarity which are NOT the same when rounded to the sixth decimal place',
#     f'There are --> {no_entry_error} <-- entries of similarity which are NOT computed when they SHOULD be computed'
#     ]
#     print_box_with_message(150,10,message)