#!/usr/bin/python
# -*- coding:utf-8 -*-
#from crypt import methods
import hashlib as hasher
from time import time
import json
from tkinter.tix import Tree
from urllib import response
from flask import Flask, jsonify,render_template,request
from argparse import ArgumentParser
import os, sys
import random
import string

os.chdir(sys.path[0])
blockchain = []

author_list = []
subject_list = []
message_list = []
data_list = []

sql_attack_list = ['\'','\"',"select",'union','and','or','=','update','extract','floor']
xss_attack_list = ['xss','<','>','script','alert']

#哈希函数随机盐值
def getSalt():
    chars = string.ascii_letters + string.punctuation
    return ''.join(random.choice(chars) for x in range(6))

#获取论坛信息
def getMessage(path):
    data = open(path,'rb')
    jsonData = json.load(data)
    for i in range(len(jsonData)) :
        author_list.append(jsonData[i]['author'])
        subject_list.append(jsonData[i]['subject'])
        message_list.append(jsonData[i]['message'])
    length = len(author_list)
    for i in range(length) :
        tinyDict = {'Author':'','Subject':'','Message':''}
        tinyDict['Author'] = author_list[i]
        tinyDict['Subject'] = subject_list[i]
        tinyDict['Message'] = message_list[i]
        data_list.append(tinyDict)
    #print(data_list)

def hash(index,data,timestamp,previous_hash):
    sha = hasher.sha256()
    salt = getSalt()
    sha.update("{0}{1}{2}{3}{4}".format(index,data,timestamp,previous_hash,salt).encode("utf8"))
    return sha.hexdigest()

def make_a_block(index,timestamp,data,previous_hash):
    block={}
    block["index"]=index
    block["timestamp"]=timestamp
    block["data"]=data
    block["previous_hash"]=previous_hash
    block["hash"]=hash(index,data,timestamp,previous_hash)
    return block

def add_a_block(data):

    last_block = blockchain[len(blockchain)-1]

    index=last_block["index"]+1
    timestamp=int(round(time() * 1000))
    previous_hash=last_block["hash"]


    blockchain.append(make_a_block(index,timestamp,data,previous_hash))


def make_a_genesis_block():
    index=0
    timestamp=int(round(time() * 1000))
    data="Head Block"
    previous_hash=0

    blockchain.append(make_a_block(index,timestamp,data,previous_hash))

def isHacker(content) :
    ans = False
    for i in sql_attack_list :
        if (content.find(i) >= 0) :
            ans = True
            break
    for i in xss_attack_list :
        if (i in content) :
            ans = True
            break
    return ans

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#@app.route('/say/<string:msg>',methods=['GET'])
def add_block(msg):
    add_a_block(msg)
    return jsonify(blockchain)

@app.route('/uploadData',methods=['GET','POST'])
def uploadData():
    global blockchain
    global author_list
    global subject_list
    global message_list
    global data_list
    blockchain = []
    author_list = []
    subject_list = []
    message_list = []
    data_list = []
    data = request.values.get('json_data')
    make_a_genesis_block()
    jsonData = json.loads(data)
    #print(jsonData)
    for i in range(len(jsonData)) :
        author_list.append(jsonData[i]['author'])
        subject_list.append(jsonData[i]['subject'])
        message_list.append(jsonData[i]['message'])
    length = len(author_list)
    for i in range(length) :
        tinyDict = {'Author':'','Subject':'','Message':''}
        tinyDict['Author'] = author_list[i]
        tinyDict['Subject'] = subject_list[i]
        tinyDict['Message'] = message_list[i]
        data_list.append(tinyDict)
    for i in range(len(data_list)) :
        add_str = data_list[i]
        add_a_block(add_str)
    response = {}
    for i in range(len(blockchain)) :
        st = "Block"+str(i)
        response[st] = blockchain[i]
    return jsonify(response)

@app.route('/showData/',methods=['GET'])
def showData():
    data = open("pre_forum_post.json",'r',encoding="UTF-8")
    jsonData = json.load(data)
    #jsonData = json.dumps(jsonData).encode('utf-8').decode('unicode_escape')
    return jsonify(jsonData)

@app.route('/login',methods=['GET','POST'])
def login() : 
    username = request.values.get('username')
    password = request.values.get('password')
    #print(str(username)+str(password))
    ans = isHacker(str(username)) | isHacker(str(password))
    if (ans == True) :
        res = {
            'isLogin': '0',
            'msg': 'hacker'
        }
        return jsonify(res)
    if username == 'admin' and password == '123456':
        res = {
            'isLogin': '1',
            'msg': 'success'
        }
        return jsonify(res)
    else:
        res = {
            'isLogin': '-1',
            'msg': 'fail'
        }
        return jsonify(res)

@app.route('/getData')
def getData():
    global blockchain
    global author_list
    global subject_list
    global message_list
    global data_list
    blockchain = []
    author_list = []
    subject_list = []
    message_list = []
    data_list = []
    response = {}
    make_a_genesis_block() #初始化创世区块
    getMessage("pre_forum_post.json")
    for i in range(len(data_list)) :
        add_str = data_list[i]
        add_a_block(add_str)
    for i in range(len(blockchain)) :
        st = "Block"+str(i)
        response[st] = blockchain[i]
    return jsonify(response)

if __name__ == '__main__':
    # make_a_genesis_block() #初始化创世区块
    
    # getMessage("pre_forum_post.json")

    # for i in range(len(data_list)) :
    #     add_str = data_list[i]
    #     add_a_block(add_str)

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    app.config['JSON_AS_ASCII'] = False
    port = args.port
    app.run(debug=True,host='0.0.0.0',port=port)
