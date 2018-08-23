**uptrobot.py** is a python script that can be used to get information from [UpTime Robot](https://uptimerobot.com) to your terminal. It uses your account UpTime Robot API key to get the information and print them.

Features:
- show the monitors the user has created and their status


### Usage
Before you use the script you have to edit it and add the your API key. The UpTime Robot API key can be found under "My Settings" page.

The above values should be entered at the following line of the script, by replacing the dummy values.

```python
key = "YOUR_API_KEY"
```
As soon as you save the script you are good to go. Open a terminal and run the script using 
```bash
uptrobot.py [-h] [--version]
```

To make it available from any folder on your Linux machine, you can edit the .bashrc file under your user home folder and add the following line at the end of the file.
```
export PATH=$PATH:</path/to/file>
```


#### Parameters and Actions
```bash
uptrobot.py [-h] [--version]

This is a python script that can be used to get information about your
monitors at UpTime Robot (https://uptimerobot.com). For more information visit
https://github.com/walkero-gr/uptrobot

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```
