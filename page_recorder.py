from flask import Flask
from flask import request
import codecs
import argparse
import time
import datetime

timestampfname = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


parser = argparse.ArgumentParser(
    description="""Listens to javascript output and saves it to a file""")
parser.add_argument("outfilename",
    help="Name of outfile e.g. outfilename.txt",
    default='outfile.txt'+timestampfname, nargs='?')
args = parser.parse_args()

app = Flask(__name__)

fileout = codecs.open('Pagerecordings/'+args.outfilename+timestampfname, 'w', 'utf-8')

@app.route('/', methods=['POST'])
def hello_world():
	print(str(request.form))
	fileout.write(str(request.form))
	#return str(request.form)

#	return 'Hello World!'


app.run(debug=True)
fileout.close()