# The highest level code that brings everything together.

import extractor
import filter
import scoring
from sys import argv
import numpy as np
import additional_filter
from nltk.stem import PorterStemmer, WordNetLemmatizer
 
stemmer = PorterStemmer()
lemmatiser = WordNetLemmatizer()

def print_usage():
    # Display the parameters and what they mean.
    print('''
    Usage:
        main.py <article.txt> <summary length>

    Explanation:
        Parameter 1: the location and name of the text to summarize
        Parameter 2: the number of sentences for the summary to contain
    ''')

def topic_sent(sentence,topics):
    topic_sentences=[]
    rem=[]
    for x in topics:
        short=[]
        for y in x:
            for s in sentence:
                if lemmatiser.lemmatize(y) in lemmatiser.lemmatize(s):
                        short.append(s)
                else:
                        rem.append(s)
        topic_sentences.append(short)
    topic_sentences.append(rem)
    return topic_sentences


def summarize(filename,topics,input_words,num_of_sentences):
    # Summarize a file. The length of the summary will be the number of sentences specified.
    file = filename

    # Extract all the words and sentences and get their respective scores.
    all_words = extractor.get_words(file)
    word_scores = scoring.get_word_scores(all_words)
    all_sentences = extractor.get_sentences(file)
    all_sentences = filter.omit_transition_sentences(all_sentences)
            
    all_sentences=topic_sent(all_sentences,topics)
    i=0
    complete_summary=[]

    for all_sentences_part in all_sentences:
            num_of_sentences_new=num_of_sentences
            sentence_scores_part = scoring.get_sentence_scores_list(all_sentences_part, word_scores)
            all_sentences_part,sentence_scores_part=additional_filter.remove_duplicates(all_sentences_part,sentence_scores_part)

            if num_of_sentences_new > len(all_sentences_part):
                #print("The summary cannot be longer than the text.")
                num_of_sentences_new=len(all_sentences_part)
                
    # Get x sentences with the highest scores, in chronological order.
   
            threshold = scoring.x_highest_score(sentence_scores_part, num_of_sentences_new)
            top_sentences = scoring.top_sentences(all_sentences_part, sentence_scores_part, threshold)
   
    # Put the top sentences into one string.
            top_sentences = top_sentences[-num_of_sentences_new:]
            
            summary = input_words[i]+ ": \n"
            i=i+1
            for sentence in top_sentences:
                summary += sentence + " "
            complete_summary.append(summary+'\n')
            
    return complete_summary


if __name__ == '__main__':
    if len(argv) != 3:
        print_usage()
    elif not str(argv[2]).isdigit():
        print_usage()
    else:
        summarize(argv[1], int(argv[2]))
