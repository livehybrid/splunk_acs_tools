#!/usr/local/bin/python
import json

acsExecutable="acsstg"

targetAppDataRaw = json.load(open("target_splunkbase_apps.json","r"))
# Restructure to allow addressable values by appId
targetAppDataObj = {}
externallyManagedApps = []
for app in targetAppDataRaw['apps']:
    if 'externallyManaged' in app and app['externallyManaged']==True:
        externallyManagedApps.append(str(app['id']))
    targetAppDataObj[f"{app['id']}"] = app

licenseData = json.load(open("license-report.json","r"))
for app in [licapp for licapp in licenseData['results'] if str(licapp['identifier']) in targetAppDataObj.keys()]:
    licResponse = json.loads(app['response'])
    print(f"splunkbaseId={app['identifier']} appId={licResponse['appid']} licenseUrl={licResponse['licenseUrl']}")
    targetAppDataObj[f"{app['identifier']}"]['licenseUrl'] = licResponse['licenseUrl']
    targetAppDataObj[f"{app['identifier']}"]['appid'] = licResponse['appid']

licensedTargetAppDataObj = [targetAppDataObj[app] for app in targetAppDataObj]
json.dump({"apps":licensedTargetAppDataObj}, open("target_splunkbase_apps.json","w"), indent=4)


# # licensedTargetAppDataObj = target state
remoteAppDataRaw = json.load(open("remote_splunkbase_apps.json","r"))
remoteAppDataObj = {}
for app in remoteAppDataRaw['apps']:
    remoteAppDataObj[f"{app['splunkbaseID']}"] = app

appsToUpdate = [targetAppDataObj[app] for app in targetAppDataObj if app not in externallyManagedApps and app in remoteAppDataObj and (targetAppDataObj[app]['version'] > remoteAppDataObj[app]['version'])]
appsToInstall = [targetAppDataObj[app] for app in targetAppDataObj if app not in remoteAppDataObj]
appsToRemove = [remoteAppDataObj[app] for app in remoteAppDataObj if app not in targetAppDataObj and app not in externallyManagedApps]
print(f"AppsToUpdate: {appsToUpdate}")
print(f"AppsToInstall: {appsToInstall}")
print(f"AppsToRemove: {appsToRemove}")

json.dump({"apps":appsToUpdate}, open("target_splunkbase_apps_update.json","w"),indent=4)
json.dump({"apps":appsToInstall}, open("target_splunkbase_apps_install.json","w"),indent=4)
json.dump({"apps":appsToRemove}, open("target_splunkbase_apps_remove.json","w"),indent=4)

print("Now run:")
print(f"{acsExecutable} apps bulk-install splunkbase --file target_splunkbase_apps_install.json")
print(f"{acsExecutable} apps bulk-uninstall splunkbase --file target_splunkbase_apps_remove.json")
# Update has to be done individually because there is
for updateApp in appsToUpdate:
    print(f"{acsExecutable} apps update {updateApp['appid']} --version {updateApp['version']} --acs-licensing-ack {updateApp['licenseUrl']}")