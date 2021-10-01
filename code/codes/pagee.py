
from codes.dashboard_app.dashbo import create_dash_app
from flask import Blueprint, app, render_template
import json
from bson import json_util
from builtins import str
from flask import Blueprint, render_template, request
import pymongo
from pymongo import MongoClient
from codes.webb import web_scraping


pagee=Blueprint('pagee', __name__)

@pagee.route('/page2/', methods=['GET', 'POST'])
def Page():
    
    return render_template("page1.html")
    