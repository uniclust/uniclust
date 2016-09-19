#!/usr/bin/env python
from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/jobs", methods=["GET"])
def jobs_action():
    if request.method == "GET":
        return "GETED"

@app.route("/job/<jobid>", methods=["GET", "POST", "DELETE"])
def job_action(jobid):
    if request.method == "POST":
        return "POSTED"
    elif request.method == "GET":
        return "GETED"
    elif request.method == "DELETE":
        return "DELETED"

@app.route("/apps", methods=["GET"])
def apps_action():
    if request.method == "GET":
        return "GETED"

@app.route("/app/<appid>", methods=["GET"])
def app_action(appid):
    if request.method == "GET":
        return "GETED"

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
