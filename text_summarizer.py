import spacy
from heapq import nlargest
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

def summarizer(rawdocs): 
    stopwords = list(STOP_WORDS)
    # print(stopwords)
    
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    
    tokens = [token.text for token in doc]
    # print(tokens)

    # It picks up each word from doc, converts it into lower case and checks if it is in stopwords or punctuations.     
    word_freq = {}
    # Each word will be added into the dictionary and assigned a value.
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            # If not, convert word into text and check if word is in word_freq's dictionary. 
            # If not, then assign that word 1, and if repeated again, then increase its value.
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
     # Handle case when no valid words are found
    if not word_freq:
        return "Input text is too short or does not contain meaningful content.", doc, len(rawdocs.split(' ')), 0
    
    # print(word_freq)
    max_freq = max(word_freq.values())
    # print(max_freq)

    # Normalized frequency = frequency of each word / max frequency.
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq
    # print(word_freq)

    # Sentence tokenize  
    sent_tokens = [sent for sent in doc.sents]
    # print(sent_tokens)

    # Make dictionary for sentence in a similar manner
    sent_score = {}
    for sent in sent_tokens:  # Picking each sentence from tokens.
        for word in sent:     # Picking each word from the tokenized sentence.
            if word.text in word_freq.keys():  # Check if the word exists in word_freq dictionary.
                if sent not in sent_score.keys():  # If the sentence doesn't exist in sent_score, add it.
                    sent_score[sent] = word_freq[word.text]  # Assign value.
                else:
                    sent_score[sent] += word_freq[word.text]  # Add the normalized frequency.

    # It calculates the total frequency of each sentence.
    # print(sent_score)  # Total frequency of each sentence.

    select_len = int(len(sent_tokens) * 0.3)  # 30% length of sent tokens.
    # print(select_len)

    # Select sentences with the highest frequency from sent_score.
    summary = nlargest(select_len, sent_score, key=sent_score.get)
    final_summary = [word.text for word in summary]  # Make a list using word.text and join by space.
    summary = ' '.join(final_summary)
    
    # print("Original Text is: ")
    # print(rawdocs)
    # print("_________________________________________________________________________________________________")
    # print("Summarized Text is:")
    # print(summary)
    # print("_________________________________________________________________________________________________")

    # print("Length Of Original Text:", len(rawdocs.split(' ')))
    # print("Length Of Summarized Text:", len(summary.split(' ')))

    return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))
    
