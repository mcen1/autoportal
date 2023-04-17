
from flask import Flask,request,render_template,jsonify,redirect, url_for,abort,make_response
import json
from runapi import *
from app import app
from accessops import *
from sharedfunctions import *
try:
  LOCALDEV=os.environ["LOCALDEV"]
except:
  LOCALDEV="no"
try:
  URLPREFACE=os.environ["URLPREFACE"]
except:
  URLPREFACE=""
cookiesecurity=True
if LOCALDEV=="yes":
  cookiesecurity=False



@app.route('/dynamic-job')
def render_dynamic_job():
  sessionid=request.cookies.get('sessionid')
  sessioncheckresults=checkUserSession(sessionid)
  if sessioncheckresults!="ok":
    return render_template('login.html',URLPREFACE=URLPREFACE, redirecturl=f"{URLPREFACE}/dynamic-job",userinfo="Please log in with your ABC Active Directory account to continue to dynamic-job.")

  username=retrieveDBData(sessionid,"username")
  canrun=checkUserJobPerms(sessionid,username,"automation-awx-jobtesting-job")
  if canrun == False:
    return render_template('awxerror.html',URLPREFACE=URLPREFACE,errordata="Error: you are not in a group that can view this job.")
  f = open('json/dynamicexample.json')
  jobdata = json.load(f)
  f.close()
  expiry=renewDBSession(sessionid)
  resp=make_response(render_template('awxjob.html',URLPREFACE=URLPREFACE,jobdata=jobdata))
  resp.set_cookie('sessionid', sessionid, httponly=True, secure=cookiesecurity, samesite='Lax',expires=expiry)
  return resp


@app.route('/automation-awx-lookup_user_ldap_groups')
def render_automation_awx_lookup_user_ldap_groups():
  sessionid=request.cookies.get('sessionid')
  sessioncheckresults=checkUserSession(sessionid)
  if sessioncheckresults!="ok":
    return render_template('login.html',URLPREFACE=URLPREFACE, redirecturl=f"{URLPREFACE}/automation-awx-lookup_user_ldap_groups",userinfo="Please log in with your ABC Active Directory account to continue to automation-awx-lookup_user_ldap_groups.")

  username=retrieveDBData(sessionid,"username")
  canrun=checkUserJobPerms(sessionid,username,"automation-awx-lookup_user_ldap_groups-job")
  if canrun == False:
    return render_template('awxerror.html',URLPREFACE=URLPREFACE,errordata="Error: you are not in a group that can view this job.")
  f = open('json/automation-awx-lookup_user_ldap_groups.json')
  jobdata = json.load(f)
  f.close()
  expiry=renewDBSession(sessionid)
  resp=make_response(render_template('awxjob.html',URLPREFACE=URLPREFACE,jobdata=jobdata))
  resp.set_cookie('sessionid', sessionid, httponly=True, secure=cookiesecurity, samesite='Lax',expires=expiry)
  return resp


@app.route('/skillsmatrixassessment')
def render_skillsmatrixassessment():
  sessionid=request.cookies.get('sessionid')
  sessioncheckresults=checkUserSession(sessionid)
  if sessioncheckresults!="ok":
    return render_template('login.html',URLPREFACE=URLPREFACE, redirecturl=f"{URLPREFACE}/skillsmatrixassessment",userinfo="Please log in with your ABC Active Directory account to continue to skillsmatrixassessment.")

  username=retrieveDBData(sessionid,"username")
  canrun=checkUserJobPerms(sessionid,username,"automation-awx-itoa_survey-job")
  if canrun == False:
    return render_template('awxerror.html',URLPREFACE=URLPREFACE,errordata="Error: you are not in a group that can view this job.")
  f = open('json/automation-awx-itoa_survey.json')
  jobdata = json.load(f)
  f.close()
  expiry=renewDBSession(sessionid)
  resp=make_response(render_template('awxjob.html',URLPREFACE=URLPREFACE,jobdata=jobdata))
  resp.set_cookie('sessionid', sessionid, httponly=True, secure=cookiesecurity, samesite='Lax',expires=expiry)
  return resp


@app.route('/automation-awx-jobtesting-job')
def render_automation_awx_jobtesting_job():
  sessionid=request.cookies.get('sessionid')
  sessioncheckresults=checkUserSession(sessionid)
  if sessioncheckresults!="ok":
    return render_template('login.html',URLPREFACE=URLPREFACE, redirecturl=f"{URLPREFACE}/automation-awx-jobtesting-job",userinfo="Please log in with your ABC Active Directory account to continue to automation-awx-jobtesting-job.")

  username=retrieveDBData(sessionid,"username")
  canrun=checkUserJobPerms(sessionid,username,"automation-awx-jobtesting-job")
  if canrun == False:
    return render_template('awxerror.html',URLPREFACE=URLPREFACE,errordata="Error: you are not in a group that can view this job.")
  f = open('json/jobexample1.json')
  jobdata = json.load(f)
  f.close()
  expiry=renewDBSession(sessionid)
  resp=make_response(render_template('awxjob.html',URLPREFACE=URLPREFACE,jobdata=jobdata))
  resp.set_cookie('sessionid', sessionid, httponly=True, secure=cookiesecurity, samesite='Lax',expires=expiry)
  return resp


@app.route('/automation-awx-itcc_handover_page')
def render_automation_awx_itcc_handover_page():
  sessionid=request.cookies.get('sessionid')
  sessioncheckresults=checkUserSession(sessionid)
  if sessioncheckresults!="ok":
    return render_template('login.html',URLPREFACE=URLPREFACE, redirecturl=f"{URLPREFACE}/automation-awx-itcc_handover_page",userinfo="Please log in with your ABC Active Directory account to continue to automation-awx-itcc_handover_page.")

  username=retrieveDBData(sessionid,"username")
  canrun=checkUserJobPerms(sessionid,username,"automation-awx-itcc_handover_page-job")
  if canrun == False:
    return render_template('awxerror.html',URLPREFACE=URLPREFACE,errordata="Error: you are not in a group that can view this job.")
  f = open('json/automation-awx-itcc_handover_page.json')
  jobdata = json.load(f)
  f.close()
  expiry=renewDBSession(sessionid)
  resp=make_response(render_template('awxjob.html',URLPREFACE=URLPREFACE,jobdata=jobdata))
  resp.set_cookie('sessionid', sessionid, httponly=True, secure=cookiesecurity, samesite='Lax',expires=expiry)
  return resp


@app.route('/all-inputs-example')
def render_all_inputs_example():
  sessionid=request.cookies.get('sessionid')
  sessioncheckresults=checkUserSession(sessionid)
  if sessioncheckresults!="ok":
    return render_template('login.html',URLPREFACE=URLPREFACE, redirecturl=f"{URLPREFACE}/all-inputs-example",userinfo="Please log in with your ABC Active Directory account to continue to all-inputs-example.")

  username=retrieveDBData(sessionid,"username")
  canrun=checkUserJobPerms(sessionid,username,"automation-awx-jobtesting-job")
  if canrun == False:
    return render_template('awxerror.html',URLPREFACE=URLPREFACE,errordata="Error: you are not in a group that can view this job.")
  f = open('json/allinputs.json')
  jobdata = json.load(f)
  f.close()
  expiry=renewDBSession(sessionid)
  resp=make_response(render_template('awxjob.html',URLPREFACE=URLPREFACE,jobdata=jobdata))
  resp.set_cookie('sessionid', sessionid, httponly=True, secure=cookiesecurity, samesite='Lax',expires=expiry)
  return resp


