import numpy as np

x = np.array([1,5,0,1,3,1,2,1,4])
v = np.array([[0.00,0.23,-0.99,0.01],[0.50,0.00,0.12,-0.78],[-1.00,0.56,0.25,0.89],[0.75,-0.95,0.11,0.30],[0.20,0.40,-0.85,0.65],[1.00,-0.11,0.05,0.00],[-0.99,0.77,0.33,0.01],[0.02,0.88,-0.76,0.45],[0.58,-0.64,0.20,0.90]])

vX = np.matmul(x,v)

# print(vX)

b1 = np.array([-0.75,-0.95,0.10,0.30])
b2 = np.array([0.90,3.81,1.72,0.23,3.54,0.75,0.30,2.02,3.53])

gx = vX + b1

# print(gx)

denom = -1 * gx

sigmoid = 1.00/(1.0 + np.exp(denom))

# print(sigmoid)

w = np.array([[0.00, 0.11, 0.22, -0.33, 0.44, -0.55, 0.66, -0.77, 0.88],[-0.99,0.88,0.77,0.66,-0.55,0.44,0.33,-0.22,0.11],[0.90,0.81,-0.72,0.63,-0.54,0.45,0.36,-0.27,0.18],[0.09,-0.98,0.87,0.76,-0.65,0.54,-0.43,-0.32,-0.21]])

prod = np.matmul(sigmoid, w)

# print(prod)

prod += b2

print(f'Answer 1.1: {prod}')

# Answer for problem 1.1
fx = prod


# COde for problem 1.2

print('\nPROBLEM 1.2\n')

v = np.array([[0.12, -0.34, 0.56, -0.78],[-0.91, 0.23, 0.45, -0.67],[-0.89, 0.10, -0.32, 0.54],[0.76, -0.98, 0.21, -0.43],[0.65, -0.87, 0.09, 0.30],[-0.29, 0.48, 0.66, -0.84],[-0.13, 0.57, -0.91, 0.20]])

w = np.array([[0.33, -0.44, -0.55, 0.66, -0.77, 0.88, 0.99],[0.11, 0.22, -0.33, 0.44, -0.55, 0.66, -0.77],[0.88, 0.99, -0.10, 0.21, -0.32, -0.43, 0.54],[0.65, -0.76, 0.87, -0.98, 0.09, -0.20, 0.31]])

b1 = [0.45, 0.35, 0.80, 0.20]

b2 = [3.10, 1.31, 4.22, 3.46, 3.29, -0.53, 1.93]

x = [4,0,5,0,3,0,3]

vX = np.matmul(x,v)

gx = vX + b1

denom = -1 * gx

sigmoid = 1.00/(1.0 + np.exp(denom))

prod = np.matmul(sigmoid, w)

prod += b2

print(f'Answer 1.2: {prod}')

# Answer for problem 1.1
fx = prod


# problem 2.1

# https://medium.com/mti-technology/n-gram-language-model-b7c2fc322799
# https://www.analyticsvidhya.com/blog/2022/01/building-language-models-in-nlp/

import nltk
# nltk.download()
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from collections import Counter

text = 'If a student attends every class, he or she will automatically get an A.'
vocab = 'If a student attends every class, he or she will automatically get an A. Cav'.split()
token=nltk.word_tokenize(text)
unigrams = ngrams(token,1)
bigrams = ngrams(token,2)

print(Counter(unigrams))

unigram = {'If': 1, 'a': 1, 'student': 1, 'attends': 1, 'every': 1, 'class': 1, ',': 1, 'he': 1, 'or': 1, 'she': 1, 'will': 1, 'automatically': 1, 'get': 1, 'an': 1, 'A.': 1, 'Cav': 1, '.': 1}
unigram['Cav'] = 0
total_words = len(vocab)

for key in unigram.keys():
    unigram[key] = 1.0/total_words
    
print(unigram)

sentence = 'Every student will get an A.'


words_in_sentence = sentence.split()

sentence_prob = 1

for word in words_in_sentence:
    if word in unigram:
        sentence_prob *= unigram[word]
        
print(f'Probabilty = {sentence_prob}')

for key in unigram.keys():
    unigram[key] = (1 + unigram[key]) / (total_words + unigram[key])
    
sentence = 'Cav says every student will get an A.'

words_in_sentence = sentence.split()  
    
words_in_sentence = sentence.split()

sentence_prob = 1

for word in words_in_sentence:
    if word in unigram:
        sentence_prob *= unigram[word]
        
print(f'Probabilty = {sentence_prob}')
    
    
total_probability = 1
    
for key in unigram.keys():
    total_probability *= unigram[word]

# Calculate perplexity
num_words = total_words
perplexity = pow(total_probability, -1/num_words)

print("Perplexity:", perplexity)

# bigram part

# print(Counter(bigrams))

bigram = {('If', 'a'): 1, ('a', 'student'): 1, ('student', 'attends'): 1, ('attends', 'every'): 1, ('every', 'class'): 1, ('class', ','): 1, (',', 'he'): 1, ('he', 'or'): 1, ('or', 'she'): 1, ('she', 'will'): 1, ('will', 'automatically'): 1, ('automatically', 'get'): 1, ('get', 'an'): 1, ('an', 'A'): 1, ('A', '.'): 1}
print(bigram)

# set probabiltiies
for key in bigram.keys():
    bigram[key] = (bigram[key] + 1) / (bigram[key] + len(vocab))

bigram_sent = 'Cav says every student will get an A.'.split()

pairs = []

for i in range(len(bigram_sent)-1):
    pairs.append((bigram_sent[i], bigram_sent[i+1]))
    
print(pairs)

bigram_prob = 1
for pair in pairs:
    if pair in bigram:
        bigram_prob *= bigram[pair]
    else:
        bigram_prob *= (1.0/len(vocab))
        
print(f'Probabilty Bigram: {bigram_prob}')

total_prob = 1
for key in bigram.keys():
    total_prob *= unigram[word]

# Calculate perplexity
num_words = total_words
perplexity = pow(total_prob, -1/num_words)

print("Perplexity:", perplexity)