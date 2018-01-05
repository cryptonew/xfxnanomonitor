#import config
from config import *
import json, requests
import time
requests.packages.urllib3.disable_warnings()

def sendAlert(message, alert):
   	 # trigger IFTTT event
   	 report = {}
   	 report["value1"] = message
   	 requests.post("https://maker.ifttt.com/trigger/" + alert + "/with/key/" + iftttKey, data=report)

def getStats():
    	# query the nicehash API and check worker's status
    	url = 'https://api.nanopool.org/v1/eth/workers/' + ethAddress

    	resp = requests.get(url=url, verify=False)
    	stats = json.loads(resp.text)
    	return stats

stats = getStats()
#print stats

print len(stats.get("data"))

if len(stats.get("data")) < workers_num:
        print ""
        print "First Check Fails. Workers < " + str(workers_num)
        print stats
        print ""
        time.sleep(30)
        stats = getStats()
        if len(stats.get("data")) < workers_num:
                print ""
                print "Second Check Fails. Workers < " + str(workers_num)
                print stats
                print ""
                time.sleep(30)
                stats = getStats()
                if len(stats.get("data")) < workers_num:
                        sendAlert("XFX NanoPool worker DOWN. Please fix it!","nanopool")
                        print ""
                        print "Third Check Fails. Workers< " + str(workers_num) + " Sending Alert"
                        print stats
                        print ""
                        print time.strftime("%Y-%m-%d %H:%M:%S")
                        print "--------------------------------------------"
                        exit()

workers = stats['data']

for worker in workers:
    if float(worker['hashrate']) < 50:
        sendAlert("Trouble! Worker " + str(worker['id']) + " Speed = " + str(worker['hashrate']), "nanopool")
        print worker['id'] + "Accepted <50"
        print str(worker['id']) + "ETH Speed = " + str(worker['hashrate'])

print ""
print "Exit without Errors"
print "ETH Speed = " + str(worker['hashrate'])
print time.strftime("%Y-%m-%d %H:%M:%S")
print "--------------------------------------------"
exit()
