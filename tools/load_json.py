import os
import json

def file2json(file_name):
    f=open(file_name,'r')
    lines=f.read()
    j=json.loads(lines)
    f.close()
    return j
