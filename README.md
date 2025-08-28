# Word Cosine Semantic Similarity Analysis

This program computes the **cosine similarity** of each word in a text with the **mean vector of the words that precede it**. The goal is to analyze the predictability or “surprise” of a word in a sentence, which can provide insight into its relationship with the **N400 event-related potential** in neuroscience.

The program is optimized for efficiency using **Pandas** to process input CSV files containing tokenized sentences.

---

## Features

* Computes the mean vector of preceding words for each target word.
* Calculates cosine similarity between the current word vector and the preceding words’ mean vector.
* Supports **normalization** of word vectors for more accurate similarity measures.
* Processes multiple CSV input files and outputs results to a dedicated folder.
* Handles proper nouns and function words differently to better model linguistic relevance.

---

## Requirements

* Python 3.12 (recommended for compatibility with prebuilt SciPy and Gensim wheels)
* [Gensim](https://radimrehurek.com/gensim/)
* Pandas
* NumPy

Install dependencies via:

```bash
pip install numpy pandas gensim
```

---

## Google News Pretrained Vectors

This program uses the **pretrained Google News Word2Vec vectors**:

* [Download link](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?pli=1&resourcekey=0-wjGZdNAUop6WykTtMip30g)
* File: `GoogleNews-vectors-negative300.bin`
* Format: Word2Vec binary

Place the file path in your `config.json` under `GOOGLE_NEWS_VECTOR_DATA_FILE_PATH`.

---

## Usage

1. **Create a configuration file (`config.json`)** with input files:

```json
{
    "GOOGLE_NEWS_VECTOR_DATA_FILE_PATH": "GoogleNews-vectors-negative300.bin",
    "INPUT_FILE_NAMES": ["l1_in", "l2_in"]
}
```

2. **Prepare input CSV files** in `input_files/` folder. Each CSV should include:

   * `Word`, `WordNoPunctuation`, `PartOfSpeech`, `WordClass`, `Passage`, and an ID column for sentence grouping.

3. **Run the program:**

```bash
python cos_similarity.py
```

4. **Output:**
   Results are saved in `output_files/` with two new columns:

* `CosineSimilarity` (unnormalized)
* `CosineSimilarity_Normalized` (normalized)

---

## Notes

* Words not found in the pretrained model default to `'null'`.
* Proper nouns (`PROPN`) are treated differently to preserve capitalization relevance.




