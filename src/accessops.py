#!/bin/env python3
# This file contains the logic behind who gets access to what and how.
# It also does the LDAP login for the user and retrieves their groups.
import os
import glob
import ldap3
import json
from dbops import *

LDAP_HOST=os.environ["LDAP_HOST"]

try:
  LDAP_BASEDN=os.environ["LDAP_BASEDN"]
except:
  print("Error loading LDAP_BASEDN env var. Defaulting to OU=users,DC=something,DC=company,DC=com")
  LDAP_BASEDN="OU=users,DC=something,DC=company,DC=com"

try:
  GROUP_BASE=os.environ["GROUP_BASE"]
except:
  print("Error loading GROUP_BASE env var. Defaulting to DC=something,DC=company,DC=com")
  GROUP_BASE="DC=something,DC=company,DC=com"
AUTO_BIND_NO_TLS=True

# Change this for local dev
jsonfilesdir="/git/automation-portal-simportal/src/json/"
try:
  jsonfilesdir=os.environ["JSON_FILES_DIR"]
except:
  print("Error loading JSON_FILES_DIR env var. Defaulting to /usr/portal/json/")
  jsonfilesdir="/usr/portal/json/"

externallinksdir="/git/automation-portal-simportal/src/external_links/"
try:
  externallinksdir=os.environ["JSON_LINKS_DIR"]
except:
  print("Error loading JSON_LINKS_DIR env var. Defaulting to /usr/portal/external_links/")
  externallinksdir="/usr/portal/external_links/"

logfiltersdir="/git/automation-portal-simportal/src/log_filters/"
try:
  logfiltersdir=os.environ["JSON_FILTERS_DIR"]
except:
  print("Error loading JSON_FILTERS_DIR env var. Defaulting to /usr/portal/log_filters/")
  logfiltersdir="/usr/portal/log_filters/"


if os.path.exists(jsonfilesdir)==False:
  raise Exception(f"{jsonfilesdir} does not exist!")

if os.path.isdir(jsonfilesdir)==False:
  raise Exception(f"{jsonfilesdir} is not a directory!")



def getJobLogFilters(jobname):
  data=[]
  returndata={}
  for file in glob.glob(f"{logfiltersdir}*.json"):
    with open(file) as f:
      datafromfile=json.load(f)
      datafromfile["filename"]=file
      data.append(datafromfile)
  for item in data:
    if item["awx-job-name"] == jobname:
      if "replacements" in item:
        returndata["replacements"]=item["replacements"]
      if "regex_replacements" in item:
        returndata["regex_replacements"]=item["regex_replacements"]
  return returndata



def checkGroups(adgroups,jobgroups):
  for aditem in adgroups:
    for jobitem in jobgroups:
      if jobitem.lower() == aditem.lower():
        return True
  return False

# Function to retrieve what jobs and endpoints should be accessible to the user based on his or her AD groups in our json files.
def populateUserJobsAndEndpoints(usergroups):
  data=[]
  for file in glob.glob(f"{jsonfilesdir}*.json"):
    with open(file) as f:
      datafromfile=json.load(f)
      datafromfile["filename"]=file
      data.append(datafromfile)
      print(f"added {datafromfile['filename']} for user")
  validjobs=[]
  validendpoints=[]
  for job in data:
    if checkGroups(usergroups,job['valid-ad-groups']) or 'everyone' in job['valid-ad-groups']:
      validjobs.append(job['awx-job-name'])
      validendpoints.append(job['portal-endpoint'])
  datalinks=[]
  print("checking links...")
  for file in glob.glob(f"{externallinksdir}*.json"):
    with open(file) as f:
      datafromfile=json.load(f)
      datafromfile["filename"]=file
      datalinks.append(datafromfile)
      print(f"added {datafromfile['filename']} for user")
  validlinks=[]
  for extlink in datalinks:
    nameo=extlink['name']
    groupo=extlink['valid-ad-groups']
    if checkGroups(usergroups,extlink['valid-ad-groups']) or 'everyone' in extlink['valid-ad-groups']:
      validlinks.append(extlink['name'])
  return (validjobs,validendpoints,validlinks)

def getLinkInfo(linkgroup):
  datalinks=[]
  toreturn=[]
  for file in glob.glob(f"{externallinksdir}*.json"):
    with open(file) as f:
      datafromfile=json.load(f)
      datafromfile["filename"]=file
      datalinks.append(datafromfile)
  for linkname in linkgroup:
    for extlink in datalinks:
      nameo=extlink['name']
      if nameo==linkname:
        toreturn.append(extlink)
  return toreturn


# Function to query our db for user's allowed jobs
def getUserJobsByGroup(sessionid):
  try:
    jobshere=retrieveDBData(sessionid,"jobs")
    if jobshere != None:
      #print(f"DB hit for jobs that {sessionid} can run! Jobs: {jobshere}")
      return jobshere.split(",")
  except Exception as e:
    print(f"User getUserJobsByGroup db error: {e}")
  return False
    
def getJobsRanByURL():
  allowedjobs=[]
  for file in glob.glob(f"{jsonfilesdir}*.json"):
    with open(file) as f:
      datafromfile=json.load(f)
      try:
        if "url" in datafromfile['run-via']:
          allowedjobs.append(datafromfile['awx-job-name'])
      except:
        pass
  return allowedjobs

# Function to query our db for user's endpoints
def getUserEndpointsByGroup(sessionid):
  try:
    jobshere=retrieveDBData(sessionid,"endpoints")
    if jobshere != None:
      return jobshere.split(",")
  except Exception as e:
    print(f"User getUserEndpointsByGroup jobs db error: {e}")
  return False

def loginUserLDAP(ldusername,ldpassword,domain):
  print(f"username is {ldusername}")
  print(f"Querying LDAP for {ldusername} groups...")
  conn = ldap3.Connection(ldap3.Server(LDAP_HOST, port=389, use_ssl=False),
    auto_bind=AUTO_BIND_NO_TLS, user=f"{ldusername}@{domain}",
    password=ldpassword)
  filter3=f'(&(sAMAccountName={ldusername}))'
  conn.search(search_base=GROUP_BASE,
    search_filter=filter3, search_scope="SUBTREE",
    attributes=['memberOf'], size_limit=0)
  response=json.loads(str(conn.response_to_json()))
  memberof=response['entries'][0]['attributes']['memberOf']
  return memberof

print(getJobsRanByURL())
