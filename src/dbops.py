#!/bin/env python3
import sqlite3
from sqlite3 import Error
import os
import datetime
import uuid
import secrets


def makeTokens(mysize):
  return secrets.token_urlsafe(mysize)  

try:
  DB_FILE=os.environ["DB_FILE"]
except:
  DB_FILE="/usr/portal/appdatabase/database.db"
SESSION_IDLE=10

def getTimeFromNow():
  current_time = datetime.datetime.now()  # use datetime.datetime.utcnow() for UTC time
  expiry = current_time + datetime.timedelta(minutes=SESSION_IDLE)
  return int(expiry.timestamp())

def showDB():
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  sql="SELECT * FROM sessions"
  vars=()
  c.execute(sql,vars)
  return c.fetchall()

def deleteDBSession(session_id):
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  sql="DELETE FROM sessions WHERE sessionid = ?"
  vars=(session_id,)
  c.execute(sql,vars)
  return True

def checkDBSession(session_id):
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  sql="SELECT expires,jobs FROM sessions where sessionid = ?"
  vars=(session_id,)
  c.execute(sql,vars)
  relevantsessions=c.fetchone()
#  print(f"relevant sessions: {relevantsessions}")
  if relevantsessions == None:
    print("No session found")
    return False
  expiry=int(relevantsessions[0])
  jobs=relevantsessions[1]
  if int(expiry)<int(datetime.datetime.now().timestamp()):
    print(f"User session for session_id has expired")
    deleteDBSession(session_id)
    return False
  if expiry>=int(datetime.datetime.now().timestamp()):
    renewDBSession(session_id)
  return jobs

def retrieveDBData(session_id,toget):
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  sql=f"SELECT {toget} FROM sessions where sessionid = ?"
  vars=(session_id,)
  c.execute(sql,vars)
  relevantsessions=c.fetchone()
  #print(f"Returning relevantsessions: {relevantsessions[0]}")
  if relevantsessions==None:
    return None
  return relevantsessions[0]

def dbDumpAll():
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  sql=f"SELECT * FROM sessions"
  vars=()
  c.execute(sql,vars)
  relevantsessions=c.fetchall()
  #print(f"Returning relevantsessions: {relevantsessions[0]}")
  return relevantsessions


def createUserDBSession(username,jobs,endpoints,extlinks):
  expiry=getTimeFromNow()
  session_id=makeTokens(32)
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  sql="INSERT INTO sessions (sessionid,username,jobs,expires,endpoints,extlinks) VALUES(?,?,?,?,?,?)"
  vars=(session_id,username,jobs,expiry,endpoints,extlinks)
  c.execute(sql,vars)
  conn.commit()
  return (session_id,expiry)

def renewDBSession(session_id):
  expiry=getTimeFromNow()
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  sql="UPDATE sessions SET expires = ? WHERE sessionid=?"
  vars=(expiry, session_id)
  c.execute(sql,vars)
  conn.commit()
  print(f"{session_id} renewed!")
  return expiry


def setupDB():
  print("setting up db...")
  conn = sqlite3.connect(DB_FILE) 
  c = conn.cursor()

  c.execute('''
          CREATE TABLE IF NOT EXISTS sessions
          ([sessionid] TEXT PRIMARY KEY, [username] TEXT, [jobs] TEXT, [expires] TEXT, [endpoints] TEXT, [extlinks] TEXT)
          ''')
  conn.commit()

if __name__ == '__main__':
    setupDB()

