#!/usr/local/bin/python
import json

ignoredRemoteApps = json.load(open("remote_apps_ignored.json","r"))

remoteAppDataRaw = json.load(open("remote_apps.json","r"))
remoteSplunkbaseApps = [app for app in remoteAppDataRaw['apps'] if 'splunkbaseID' in app]
json.dump({"apps":remoteSplunkbaseApps},open("remote_splunkbase_apps.json","w"), indent=4)
print("Written remote_splunkbase_apps.json")

# Ignore apps which are part of SplunkCloud Core app list
remotePrivateApps = [app for app in remoteAppDataRaw['apps'] if app['appID'] not in ignoredRemoteApps]
json.dump({"apps":remoteSplunkbaseApps},open("remote_private_apps.json","w"), indent=4)
print("Written remote_private_apps.json")
# # Restructure to allow addressable values by appId
# targetAppDataObj = {}
# for app in targetAppDataRaw['apps']:
#     targetAppDataObj[f"{app['id']}"] = app
# print(targetAppDataObj)
# licenseData = json.load(open("licenses.json","r"))
# for app in licenseData['apps']:
#     print(f"AppID={app['id']} licenseUrl={app['licenseUrl']}")
#     print(targetAppDataObj[f"{app['id']}"])
#     targetAppDataObj[f"{app['id']}"]['licenseUrl'] = app['licenseUrl']
# print(targetAppDataObj)
#
# licensedTargetAppDataObj = [targetAppDataObj[app] for app in targetAppDataObj]
# json.dump({"apps":licensedTargetAppDataObj}, open("licensed_target_splunkbase_apps.json","w"), indent=4)