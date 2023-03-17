#!/usr/local/bin/python
import json
import os

ACS_STACK=os.getenv("ACS_STACK","nhsdptl")
ACS_TOKEN=os.getenv("ACS_TOKEN","")

remoteIndexListRaw = json.load(open("remote_indexList.json","r"))
targetIndexListRaw = json.load(open("target_indexList.json","r"))

remoteIndexList = {}
for idx in remoteIndexListRaw:
    if 'totalRawSizeMB' in idx: del(idx['totalRawSizeMB'])
    if 'totalEventCount' in idx: del(idx['totalEventCount'])
    remoteIndexList[idx['name']] = idx

targetIndexList = {}
for idx in targetIndexListRaw:
    if 'totalRawSizeMB' in idx: del(idx['totalRawSizeMB'])
    if 'totalEventCount' in idx: del(idx['totalEventCount'])
    targetIndexList[idx['name']] = idx


indexesToCreate = [idx for idx in targetIndexListRaw if idx['name'] not in remoteIndexList]
indexesToDelete = [idx for idx in remoteIndexListRaw if idx['name'] not in targetIndexList]
indexesToUpdate = [idx for idx in targetIndexListRaw if idx['name'] in remoteIndexList and targetIndexList[idx['name']] != remoteIndexList[idx['name']] ]


#appsToUpdate = [targetAppDataObj[app] for app in targetAppDataObj if app not in externallyManagedApps and app in remoteAppDataObj and (targetAppDataObj[app]['version'] > remoteAppDataObj[app]['version'])]

print(f"Indexes to create: {len(indexesToCreate)}")
#print(indexesToCreate)
print(f"Indexes to update: {len(indexesToUpdate)}")
#print(indexesToUpdate)
print(f"Indexes to delete: {len(indexesToDelete)}")
#print(indexesToDelete)



def acsIndexFlag(key):
    flags = {
        "searchableDays":"--searchable-days",
        "maxDataSizeMB":"--max-data-size-mb",
        "selfStorageBucketPath":"--splunk-archival-retention-days",
        "splunkArchivalRetentionDays":"--self-storage-bucket-path"
    }
    if key in flags:
        return flags[key]
    else:
        print(f"Could not find flag mapping for {key}")
        exit(999)

def acsProcessIndex(idxDef, action, key=False):
    #TODO - Check that we are not trying to update an internal index
    #TODO - Disallow reducing prod index retention?
    #TODO - Disallow deleting prod indexes?

    if action=="update":
        print(f"[INFO] Updating index={idxDef['name']} key={key} to value={idxDef[key]}")
        flag=acsIndexFlag(key)
        command = f"acs indexes update {idxDef['name']} {flag} {idxDef[key]} -f structured"

    if action=="create":
        print(f"[INFO] Creating index={idxDef['name']}")
        command = f"acs indexes create --name {idxDef['name']} -f structured"

    if action=="delete":
        print(f"[INFO] Deleting index={idxDef['name']}")
        command = f"acs indexes delete {idxDef['name']} -f structured"

    print(command)



for idx in indexesToCreate:
    acsProcessIndex(idx, "create")

for idx in indexesToUpdate:
    for key in idx.keys():
        if idx[key]!=remoteIndexList[idx['name']][key]:
            print(f"[DEBUG] Difference in key={key} remoteVal={remoteIndexList[idx['name']][key]} targetVal={idx[key]}")
            acsProcessIndex(idx,"update", key)

for idx in indexesToDelete:
    acsProcessIndex(idx, "delete")

#Delete
# acs indexes delete test -f structured

#Create
# acs indexes create --name deleteme --data-type event --max-data-size-mb 500 --searchable-days 90 --splunk-archival-retention-days 0

# Update
# acs indexes update deleteme --searchable-days 30

#curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' YOUR_WEBHOOK_URL
