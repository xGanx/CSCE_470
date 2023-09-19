# we provide you code here
import json
from nltk.stem import WordNetLemmatizer
from collections import Counter

data = []
with open('content/lyrics_200.jl') as f: # add / in front of content when copying back over
  for line in f:
    data.append(json.loads(line))

songs = []
lyrics = []
count = 0
for i in data:
  songs.append(i['song'])
  lyrics.append(i['lyrics'])
  
#print('DocumentID: ' + songs[1])
#print('Document: ' + lyrics[1])


#print('\nNew Section\n')
# <--------------------------------- Tokenization --------------------------------->
def doc_parser(doc, options):
  # lyrics[0]is a single song
  
  # Cleaning Doc
  while(doc.find('\n') != -1):
    doc = doc.replace('\n',' ')
  
  if 1 in options:
    # Remove background vocals (vocals in parentheses) and song structure indicators (strings in square brakes [])
    bg_vocal_rem = False
    song_struct_rem = False
        
    # Remove brackets
    while (not bg_vocal_rem):
      fir_ind = doc.find('[')
      if (fir_ind == -1):
        bg_vocal_rem = True
      else:
        sec_ind = doc.find(']')
        if sec_ind >= len(doc):
            sec_ind = len(doc)-1
        if sec_ind == -1:
          doc = doc[:fir_ind]
        else:
          doc = doc[:fir_ind] + doc[sec_ind+1:]
        
    # Remove Paranthesis
    while(not song_struct_rem):
      fir_ind = doc.find('(')
      if (fir_ind == -1):
        song_struct_rem = True
      else:
        sec_ind = doc.find(')')
        if sec_ind >= len(doc):
            sec_ind = len(doc)-1
        if sec_ind == -1:
          doc = doc[:fir_ind]
        else:
          doc = doc[:fir_ind] + doc[sec_ind+1:]
  
  # Lowercase all words
  if 2 in options:
    doc = doc.lower()
    
  words = doc.split(' ')
  
  # Lemmatization (use nltk.tokenize.word_tokenize)
  lemmatizer = WordNetLemmatizer()
  for i in range(0, len(words)):
    words[i] = lemmatizer.lemmatize(words[i])
      
  # Cleaning Doc
  while('' in words):
    words.remove('')
  
  current_tokens = words
  return current_tokens

#print(songs[0])
#print(songs[1])



#print first two documents (documentID only)

# report the size of your dictionary, that is, how many unique tokens

# print a list of the top-10 most popular words by count

# TODO before pre-processing
no_proc = dict()
for i in range(0, len(lyrics)):
  parse = doc_parser(lyrics[i], [])
  for word in parse:
    if word in no_proc:
      no_proc[word] += 1
    else:
      no_proc[word] = 1

# print('DocumentID: ' + songs[0])
# print('DocumentID: ' + songs[1])

# print('Dictionary Size = ', len(no_proc))

# word_counter = Counter(no_proc)
# top_10_words = word_counter.most_common(10)
# print('List of Top 10 Most Popular Words by Count = ', top_10_words)

# TODO after lower case folding
lower = dict()
for i in range(0, len(lyrics)):
  parse = doc_parser(lyrics[i], [1])
  for word in parse:
    if word in lower:
      lower[word] += 1
    else:
      lower[word] = 1

# print('DocumentID: ' + songs[0])
# print('DocumentID: ' + songs[1])

# print('Dictionary Size = ', len(lower))

# word_counter = Counter(lower)
# top_10_words = word_counter.most_common(10)
# print('List of Top 10 Most Popular Words by Count = ', top_10_words)

# TODO after lower case folding + lemmatization
lower_and_lem = dict()
for i in range(0, len(lyrics)):
  parse = doc_parser(lyrics[i], [1,2])
  for word in parse:
    if word in lower_and_lem:
      lower_and_lem[word] += 1
    else:
      lower_and_lem[word] = 1

# print('DocumentID: ' + songs[0])
# print('DocumentID: ' + songs[1])

