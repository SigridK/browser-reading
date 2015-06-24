from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
	print(str(request.form))
	return str(request.form)

#	return 'Hello World!'


app.run(debug=True)