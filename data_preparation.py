from nltk.tokenize import word_tokenize
import random
from tqdm import tqdm
from utils import chunks
from config import BASE_PATH

with open(BASE_PATH + '/chat_sentences.txt', 'r') as in_file:
    sentences = in_file.readlines()
    in_file.close()
    
sentences = [sent.strip() for sent in sentences]
bigrammed_sentences = []

with open(BASE_PATH + 'final_dataset/chat_sentences_phrased.txt', 'r') as in_file:
    phrased_sentences = in_file.readlines()
    in_file.close()

phrased_sentences = [sent.strip() for sent in phrased_sentences]

vocab = dict()
for sent in tqdm(phrased_sentences):
    for word in word_tokenize(sent):
        if word in vocab.keys():
            vocab[word]+=1
        else:
            vocab[word] = 1

with open(BASE_PATH + 'final_dataset/vocabulary.txt', 'a+') as file:
    for w in sorted(vocab.keys(), reverse=True, key=vocab.get):
        file.write(str(w)+'\n')


random.shuffle(phrased_sentences)

training_sentences = phrased_sentences[:200]
heldout_sentences = phrased_sentences[200:]

heldout_files = list(chunks(heldout_sentences, 9))
training_files = list(chunks(training_sentences, 20))


for index, value in tqdm(enumerate(training_files)):
    with open(BASE_PATH + f'/final_dataset/training/{index}.txt', 'w+') as file:
        for sent in value:
            file.write(str(sent)+'\n')
        file.close()
        
for index, value in tqdm(enumerate(heldout_files)):
    with open(BASE_PATH + f'/final_dataset/heldout/{index}.txt', 'w+') as file:
        for sent in value:
            file.write(str(sent)+'\n')
        file.close()





sentence_stream = [sent.split(' ') for sent in sentences]


from gensim.models import Phrases

bigrammer = Phrases(sentence_stream, threshold=105, min_count=1)

bigrammed_sent = [bigrammer[sent] for sent in sentence_stream]

for i in range(len(sentence_stream)):
    if sentence_stream[i] != bigrammed_sent[i]:
        print(sentence_stream[i])
        print(bigrammed_sent[i])


training_sentences = []
for index in tqdm(range(10)):
    with open(BASE_PATH + f'/final_dataset/training/{index}.txt', 'r') as file:
        training_sentences+=[sent.strip() for sent in file.readlines()]
        file.close()
        
count = 0
for sent in training_sentences:        
    for word in word_tokenize(sent):
        count+=1
    
