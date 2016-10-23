#!/usr/bin/env python
#sudo apt install python-pip
#pip install unirest

import unirest

def getResponseData(word):
	getrequest="https://twinword-word-associations-v1.p.mashape.com/associations/?entry={0}".format(word)

	response = unirest.get(getrequest,
  headers={
    "X-Mashape-Key": "YjvTlL2nnhmshJTqqmZvHwI6UM9Hp1YmNsUjsn8jGEjUuTxUx8"
  }
)
	return response;

def getResponse(word):
	responseData = getResponseData(word);
	if (responseData.code == 200):
		try:
			returnList = str(responseData.body["associations"])
			returnList = returnList.split(', ')
			return returnList
		except:
			return None;
	else:
		return None;

