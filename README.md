# Toolbox

## Installation

#### Requirements: Python 3
- `git clone https://github.com/nyzlo/toolbox`
- `cd toolbox`
- `pip install -r requirements.txt`

## Usage
### Chen (subdomain & technology finder)
`python main.py chen hackerone.com`
### Aiur (ssh & ftp bruteforcer)
#### Options
```
-H Host of the target: -H host
-s Service choice: -s ssh / ftp
-l Username: -l username 
-L Username wordlist: -L path/to/wordlist
-p Password: -p password
-P Password wordlist: -P path/to/wordlist
-t Port: -t X (defaults to 22 for SSH, 21 for FTP when omitted)
```

`python main.py aiur -H bandit.labs.overthewire.org -s ssh -l bandit0 -p bandit0 -t 2220`

`python main.py aiur -H ftp.dlptest.com -s ftp -l dlpuser -p rNrKYTX9g7z3RgJRmxWuGHbeu`
### Arakaali (spider)
`python main.py arakaali https://www.inlanefreight.com`
