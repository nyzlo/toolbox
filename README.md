# Toolbox

## Installation

#### Requirements: Python 3
- `git clone https://github.com/nyzlo/toolbox`
- `cd toolbox`
- `pip install -r requirements.txt`

## Usage
### Chen (subdomain & technology finder)
`python main.py chen hackerone.com`
### Arakaali (spider)
`python main.py arakaali https://www.inlanefreight.com`
### Aiur (ssh & ftp bruteforcer)
#### Options
```
-H Host of the target: -H host
-s Service choice: -s ssh / ftp
-l Username: -l username 
-L Username wordlist: -L path/to/wordlist
-p Password: -p password
-P Password wordlist: -P path/to/wordlist
-t Port: -t X (defaults to 22 for SSH, 21 for FTP)
```
`python main.py aiur -H host -s ssh -l user -P passwords -t 2220`

`python main.py aiur -H host -s ftp -L users -p password`
### Limitations
General
- All tools are designed and tested on Linux

Chen
- Less potetent than already existing tools in the same category

Arakaali
- Domain restriction logic is primitive
- Only handles single URL input in its current itteration
- Default Scrapy user-agent/no ip rotation goin' on, susceptible to just getting blocked

Aiur
- Performance is lacking and doesn't utilize threading/asynchronous calls
- Also likely to get blocked~
