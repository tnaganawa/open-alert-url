When an alert is found,  
you have to open some url, which contains operation manual to deal with that alert.  
This script will open a new window for you.

It also could give some variables extracted from the alert to opened url,  
if opened url could deal with dynamic content, or you could upload jupyter notebook that will be used for that incident.

Optionally, it could make a sound on your laptop PC.


````
- tested on centos7
$ sudo pip install flask requests netifaces
$ cd /var/tmp && git clone https://github.com/tnaganawa/open-alert-url.git
$ cd open-alert-url && ./index.py
````
