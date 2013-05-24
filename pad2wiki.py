#!/usr/bin/python
import mwclient
import requests
from urlparse import urlparse
import sys
import json

def get_pad(url):
	url_parts = urlparse(url)
	baseurl = url_parts.netloc
	url_parts = urlparse(url)
	pad_id =  url_parts.path.split("/")
	pad_id =  pad_id[1]
	text = requests.get("http://%s/ep/pad/export/%s/latest?format=wiki" % (baseurl, pad_id))
	return text.text


def put_wiki(url, text, config):
	site = mwclient.Site(config["url"], path=config["wiki_path"])
	site.login(config["username"], config["password"])
	page = site.Pages[url]	
	page.save(text=text, bot=True)


args = sys.argv
if len(args) == 3:
	pad_url = args[1]
	wiki_url = args[2]
else:
	print "Usage: pad2wiki.py <pad_url> <wiki_url>"
	sys.exit()
config_file = open("config.json")
config =  config_file.read()
config = json.loads(config)

pad_data = get_pad(pad_url)

put_wiki(wiki_url, pad_data, config)

print "done"

