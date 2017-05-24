#!/usr/bin/python
import json
import requests
from flask import Flask, render_template, request
app = Flask(__name__)



###
jupyter_url='http://127.0.0.1:8888'
alertfile='alertfile.txt'
basepath='/var/tmp/open-pager-url/'
notebookdir=basepath+'notebooks/'
alert_to_notebook={
 "jupyter-upload-test" : "jupyter-upload.ipynb"
}
alert_to_url={
 "test-alert" : "http://www.google.co.jp"
}
#
# override settings if local_settings.py is there
try:
 from local_settings import *
except ImportError as e:
 pass
###
# $ echo "test-alert" >> alertfile.txt
# $ echo "jupyter-upload-test" >> alertfile.txt
###

@app.route("/")
def index():
    # read alertfile
    alerts=[]
    with open(alertfile) as f:
     tmp=f.read()
     if (len(tmp)==0):
      pass
     else:
      alerts=tmp.split('\n')
      if ('' in alerts):
       alerts.remove('')

    # null clear alertfile
    with open(alertfile, 'w') as f:
     f.write('')

    # create urllist
    urls=[]
    for alert in alerts:
     if (alert in alert_to_url):
      urls.append(alert_to_url[alert])
     elif (alert in alert_to_notebook):
      notebookname=alert_to_notebook[alert]
      notebookpath=notebookdir+notebookname
      with open(notebookpath) as f:
       notebook_content = json.load(f)
       notebook = {"content": notebook_content}
       return_value=requests.put(jupyter_url+'/api/contents/{0}'.format(notebookname), data=json.dumps(notebook))
       if (199 < return_value.status_code < 299):
        urls.append('{0}/notebooks/{1}'.format(jupyter_url, notebookname))
     else:
      #print ("No such alert: {0}", alert)
      my_url=request.url
      urls.append("{0}nosuchalert/{1}".format(my_url, alert))
    return render_template("index.html", urls=urls)

@app.route("/nosuchalert/<alertname>")
def nosuchalert(alertname):
 return ("HTTP 200 No Such Alert: {0}".format(alertname))

@app.route("/alertmanager", methods=["POST"])
def alertmanager():
 """
 to test this:
 $ curl -H "Content-Type: application/json" -d '[{"labels":{"alertname":"test-alert"}}]' 172.17.0.2:9093/api/v1/alerts
 or
 $ curl -H "Content-Type: application/json" -d '{"alerts":[{"labels":{"alertname":"test-alert"}}]}' 127.0.0.1:5000/alertmanager
 """
 alert_json=request.get_json()
 #print (alert["alerts"])
 with open(alertfile, 'a') as f:
  for alert in alert_json["alerts"]:
   f.write(alert["labels"]["alertname"])
   f.write('\n')
 return ("HTTP 200 received")


if __name__ == "__main__":
    app.run()
