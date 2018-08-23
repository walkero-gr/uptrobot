**uptrobot.py** is a python script that can be used to get information from [UpTime Robot](https://uptimerobot.com) to your terminal. It uses your account UpTime Robot API key to get the information and print them.

Features:
- show the monitors the user has created and their status
- use follow mode to autorefresh the list in every n secs (default: 300). The update seconds can be set using the **-s SLEEP, --sleep SLEEP** parameter.


### Usage
Before you use the script you have to edit it and add your API key. The UpTime Robot API key can be found under "My Settings" page.

The above values should be entered at the following line of the script, by replacing the dummy values.

```python
key = "YOUR_API_KEY"
```
As soon as you save the script you are good to go. Open a terminal and run the script using 
```bash
uptrobot.py [-h] [-f] [-s SLEEP] [--version]
```

To make it available from any folder on your Linux machine, you can edit the .bashrc file under your user home folder and add the following line at the end of the file.
```
export PATH=$PATH:</path/to/file>
```


#### Parameters and Actions
```bash
uptrobot.py [-h] [-f] [-s SLEEP] [--version]

This is a python script that can be used to get information about your
monitors at UpTime Robot (https://uptimerobot.com). For more information visit
https://github.com/walkero-gr/uptrobot

optional arguments:
  -h, --help            show this help message and exit
  -f, --follow          keep requesting information until the user press
                        CTRL-C
  -s SLEEP, --sleep SLEEP
                        set the maximum sleep time in seconds, when using the
                        follow mode
  --version             show program's version number and exit
```
