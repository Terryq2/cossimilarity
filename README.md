# About


Specialized program to compute the cosine similarity of a vectorized word with the sum of the vector of the words preceding it. 

For example, the following sentence
```
Very few issues can bring together lawmakers of both parties
```
when inputted in the following format 
```
Passage,WordNo,NewID,Sentence,WP,WordNoPunctuation,Word,WordClass,SimilarityWithPrevious,PartOfSpeech
1,1,1Aw01,1,1,Very,Very,Content,,ADV
1,2,1Aw02,1,2,few,few,Content,,ADJ
1,3,1Aw03,1,3,issues,issues,Content,,NOUN
1,4,1Aw04,1,4,can,can,Function,,AUX
1,5,1Aw05,1,5,bring,bring,Content,,VERB
1,6,1Aw06,1,6,together,together,Content,,ADV
1,7,1Aw07,1,7,lawmakers,lawmakers,Content,,NOUN
1,8,1Aw08,1,8,of,of,Function,,ADP
1,9,1Aw09,1,9,both,both,Function,,DET
1,10,1Aw10,1,10,parties,parties.,Content,,NOUN
```
and calling
```python
position_of_word: int = 6
position_of_word_class: int = 7
position_of_part_of_speech: int = 9
position_of_similarity: int = 8

column_names : list[str] = ["Passage","WordNo","NewID","Sentence","WP","WordNoPunctuation","Word","WordClass","SimilarityWithPrevious", "PartOfSpeech"]
program.compute_similarities(position_of_sentence_id,
    position_of_word,
    position_of_word_class,
    position_of_part_of_speech,
    'l2_in.csv')
program.write_similarity('l2_in.csv','l2_out.csv',position_of_similarity, column_names_l2)
```


outputs
```
Passage,WordNo,NewID,Sentence,WP,WordNoPunctuation,Word,WordClass,SimilarityWithPrevious,PartOfSpeech
1,1,1Aw01,1,1,Very,Very,Content,null,ADV
1,2,1Aw02,1,2,few,few,Content,0.18984218873220016,ADJ
1,3,1Aw03,1,3,issues,issues,Content,0.14730018791399555,NOUN
1,4,1Aw04,1,4,can,can,Function,0.27303981047049225,AUX
1,5,1Aw05,1,5,bring,bring,Content,0.19822961978623127,VERB
1,6,1Aw06,1,6,together,together,Content,0.30000838998493606,ADV
1,7,1Aw07,1,7,lawmakers,lawmakers,Content,0.16010041370735328,NOUN
1,8,1Aw08,1,8,of,of,Function,null,ADP
1,9,1Aw09,1,9,both,both,Function,0.437474755237959,DET
1,10,1Aw10,1,10,parties,parties.,Content,0.33400488099464337,NOUN
```
where the SimilarityWithPrevious column gives the cosine similarity of the vector of the word in question with the words preceding it.
## Usage
### Google Word2Vec
A pre-trained word embedding model by goolge was used. 
```
https://code.google.com/archive/p/word2vec/
```
It is necessary to download this model in the above site and indicate the position of the model file in the line below.
```python
google: gensim.models.KeyedVectors = gensim.models.KeyedVectors.load("pre_trained_data/goolge.bin", 'r')
```

### Part of speech filling
Example input:
```
Passage,WordNo,NewID,Sentence,WP,WordNoPunctuation,Word,WordClass,SimilarityWithPrevious,PartOfSpeech
1,1,1Aw01,1,1,Very,Very,Content,,
1,2,1Aw02,1,2,few,few,Content,,
1,3,1Aw03,1,3,issues,issues,Content,,
1,4,1Aw04,1,4,can,can,Function,,
1,5,1Aw05,1,5,bring,bring,Content,,
1,6,1Aw06,1,6,together,together,Content,,
1,7,1Aw07,1,7,lawmakers,lawmakers,Content,,
1,8,1Aw08,1,8,of,of,Function,,
1,9,1Aw09,1,9,both,both,Function,,
1,10,1Aw10,1,10,parties,parties.,Content,,
```
Function calls:
```python
position_of_word: int = 5
position_of_sentence_idx: int = 3
position_of_pos: int = 9

program = calculation_class.Calculations()
column_names : list[str]= ["Passage","WordNo","NewID","Sentence","WP","WordNoPunctuation","Word","WordClass","SimilarityWithPrevious", "PartOfSpeech"]
program.get_pos('corpus.csv',position_of_word, position_of_sentence_idx)
program.write_pos('corpus.csv', 'processed.csv',position_of_pos, column_names)
```
Example output:
```
Passage,WordNo,NewID,Sentence,WP,WordNoPunctuation,Word,WordClass,SimilarityWithPrevious,PartOfSpeech
1,1,1Aw01,1,1,Very,Very,Content,,ADV
1,2,1Aw02,1,2,few,few,Content,,ADJ
1,3,1Aw03,1,3,issues,issues,Content,,NOUN
1,4,1Aw04,1,4,can,can,Function,,AUX
1,5,1Aw05,1,5,bring,bring,Content,,VERB
1,6,1Aw06,1,6,together,together,Content,,ADV
1,7,1Aw07,1,7,lawmakers,lawmakers,Content,,NOUN
1,8,1Aw08,1,8,of,of,Function,,ADP
1,9,1Aw09,1,9,both,both,Function,,DET
1,10,1Aw10,1,10,parties,parties.,Content,,NOUN
```


## TODO & Problems
### Problems
Probably a bad design choice to allow any format of data provided that the user manually enter the index of the columns. In theory,
this allows more degrees of freedom, but in pratice this was very bothersome.
### TODO 
Implement a constructor which takes in the input file and automatically detects the various positions of the column, effectively removing the need 
for users to manually check and pass the positions of the columns into the functions as they need to do now.
  -It is then possibly necessary to restrict the input column names to allow only specific ones. Now it does not matter what the names of the columns are, only their positions.



