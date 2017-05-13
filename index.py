#!/usr/bin/python
from flask import Flask, render_template
app = Flask(__name__)

urlfile='urlfile.txt'
# $ echo "http://www.google.co.jp" >> urlfile.txt

@app.route("/")
def index():
    with open(urlfile) as f:
     tmp=f.read()
     if (len(tmp)==0):
      urls=[] 
     else:
      urls=tmp.split('\n')
    with open(urlfile, 'w') as f:
     f.write('')
    return render_template("index.html", urls=urls)

if __name__ == "__main__":
    app.run()
