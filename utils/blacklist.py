import fnmatch
import os
import yaml

def load_blacklist(path="ironshell/blacklist.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)["paths"]

def is_path_blacklisted(path, blacklist):
    abspath = os.path.abspath(path)
    for rule in blacklist:
        if abspath.startswith(rule) or fnmatch.fnmatch(abspath, rule):
            return True
    return False