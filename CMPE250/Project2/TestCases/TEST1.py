from phBot import *
import phBotChat
from time import sleep
import urllib.request

log("Plugin: KervanKey alındı.")

# Return string containing the kervankey
def getKervanKey():
	# Emulating a quick browser
	req = urllib.request.Request("http://rsilkroad.com/", headers={'User-Agent' : "JellyBrowser"})
	# Getting stream
	resp = urllib.request.urlopen(req)
	# Getting html data
	html = str(resp.read().decode("utf-8"))  # => "<!DOCTYPE html><html><head>..."
	# Extracting data: <span id="KervanKey" class="text-orange">XXX</span>
	pos = html.find('<span id="KervanKey" class="text-orange">') # 41 characters used to find the right position
	kervankey = html[pos+41:pos+41+10].split("<")[0] # in case is not only three number key
	log("Plugin: KervanKey girildi. ("+kervankey+")")
	return kervankey

def handle_chat(t, player, msg):
	if len(player) > 0:
		if player == "BotCheck" and "BotCheck" in msg:
			sleep(1.0)
			phBotChat.Private(player,getKervanKey())

getKervanKey() # just for test purpose at loading
