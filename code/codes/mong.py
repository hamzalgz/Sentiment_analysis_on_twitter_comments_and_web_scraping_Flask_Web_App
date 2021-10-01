from flask import Flask
import pymongo
from pymongo import MongoClient

cluster= MongoClient('mongodb+srv://hamzalgz:27480@cluster0.htzn9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db=cluster['twitter']
collec=db['tweets']

post={'_id':0, 'name':'hamza', 'age':21}

collec.insert_one(post)
