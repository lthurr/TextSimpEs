import utils
import os.path

def pre_process():
    assert not os.path.isfile('Language_Model/ngram_count_corpus_ordered.txt'), "The corpus is really preprocessed."
    with open('Language_Model/ngram_count_corpus_ordered.txt', 'w') as output:
        with open('Language_Model/ngram_count_corpus.txt', 'r') as f:
            for line in sorted(f):
                line = line.lower()
                line = utils.separate_punt_marks(line)
                line = utils.tag_numbers(line)
                output.write(line)

if __name__ == '__main__':
    pre_process()
