#!/bin/env python3
from dbops import *
from accessops import *
def checkUserSession(sessionid):
  sessionvalid=checkDBSession(sessionid)
  username=retrieveDBData(sessionid,"username")
  if sessionid==None or sessionvalid==False:
    return "invalid_session"
  if username==None:
    return "username_not_found_in_db"
  return "ok"

def checkUserJobPerms(sessionid,username,jobname):
  userjobs=getUserJobsByGroup(sessionid)
  print(f'{sessionid} by {username} is trying to run {jobname}...')
  if jobname not in userjobs:
    print(f'{username} is not allowed to run {jobname}.')
    return False
  print(f'{username} is allowed to run {jobname}.')
  return True

