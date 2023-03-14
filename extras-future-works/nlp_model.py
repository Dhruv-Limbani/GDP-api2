import pickle
from sentence_transformers import SentenceTransformer, util
import re
import pandas as pd
import numpy as np
from symptoms import syms
import streamlit as st
import fastapi


model = SentenceTransformer('STModel')

#desc = "It's very hard to breathe and I am always feeling hungry. I am also having a little pain in chest. I am also having cough, mild fever"
desc = input("How are feeling?\n")
desc = desc.lower().replace("and",",").replace(".",",")
sentences1 = re.split(",", desc)
sentences2 = ['I am having ' + sym for sym in syms]
# encode list of sentences to get their embeddings
embedding1 = model.encode(sentences1, convert_to_tensor=True)
embedding2 = model.encode(sentences2, convert_to_tensor=True)
# compute similarity scores of two embeddings
cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)

# for i in range(len(sentences1)):
#   print("Sentence 1:", sentences1[i])
#   print("Sentence 2:", sentences2[np.argmax(cosine_scores[i])])
#   print("Similarity Score:", cosine_scores[i][np.argmax(cosine_scores[i])].item())

identified_syms = [sentences2[np.argmax(cosine_scores[i])].replace("I am having ",'') for i in range(len(sentences1))]
print("The identified symptoms are: \n")

for i in identified_syms:
    print(i)