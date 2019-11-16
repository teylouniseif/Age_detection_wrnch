# Mcgill hackathon : Detect land conditions through satellite imagery with a single click.

import json
import requests
import logging
import reverse_geocoder
import requests
from requests.auth import HTTPBasicAuth
import glob, os
from subprocess import Popen
import cv2
import numpy as np
import time
from wrcloud.wrcloud import wrCloud

from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request

app = Flask(__name__, static_url_path='')

@app.route("/", methods=['GET', 'POST'])
def root():
    return app.send_static_file('index.html')

@app.route('/reverse_geocode', methods=['POST'])
def get_reverse_geocode():
    try:
        pass
    except Exception:
        return jsonify({"response" : "Bad request!"}), 400

    return json.dumps(None), 200

@app.route('/coordinates', methods=['POST'])
def get_images():
    try:
        callWrench()
    except Exception:
        return jsonify({"response" : "Bad request!"}), 400

    return json.dumps(None), 200

def callWrench():

    ###########################################################################
    wrcloud=wrCloud(api_key='e5abf918-55bd-4d96-a99d-4bd7ad00f244')
    wrcloud.get_auth_token()
    job_id=wrcloud.submit_job(
        "test.jpg",
        work_type=["annotated_media", "json"],
        options={'heads': True, 'est_3d': False, 'resolution_scale': 1}
      )
    wrcloud.wait_for_processed_job(job_id)
    print(wrcloud.get_job_status(job_id))
    wrcloud.is_job_processed(job_id)
    wrcloud.is_job_successful(job_id)
    wrcloud.download_job(
        job_id=job_id,
        output="output.zip",
        work_type=""
    )

    return json.dumps(None)

if __name__ == '__main__':
    handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="127.0.0.1",port=5009)
