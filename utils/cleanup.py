import shutil
import os

def cleanup_tempdirs(tempdirs):
    for d in tempdirs:
        if os.path.exists(d) and os.path.isdir(d):
            shutil.rmtree(d, ignore_errors=True)