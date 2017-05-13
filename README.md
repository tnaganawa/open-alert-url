when an alert is found,  
you have to open some url, which contains information to deal with that alert.

This script will open that for you.

It also give some variables extracted from the alert to opened url, if opened url could deal with dynamic content. 

Optionally, it could make a sound on your laptop PC.


````
- tested on centos7
sudo pip install flask
cd /var/tmp && git clone https://github.com/tnaganawa/open-alert-url.git
cd open-alert-url && ./index.py
````
