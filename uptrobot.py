#!/usr/bin/python

import urllib3, sys, argparse, json, datetime, time, curses, signal

http = urllib3.PoolManager()

ver = "0.4"

# The UpTime Robot API key can be found under "My Settings" page
key = "YOUR_API_KEY"

defSleepTime = 300

class color:
   PURPLE       = '\033[95m'
   CYAN         = '\033[96m'
   DARKCYAN     = '\033[36m'
   BLUE         = '\033[94m'
   GREEN        = '\033[92m'
   YELLOW       = '\033[93m'
   RED          = '\033[91m'
   BOLD         = '\033[1m'
   UNDERLINE    = '\033[4m'
   END          = '\033[0m'


# Monitors' status decoding
statuses = {
    '0': { 'descr': 'Paused',           'color': color.YELLOW   },
    '1': { 'descr': 'Not checked yet',  'color': color.YELLOW   },
    '2': { 'descr': 'Up',               'color': color.GREEN    },
    '8': { 'descr': 'Seems down',       'color': color.RED      },
    '9': { 'descr': 'Down',             'color': color.RED      }
}

# Output messages
msg = {
    # 1xx Informational response
    '101': 'Enabled follow mode. Press Ctrl+C to exit.',

    # 2xx Success

    # 3xx Client errors
    '301': 'There was an error with the API request. Type -h to see the help text.',

    # 4xx Server errors

}


def introText():
	print 'uptrobot.py v' + ver + ' - Created by George Sokianos'


def signal_handler(sig, frame):
    curses.endwin()
    print('You pressed Ctrl+C!')
    sys.exit(0)



class APIHandler:
    def __init__(self):
        self.baseurl = 'https://api.uptimerobot.com/v2/'

        return


    def getMonitors(self):
        url = "{0}{1}".format(self.baseurl, 'getMonitors')
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

        if response == 200 and retData['stat'] == 'ok' :
            return retData
        else :
            return False


class outputHandler:
    def __init__(self):
        self.rawdata = {}

        return

    def printMonitors(self):
        nowStr = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        sys.stdout.write("Last update: {0}\n\r".format(nowStr))
        sys.stdout.write("Found " + str(self.rawdata["pagination"]['total']) + " monitors\n\n\r")
        sys.stdout.write("ID              Name                    Status\n\r")
        sys.stdout.write("----------      --------------------    ----------\n\r")
        for monitor in self.rawdata["monitors"] :
            statusId = str(monitor['status'])               # Get the monitor status ID
            statusStr = statuses[statusId]['descr']         # Get the description for this status, from the dictionary
            display = statuses[statusId]['color']           # Get the color for this status, from the dictionary
            statusChangeTime = monitor['logs'][0]['datetime']       # Get the last status change datetime, which is a timestamp
            datetimeStr = datetime.datetime.fromtimestamp(statusChangeTime).strftime('%Y-%m-%d %H:%M')      # Convert the last status change datetime to human datetime
            sys.stdout.write("{0:<10}\t{1:<20}\t{colorStr}{2:} since {3} {endStr}\n\r".format(monitor['id'], monitor['friendly_name'], statusStr, datetimeStr, colorStr=display,endStr=color.END))


def main(argv):
    action = ''
    sleepTime = defSleepTime

    # Parse the arguments
    argParser = argparse.ArgumentParser(description='This is a python script that can be used to get information about your monitors at UpTime Robot (https://uptimerobot.com). For more information visit https://github.com/walkero-gr/uptrobot ')
    argParser.add_argument('-f', '--follow', action='store_true', default=False, dest='follow', help='keep requesting information until the user press CTRL-C')
    argParser.add_argument('-s', '--sleep', action='store', dest='sleep', type=int, help='set the maximum sleep time in seconds, when using the follow mode')

    argParser.add_argument('--version', action='version', version='%(prog)s v' + ver)

    args = argParser.parse_args()
    if args.follow :
        action = 'follow'
    if args.sleep :
        sleepTime = args.sleep

    introText()

    if action == 'follow':
        api = APIHandler()
        output = outputHandler()

        signal.signal(signal.SIGINT, signal_handler)

        stdscr = curses.initscr()
        curses.curs_set(0)

        timeLeft = 0
        while True:
            if timeLeft == 0 :
                monitorsData = api.getMonitors()
                if monitorsData :
                    stdscr.clear()
                    stdscr.refresh()
                    sys.stdout.write(msg['101'] + '\n\r')
                    output.rawdata = monitorsData
                    output.printMonitors()
                else :
                    curses.endwin()
                    print msg['301']
                    sys.exit(2)

                timeLeft = sleepTime
            else :
                sys.stdout.write('Update in {0} secs \r'.format(timeLeft))
                sys.stdout.flush()
                timeLeft = timeLeft - 1
            time.sleep(1)

    else :
        api = APIHandler()
        monitorsData = api.getMonitors()
        if monitorsData :
            output = outputHandler()
            output.rawdata = monitorsData
            output.printMonitors()
        else :
            print msg['301']
            sys.exit(2)



if __name__ == "__main__":
	main(sys.argv[1:])

