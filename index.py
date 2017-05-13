#!/usr/bin/python
import json
import requests
from flask import Flask, render_template
app = Flask(__name__)



###
jupyter_url='http://127.0.0.1:8888'
alertfile='urlfile.txt'
basepath='/var/tmp/open-alert-url/'
notebookdir=basepath+'notebooks/'
###
# $ echo "test-alert" >> urlfile.txt
# $ echo "jupyter-upload-test" >> urlfile.txt

alert_to_notebook={
 "jupyter-upload-test" : "jupyter-upload.ipynb"
}
alert_to_url={
 "test-alert" : "http://www.google.co.jp"
}

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
       #print (return_value)
       #print (return_value.content)
       if (199 < return_value.status_code < 299):
        urls.append('{0}/notebooks/{1}'.format(jupyter_url, notebookname))
     else:
      print ("No such alert: {0}", alert)
    return render_template("index.html", urls=urls)

if __name__ == "__main__":
    app.run()
