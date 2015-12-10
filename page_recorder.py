from flask import Flask
from flask import request
import codecs
import argparse
import time
import datetime
import json


timestampfname = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
dataout = []

parser = argparse.ArgumentParser(
    description="""Listens to javascript output and saves it to a file""")
parser.add_argument("outfilename",
    help="Name of outfile e.g. outfilename.txt",
    default='outfile'+timestampfname+'.txt', nargs='?')
args = parser.parse_args()

app = Flask(__name__)

#fileout = codecs.open('Pagerecordings/'+timestampfname+args.outfilename, 'w', 'utf-8')

@app.route('/space', methods=['POST'])
def hello_world():
	#print(str(request.form))
	#fileout.write(str(request.form))
    dataout.append(request.form)
    return 'Hello World!'


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
	#print("received q")
    #not saved to file before your shut down server
    with open('Pagerecordings/'+timestampfname+args.outfilename, 'w') as outfile:
        json.dump(dataout, outfile)
    shutdown_server()
    return 'Server shutting down...'

app.run(debug=True)

