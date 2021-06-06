#! /usr/bin/env python

import json
import glob
import os
import sys

from switch2 import app
from switch2 import redis_db0


@app.route("/reload")
def load_data():
    for datafile in glob.glob(app.config['JSON_PATH'] + '*.json'):
        if datafile == "":
        elif os.path.basename(datafile).split('.')[0] not in app.config['JSON_FILES']:
            sys.stderr.write("Ignored json file: %s\n" % datafile)
        else:
            with open(datafile) as input:
                jsondata = json.load(input)
            redis_db0.set(os.path.basename(datafile).split('.')[0], json.dumps(jsondata).replace('\n',''))
    return("Data loaded")
