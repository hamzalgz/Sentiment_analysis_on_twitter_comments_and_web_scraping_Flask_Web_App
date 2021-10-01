import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import warnings
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import os
os.environ['PYTHONPATH'] += "./models"
import sys
sys.path.append("./models")
warnings.simplefilter("ignore")
import official.nlp.bert.tokenization as tokenization
from official import nlp
from official.nlp import bert
from flask import Flask
from flask import Blueprint, render_template, request
import pymongo
from pymongo import MongoClient
from codes.webb import web_scraping

cluster= MongoClient('mongodb+srv://hamza:2748@cluster0.htzn9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db=cluster['twitter']
collec=db['all']

home=Blueprint('home', __name__)

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


@home.route('/', methods=['GET','POST'])
def Home():
    if request.method == "POST":

        data=request.form.get('keys')
        a=web_scraping(data)
        for i in range (len(a)):
            post={"user":a[i][0],"date":a[i][1],'like_cntre':a[i][2],'retweet_cnt': a[i][3],'quote_cnt':a[i][4],'txt':a[i][5]}
            collec.insert_one(post)
        our_list=[]
        for x in collec.find():
            our_list.append(x)    
        df=pd.DataFrame(our_list)

        new_model=tf.keras.models.load_model (r'.\codes\static\twitter_bert')

        tokenizerSaved = bert.tokenization.FullTokenizer(
            vocab_file=os.path.join(r'.\codes\static\twitter_bert', r'assets\vocab.txt'),
            do_lower_case=False)

        
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
        
        replies_cnt=len(df)
        a=[replies_cnt,49,19,396]

        df.to_csv('ourda')

        
        return render_template("page1.html")
    return render_template('Home.html')







