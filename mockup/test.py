#!/usr/bin/env python
import sys, os, subprocess
args = sys.argv

def main():
    exit_code = subprocess.call(["./test.sh"])
    if exit_code != 0:
        print("FAILED")
        sys.exit(exit_code)
    print("PASSED", exit_code)
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    main()
    return "<p>Hello, World!</p>"

main()
