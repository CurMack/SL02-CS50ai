import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    contents = {}
    files = os.listdir(directory)
    for file in files:
        with open(os.path.join(directory, file), encoding= "utf-8") as f:
            content = f.read()
            contents[file] = content
    return contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenized = nltk.tokenize.word_tokenize(document.lower())
    contents = [word for word in tokenized 
                if word not in string.punctuation and 
                word not in nltk.corpus.stopwords.words("english")]
    return contents

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set()
    for filename in documents.keys():
        words.update(documents[filename])
        
    idfs = dict()
    for word in words:
        f = sum(word in documents[filename] for filename in documents.keys())
        idf = math.log(len(documents) / f)
        idfs[word] = idf
    
    return idfs    


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = dict()
    for filename in files.keys():
        tfidf = 0
        for word in query:
            if word not in files[filename]:
                continue
            tfidf += files[filename].count(word) * idfs[word]
        tfidfs[filename] = tfidf
    top_n = sorted(files.keys(), key=lambda f: tfidfs[f], reverse=True)[:n]
    return top_n

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = {}
    for sentence, sentwords in sentences.items():
        score = 0
        for word in query:
            if word in sentwords:
                score += idfs[word]

        if score != 0:
            density = sum([sentwords.count(x) for x in query]) / len(sentwords)
            scores[sentence] = (score, density)

    top_n =[k for k, v in sorted(scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)][:n]
    return top_n


if __name__ == "__main__":
    main()
