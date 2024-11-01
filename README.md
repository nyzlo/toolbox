# Toolbox

## Installation

#### Requirements: Python 3
- `git clone https://github.com/nyzlo/toolbox`
- `cd toolbox`
- `pip install -r requirements.txt`

## Usage
### Chen (subdomain & technology finder)
`python main.py chen https://www.hackerone.com`
### Aiur (ssh & ftp bruteforcer)
```
-H Host of the target: -H host
-s Service choice: -s ssh / ftp
-l Username: -l username 
-L Username wordlist: -L path/to/wordlist
-p Password: -p password
-P Password wordlist: -P path/to/wordlist
-t Non-default port: -t 2220 (default 22 ssh, 21 ftp when omitted -t flag)
```
`python main.py aiur -H bandit.labs.overthewire.org -s ssh -l bandit0 -p bandit0 -t 2220`

`python main.py aiur -H ftp.dlptest.com -s ftp -l dlpuser -p rNrKYTX9g7z3RgJRmxWuGHbeu`
### Arakaali (spider)
`python main.py arakaali https://www.inlanefreight.com`

### Restrictions
General
- All tools are designed for usage on Linux

Chen
- Less potetent than already existing tools in the same category

Aiur
- Performance is lacking and doesn't utilize threading/asynchronous calls

Arakaali
- Domain restriction logic is primitive
- Only handles single URL input in its current itteration
