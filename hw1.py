# we provide you code here
import json

data = []
with open('/content/lyrics_200.jl') as f:
  for line in f:
    data.append(json.loads(line))

songs = []
lyrics = []
count = 0
for i in data:
  songs.append(i['song'])
  lyrics.append(i['lyrics'])
  
print('DocumentID: ' + songs[1])
print('Document: ' + lyrics[1])