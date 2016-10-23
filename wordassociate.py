#!/usr/bin/env python
#sudo apt install python-pip
#pip install unirest

import unirest

def getresponsedata(word):
	getrequest="https://twinword-word-associations-v1.p.mashape.com/associations/?entry={0}".format(word)

	response = unirest.get(getrequest,
  headers={
    "X-Mashape-Key": "YjvTlL2nnhmshJTqqmZvHwI6UM9Hp1YmNsUjsn8jGEjUuTxUx8"
  }
)
	return response;

def getresponse(word):
	errString = "Problem associating word"
	responsedata = getresponsedata(word);
	if (responsedata.code == 200 ):
		try:
			returnlist = responsedata.body["associations"]
			return returnlist;
		except:
			return errString;
	else:
		return errString;

