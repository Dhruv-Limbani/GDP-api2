from fastapi import FastAPI, Query
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pickle
import pandas as pd
import json
# from sentence_transformers import SentenceTransformer, util
# import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

with open('model','rb') as f:
    model,diseases,sym_attrs = pickle.load(f)
df = pd.read_csv('Prototype.csv')

with open('model2','rb') as f:
    model2,diseases,sym_attrs = pickle.load(f)
df = pd.read_csv('Prototype.csv')

with open('model3','rb') as f:
    model3,diseases,sym_attrs = pickle.load(f)
df = pd.read_csv('Prototype.csv')

# stmodel = SentenceTransformer('stsb-roberta-large')

@app.get('/predict')
def predict(symptoms: list = Query(...)):
    sym_indices = [np.where(sym_attrs==sym)[0][0] for sym in symptoms]
    x = np.zeros(len(sym_attrs))
    for idx in sym_indices:
        x[idx]=1
    pred1 = model.predict([x])[0]
    pred2 = model2.predict([x])[0]
    pred3 = model3.predict([x])[0]
    pred_l = np.unique([pred1,pred2,pred3])
    preds = []
    for i in pred_l:
        preds.append(diseases[i])
    return preds

@app.get('/get_lksyms')
def get_likely_symptoms(symptoms: list = Query(...)):
    syms = []
    for sym in symptoms:
        sl = {}
        for s in df.columns[:-1]:
            if (s in symptoms):
                continue
            try:
                sl[s] = pd.crosstab(df[sym],df[s])[1][1]
            except:
                print(sym,s)
        sl = sorted(sl.items(),key = lambda x:x[1], reverse=True)
        y = [x[0] for x in sl if x[1]>0] #if x[1]>0.1*df[df[sym]==1].shape[0] 
        syms.append(y)
    #syms = sorted(syms.items(),key = lambda x:x[1], reverse=True)
    #print(syms)
    #count = int(np.mean([df[df[x]==1].shape[0] for x in sym_list]))
    l = syms[0]
    l2=[]
    for s in l:
        flag=1
        for lst in syms[1:]:
            if s in lst:
                flag=1
            else:
                flag=0
                break
        if flag:
            l2.append(s)
    js_l2 = json.dumps(l2)
    return l2

# @app.get('/identify_from_desc')
# def identify_syms(desc: str):
#     desc = desc.lower().replace("and",",").replace(".",",")
#     sentences1 = re.split(",", desc)
#     sentences2 = ['I am having ' + sym for sym in sym_attrs]
#     # encode list of sentences to get their embeddings
#     embedding1 = stmodel.encode(sentences1, convert_to_tensor=True)
#     embedding2 = stmodel.encode(sentences2, convert_to_tensor=True)
#     # compute similarity scores of two embeddings
#     cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)

#     # for i in range(len(sentences1)):
#     #   print("Sentence 1:", sentences1[i])
#     #   print("Sentence 2:", sentences2[np.argmax(cosine_scores[i])])
#     #   print("Similarity Score:", cosine_scores[i][np.argmax(cosine_scores[i])].item())

#     identified_syms = [sentences2[np.argmax(cosine_scores[i])].replace("I am having ",'') for i in range(len(sentences1))]
#     print(identified_syms)
#     sym_indices = [np.where(sym_attrs==sym)[0][0] for sym in identified_syms]
#     x = np.zeros(len(sym_attrs))
#     for idx in sym_indices:
#         x[idx]=1
#     pred1 = model.predict([x])[0]
#     pred2 = model2.predict([x])[0]
#     pred3 = model3.predict([x])[0]
#     pred_l = np.unique([pred1,pred2,pred3])
#     preds = []
#     for i in pred_l:
#         preds.append(diseases[i])
#     return preds

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)