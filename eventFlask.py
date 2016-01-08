# This script starts a HTTP listener on port 8000
# Captures the Post data sent by SDN Manager for Lync Events like Start, End and Update
# Calls "eventQueue" script to parse the data and queue the event



from flask import Flask, request, make_response, json
import sys
from lxml import etree as ET
from ljunlib import eventQueue

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])

def lFlask():
	data = request.get_data()
	eventQueue(data)
	print data
	return "Success"


if __name__== "__main__":
    app.run(host='0.0.0.0', port=8000)