# print('Dictionary Size = ', len(lower_and_lem))

# word_counter = Counter(lower_and_lem)
# top_10_words = word_counter.most_common(10)
# print('List of Top 10 Most Popular Words by Count = ', top_10_words)

print('\n\n\n')

# <--------------------------------- Boolean Retrieval --------------------------------->
def search(inverted_index, terms):
  search_results = []
  
  # if num_terms == 1:
  #   if terms[0] in inverted_index:
  #     search_results = inverted_index[terms[0]]
  # else:
  #   set_1 = inverted_index[terms[0]]
  #   for i in range(1,num_terms):
  #     if terms[i] in inverted_index:
  #       set_2 = inverted_index[terms[i]]
        
  #       shared_set = set(set_1) & set(set_2)
  #       set_1 = list(shared_set)
          
  #   search_results = set_1  
  matching_docs = set()
  if terms[0] in inverted_index:
    matching_docs = set(inverted_index[terms[0]])
  for i in range(1,len(terms)):
    if terms[i] in inverted_index:
      matching_docs.intersection_update(inverted_index[terms[i]])
  search_results = list(matching_docs)
    
  
  return search_results

inverted_index = dict()
for i in range(0, len(lyrics)):
  parse = doc_parser(lyrics[i], [1,2])
  for word in parse:
    if word in inverted_index:
      if songs[i] not in inverted_index[word]:
        inverted_index[word].append(songs[i])
    else:
      inverted_index[word] = [songs[i]]
      
# print(len(inverted_index))
# print(inverted_index['the'])

# print(inverted_index['the'])
# print(len(inverted_index['the']))

# print('\n\n\n')

# search function takes the inverted index and a list of terms
# print(search(inverted_index, ['time'])[0:5])

# print('\n')
# print(search(inverted_index, ['never','know'])[0:5])

# print('\n\n\n')

# <--------------------------------- Ranking Documents --------------------------------->
import math

def sumFreq(song_list):
  total_freq = 0
  for (title, freq) in song_list:
    total_freq += freq
    
  return total_freq


def ranked_search(inverted_index, terms, songs):
  num_terms = len(terms)
  
  unsorted_results = []
  
  if num_terms == 1:
    if terms[0] in inverted_index:
      for (doc, freq) in inverted_index[terms[0]]:
        
        tf = math.log(1+sumFreq(inverted_index[terms[0]]))
        idf = math.log(len(songs) / freq) # Num Docs / Num Doc Freq
      
        total = tf + idf
        
        unsorted_results.append((doc, total)) 
  else:
    for j in range(0, len(terms)):
      term = terms[j]
      
      print(terms[j])
      if term in inverted_index:
        for (doc, freq) in inverted_index[term]:
          
          tf = math.log(1+sumFreq(inverted_index[term]))
          idf = math.log(len(songs) / freq) # Num Docs / Num Doc Freq
        
          total = tf + idf
          
          unsorted_results.append((doc, total)) 
  
  search_results = sorted(unsorted_results, key=lambda x: x[1], reverse=True)
  
  return search_results


inverted_index = dict()

for i in range(0, len(lyrics)):
  title = songs[i]
  
  parse = doc_parser(lyrics[i], [1,2])
  
  for word in parse:
    if word in inverted_index:
      # check if the current title is in the words list
      bool_item_found = False
      for i in range(0,len(inverted_index[word])): # searches through the lists of lists
        if title == inverted_index[word][i][0]:
          inverted_index[word][i][1] += 1
          bool_item_found = True
      if not bool_item_found:
        inverted_index[word].append([title,1])
    else:
      inverted_index[word] = [[title, 1]]
      
for key, value in inverted_index.items():
  sorted_index = sorted(value, key=lambda x: x[1], reverse=True)
  inverted_index[key] = sorted_index

print(ranked_search(inverted_index, ['time'], songs)[0:5])
print(ranked_search(inverted_index, ['never', 'know'], songs)[0:5])

# <--------------------------------- Cool Extension --------------------------------->
