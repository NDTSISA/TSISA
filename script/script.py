import collections
import re
import sys
import glob
import os
import codecs
import json
import artm
import numpy as np
from LSA import make_lsa_from_text
from TextTiling import make_tt_from_text


filepath = sys.argv[1]

textArray = []
with open(filepath) as f:
    for line in f:
        textArray.append(line)

bagsofwords = [ collections.Counter(re.findall(r'\w+', txt))
            for txt in textArray]

words = []
for txt in textArray:
     words.append(re.findall(r'\w+', txt))

uniq_words = list(set([el for lst in words for el in lst]))

ind = 1
word_dict = {}
for el in uniq_words:
    word_dict[el] = ind
    ind += 1


num_of_docs = 0
num_of_uniq_words = len(uniq_words)
num_of_words = 0
lines = []
for id_ in range(len(bagsofwords)):
    num_of_docs += 1
    for el in bagsofwords[id_].keys():
        lines.append("{} {} {}".format(str(id_+1),word_dict[el],bagsofwords[id_][el]))
        num_of_words += bagsofwords[id_][el]

with open('docword.tmp.txt', 'w') as f:
    f.write(str(num_of_docs)+ "\n")
    f.write(str(num_of_uniq_words)+"\n")
    f.write(str(num_of_words)+"\n")
    for line in lines:
        f.write(line + "\n")

with open('vocab.tmp.txt', 'w') as f:
    for item in uniq_words:
        f.write("{}\n".format(item))


filename = 'tmp'
batch_vectorizer = None
if len(glob.glob(os.path.join(filename, '*.batch'))) < 1:
    batch_vectorizer = artm.BatchVectorizer(data_path='', data_format='bow_uci', collection_name=filename, target_folder=filename)
else:
    batch_vectorizer = artm.BatchVectorizer(data_path=filename, data_format='batches')


dictionary = artm.Dictionary()

model_artm = artm.ARTM(topic_names=['topic_{}'.format(i) for i in xrange(15)],
                       scores=[artm.PerplexityScore(name='PerplexityScore',
                                                    dictionary=dictionary)],
                       regularizers=[artm.SmoothSparseThetaRegularizer(name='SparseTheta', tau=-0.15)],
                       cache_theta=True)


if not os.path.isfile(filename+'/dictionary.dict'):
    dictionary.gather(data_path=batch_vectorizer.data_path)
    dictionary.save(dictionary_path=filename+'/dictionary.dict')

dictionary.load(dictionary_path=(filename+'/dictionary.dict'))
dictionary.load(dictionary_path=(filename+'/dictionary.dict'))

model_artm.initialize(dictionary=dictionary)

model_artm.scores.add(artm.SparsityPhiScore(name='SparsityPhiScore'))
model_artm.scores.add(artm.SparsityThetaScore(name='SparsityThetaScore'))
model_artm.scores.add(artm.TopicKernelScore(name='TopicKernelScore', probability_mass_threshold=0.3))

model_artm.regularizers.add(artm.SmoothSparsePhiRegularizer(name='SparsePhi', tau=-0.1))
model_artm.regularizers.add(artm.DecorrelatorPhiRegularizer(name='DecorrelatorPhi', tau=1.5e+5))
model_artm.regularizers.add(artm.TopicSelectionThetaRegularizer(name='TopicSelection',tau=0.25))

model_artm.regularizers['SparsePhi'].tau = -0.5
model_artm.regularizers['SparseTheta'].tau = -0.5
model_artm.regularizers['DecorrelatorPhi'].tau = 1e+5

model_artm.scores.add(artm.TopTokensScore(name='TopTokensScore', num_tokens=10))

model_artm.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes=40)

ex = model_artm.get_theta()
for i,el in enumerate(ex.sum(axis=1)):
    if el == 0:
        ex = ex.drop('topic_'+str(i),axis=0)

resultARTM = []
for i in ex:
    resultARTM.append(np.argmax(ex[i]))

resultLSA = make_lsa_from_text(textArray)
resultTT = make_tt_from_text(textArray)

with open("../client/components/Lines/constants.json") as f:
    obj = json.loads(f.read())

obj['constants']['1'] = resultLSA
obj['constants']['2'] = resultTT
obj['constants']['3'] = resultARTM

with open('../client/components/Lines/constants.json', 'w') as f:
    json.dump(obj,f)


