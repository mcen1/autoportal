#!/bin/env python3
import requests
import json
import time
import urllib3
import os
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def lookupKey(keytofind):
#  print(f"Looking up {keytofind} in environment variables...")
#  if keytofind in os.environ:
#    print(f"Found {keytofind} in environment variables!")
#  else:
#    print(f"Couldn't find {keytofind} in environment variables. A default value might be used.")
  return os.environ.get(str(keytofind))

token=''
api_url=''
try:
  token=lookupKey('API_TOKEN')
except Exception as e:
  print(f'ERROR: API_TOKEN undefined! Cannot launch any AWX jobs. Error: {e}')
  token=''
if not token:
  print('ERROR: API_TOKEN undefined! Cannot launch any AWX jobs.')
  token=''

headers={"Content-type": "application/json",'apikey': token}

try:
  apiurl=lookupKey('API_URL')
except Exception as e:
  print('ERROR: API_URL undefined environment variable. Cannot launch any AWX jobs. Error: {e}')
  apiurl=''
if not apiurl:
  print('ERROR: API_URL is empty. Cannot launch any AWX jobs. {apiurl}')

try:
  certVerify = lookupKey('CERT_VERIFY')
except Exception as e:
  certVerify = '/etc/ssl/certs/ca-certificates.crt'

if not certVerify:
  certVerify = '/etc/ssl/certs/ca-certificates.crt'

if certVerify.lower()=="false":
  certVerify=False
certVerify=False

def postJobAPI(tosend):
  now = datetime.datetime.now()
  url=f"https://{apiurl}/api/api/v1/automation/awx_launch/launch_nowait"
  x = requests.post(url,json = tosend, verify=certVerify, headers=headers)
  job_output=x.text
  #print(json.dumps(json_output, indent=4))
  return job_output

def getJobName(jobID):
  now = datetime.datetime.now()
  url=f"https://{apiurl}/api/api/v1/automation/awx_launch/job_info"
  x = requests.post(url, json={"job_id": jobID}, verify=certVerify,headers=headers)
  job_output=json.loads(x.text)
  job_name=job_output['results']['name']
  #print(json.dumps(json_output, indent=4))
  return job_name

def getOutputOAPI(jobID,outputtype):
  now = datetime.datetime.now()
  url=f"https://{apiurl}/api/api/v1/automation/awx_launch/job_status_format"
  x = requests.post(url, json={"job_id": jobID,"output_format": outputtype}, verify=certVerify,headers=headers)
  job_output=x.text
  #print(json.dumps(json_output, indent=4))
  return job_output



def runAPIJob(userparams,username,extrastuff):
  if 'awx-job-name' not in userparams:
    print("error: parameters passed to runAPIJob are malformed.")
    return {"error": "parameters passed to runAPIJob are malformed."}
  extravars={"_ab_itoa_portal_meta_launched": True, "_ab_itoa_portal_meta_ranby": username}
  # add extravars from form into posting
  for item in userparams:
    if item.startswith('extravar'):
      extravars[item.replace("extravar","")]=userparams[item]
  for item in extrastuff:
    print(f"adding {item} via extrastuff")
    extravars[item]=extrastuff[item]
  jobNumber=postJobAPI({"job_name":userparams['awx-job-name'],"job_params": {"extra_vars":extravars}})
  now = datetime.datetime.now()
  print(f"{now} Jobnumber is: {jobNumber}")
  return jobNumber

