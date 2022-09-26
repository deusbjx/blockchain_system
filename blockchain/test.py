import hashlib as hasher
from time import time
import json
from flask import Flask, jsonify,render_template
from argparse import ArgumentParser
import os, sys

os.chdir(sys.path[0])

author_list = []
subject_list = []
message_list = []
data_list = []

def getMessage(path):
    data = open(path,'rb')
    jsonData = json.load(data)
    for i in range(len(jsonData[2]['data'])) :
        author_list.append(jsonData[2]['data'][i]['author'])
        subject_list.append(jsonData[2]['data'][i]['subject'])
        message_list.append(jsonData[2]['data'][i]['message'])
    length = len(author_list)
    for i in range(length) :
        tinyDict = {'Author':'','Subject':'','Message':''}
        tinyDict['Author'] = author_list[i]
        tinyDict['Subject'] = subject_list[i]
        tinyDict['Message'] = message_list[i]
        data_list.append(tinyDict)
    print(data_list)


getMessage("pre_forum_post.json")
