# we provide you code here
import json
from nltk.stem import WordNetLemmatizer

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

doc = lyrics[65]
#print(doc)

bg_vocal_rem = False
song_struct_rem = False
    
# Remove brackets
while (not bg_vocal_rem):
    fir_ind = doc.find('[')
    if (fir_ind == -1):
        bg_vocal_rem = True
    else:
        sec_ind = doc.find(']')
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
#print(doc)

#print(words)

print(doc)

while(doc.find('\n') != -1):
    doc = doc.replace('\n',' ')
#print(doc)

words = doc.split(' ')
lemmatizer = WordNetLemmatizer()
for i in range(0, len(words)):
    words[i] = lemmatizer.lemmatize(words[i])

# Cleaning Doc
while('' in words):
    words.remove('')

print(words)