import os
import json
from json import JSONDecoder
import re

NOT_WHITESPACE = re.compile(r'[^\s]')

def decode_stacked(document, pos=0, decoder=JSONDecoder()):
    while True:
        match = NOT_WHITESPACE.search(document, pos)
        if not match:
            return
        pos = match.start()
        
        try:
            obj, pos = decoder.raw_decode(document, pos)
        except ValueError:
            # do something sensible if there's some error
            raise
        yield obj

s = """

{"a": 1}  


   [
1
,   
2
]


"""

path = '/Users/josue/Desktop/SLIM/robotbehaviordata/cozmo_filtered/states'
for filename in os.listdir(path):
    json_objects = []
    if filename == ".DS_Store":
        continue
    with open(os.path.join(path, filename), 'r') as f:
        text = f.read()
    for obj in decode_stacked(text):
        json_objects.append(json.loads(json.dumps(obj)))
    with open(os.path.join(path, filename), 'w') as f:
        f.write('')
    with open(os.path.join(path, filename), 'a') as f:
        for obj in json_objects:
            obj['value'] = json.loads(obj['value'])
        print('filename: ', str(filename))
        try:
            f.write(json.dump({'states': json_objects}, f, indent=2))
        except:
            continue
        json_objects = []

