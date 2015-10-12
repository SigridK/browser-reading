from flask import Flask
from flask import request
import codecs
import argparser


parser = argparse.ArgumentParser(
    description="""Listens to EyeTribe ET output and saves it to a file""")
parser.add_argument("outfilename",
    help="Name of outfile e.g. outfilename.csv",
    default='outfile.csv', nargs='?')
args = parser.parse_args()

app = Flask(__name__)

fileout = codecs.open(args.outfilename, w, 'utf-8')

@app.route('/', methods=['POST'])
def hello_world():
	print(str(request.form))
	fileout.write(str(request.form))
	return str(request.form)

#	return 'Hello World!'


app.run(debug=True)