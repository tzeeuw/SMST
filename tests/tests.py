import json


version_list = json.load(open("versions.json", 'r'))

installation_versions = version_list.keys()

print(version_list.keys())
