#!/usr/bin/python

import urllib3, sys, argparse, json, datetime
# from pprint import pprint

http = urllib3.PoolManager()

ver = "0.1"

# The UpTime Robot API key can be found under "My Settings" page
key = "YOUR_API_KEY"


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


statuses = {
    '0': {
        'descr': 'Paused',
        'color': color.YELLOW
    },
    '1': {
        'descr': 'Not checked yet',
        'color': color.YELLOW
    },
    '2': {
        'descr': 'Up',
        'color': color.GREEN
    },
    '8': {
        'descr': 'Seems down',
        'color': color.RED
    },
    '9': {
        'descr': 'Down',
        'color': color.RED
    }
}



def introText():
	print 'uptrobot.py v' + ver + ' - Created by George Sokianos'



def apiGetMonitors():
    url = "https://api.uptimerobot.com/v2/{0}".format('getMonitors')
    jsonFields = {
        "api_key": key,
        "format": "json",
        "logs": 1
    }
    jsonHeaders = {
        'cache-control': "no-cache"
    }
    request = http.request('POST', url, headers=jsonHeaders, fields=jsonFields, timeout=5.0)

    response = request.status
    retData = json.loads(request.data)
    # print response
    # print request.data
    return retData


def printMonitors(rawdata):
    print "Found " + str(rawdata["pagination"]['total']) + " monitors\n"
    print "ID              Name                    Status"
    print "----------      --------------------    ----------"
    for monitor in rawdata["monitors"] :
        statusId = str(monitor['status'])               # Get the monitor status ID
        statusStr = statuses[statusId]['descr']         # Get the description for this status, from the dictionary
        display = statuses[statusId]['color']           # Get the color for this status, from the dictionary
        statusChangeTime = monitor['logs'][0]['datetime']       # Get the last status change datetime, which is a timestamp
        datetimeStr = datetime.datetime.fromtimestamp(statusChangeTime).strftime('%Y-%m-%d %H:%M')      # Convert the last status change datetime to human datetime
        print "{0:<10}\t{1:<20}\t{colorStr}{2:} since {3} {endStr}".format(monitor['id'], monitor['friendly_name'], statusStr, datetimeStr, colorStr=display,endStr=color.END)


def main(argv):

    # Parse the arguments
    argParser = argparse.ArgumentParser(description='This is a python script that can be used to get information about your monitors at UpTime Robot (https://uptimerobot.com). For more information visit https://github.com/walkero-gr/uptrobot ')

    argParser.add_argument('--version', action='version', version='%(prog)s v' + ver)

    args = argParser.parse_args()

    introText()

    monitorsData = apiGetMonitors()
    printMonitors(monitorsData)



if __name__ == "__main__":
	main(sys.argv[1:])

