import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import os
os.environ['PYTHONPATH'] += "./models"
import sys
sys.path.append("./models")
import numpy as np
import numpy as np
import official.nlp.bert.tokenization as tokenization
from official import nlp
from official.nlp import bert
import warnings
warnings.simplefilter("ignore")
from flask import Flask
import pymongo
from pymongo import MongoClient


cluster= MongoClient('mongodb+srv://hamza:2748@cluster0.htzn9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db=cluster['twitter']
collec=db['tweets']
our_list=[]
for x in collec.find():
    our_list.append(x)    
df=pd.DataFrame(our_list)


new_model=tf.keras.models.load_model (r'.\codes\static\twitter_bert')


tokenizerSaved = bert.tokenization.FullTokenizer(
    vocab_file=os.path.join(r'.\codes\static\twitter_bert', r'assets\vocab.txt'),
    do_lower_case=False)


def encode_names(n, tokenizer):
   tokens = list(tokenizer.tokenize(n))
   tokens.append('[SEP]')
   return tokenizer.convert_tokens_to_ids(tokens)


def bert_encode(string_list, tokenizer, max_seq_length):
    num_examples = len(string_list)
    
    string_tokens = tf.ragged.constant([
        encode_names(n, tokenizer) for n in np.array(string_list)])

    cls = [tokenizer.convert_tokens_to_ids(['[CLS]'])]*string_tokens.shape[0]
    input_word_ids = tf.concat([cls, string_tokens], axis=-1)

    input_mask = tf.ones_like(input_word_ids).to_tensor(shape=(None, max_seq_length))

    type_cls = tf.zeros_like(cls)
    type_tokens = tf.ones_like(string_tokens)
    input_type_ids = tf.concat(
        [type_cls, type_tokens], axis=-1).to_tensor(shape=(None, max_seq_length))

    inputs = {
        'input_word_ids': input_word_ids.to_tensor(shape=(None, max_seq_length)),
        'input_mask': input_mask,
        'input_type_ids': input_type_ids}

    return inputs


l=[]
for x in range(len(df.txt.values)):
    inputs = bert_encode(string_list=list(df.txt.values[x]), 
                        tokenizer=tokenizerSaved, 
                        max_seq_length=240)
    m=4
    prediction= new_model.predict(inputs)
    if np.argmax(prediction)>0.5:
        pass
    else:
        m=0
    print(df.txt.values[x],' is: ', m)
    l.append(m)
df['target']=l
print(df.head(9))