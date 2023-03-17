# Apps
##Get Existing apps
`acsstg apps list > remote_apps.json`

Returns 
```json
    {
      "appID": "splunk_product_guidance",
      "label": "Splunk Product Guidance",
      "name": "splunk_product_guidance",
      "splunkbaseID": "5137",
      "stateChangeRequiresRestart": false,
      "status": "installed",
      "version": "1.2.1"
    }
  ]
```

## Get Existing apps which are Splunkbase apps
Note the presence of splunkbaseID key  
`acsstg apps list > remote_apps.json | jq '.[] | map(select(.splunkbaseID))'`  
or  
`acsstg apps list --count 100 --splunkbase=true`
## Get License info
`acsstg apps bulk-fetch-license --file target_splunkbase_apps.json --output-file licenses.json --report-file license-report.json`

## Steps
1. Download a copy of the current apps installed on the Splunk Cloud stack using:  
`acsstg apps list --count 100 > remote_apps.json`  
<br>

2. Parse the remote apps list into private (custom) and SplunkBase apps, also ignoring any apps recorded in `remote_apps_ignored.json` which would typically be internal Splunk apps on the Splunk Cloud stack.  
`./digestRemoteApps.py`  
  <br>

3. Determine any missing license data for Splunkbase apps in the target state file:  
`acsstg apps bulk-fetch-license --file target_splunkbase_apps.json --output-file licenses.json --report-file license-report.json`  
<br>
  
4. Determine any Splunkbase apps which require install/upgrade/uninstall:  
`./digestTargetSplunkbaseApps.py`  
<br>

5. 

# Indexes
## Get Current index list
1. run getIndexList.sh  
2. compare