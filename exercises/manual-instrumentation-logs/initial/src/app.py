# pyright: reportMissingTypeStubs=false, reportUnknownParameterType=false, reportMissingParameterType=false, reportUnknownArgumentType=false, reportUnknownMemberType=false, reportAttributeAccessIssue=false

import time

import requests
from client import ChaosClient, FakerClient
from flask import Flask, make_response
import logging
from logging_utils import handler
from trace_utils import create_tracer
from opentelemetry import trace as trace_api


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s",
    )

logger = logging.getLogger()
logger.addHandler(handler)

# global variables
app = Flask(__name__)
tracer = create_tracer("app.py", "0.1")

@app.route("/users", methods=["GET"])
def get_user():
    user, status = db.get_user(123)
    logging.info(f"Found user {user!s} with status {status}")
    data = {}
    if user is not None:
        data = {"id": user.id, "name": user.name, "address": user.address}
    else:
        logging.warning(f"Could not find user with id {123}")
        logging.debug(f"Collected data is {data}")
    response = make_response(data, status)
    return response

@tracer.start_as_current_span("do_stuff")
def do_stuff():
    time.sleep(0.1)
    url = "http://localhost:6000/"
    response = requests.get(url)
    return response


@app.route("/")
@tracer.start_as_current_span("index")
def index():
    span = trace_api.get_current_span()
    logging.info("Info from the index function")
    do_stuff()
    current_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
    return f"Hello, World! It's currently {current_time}"


if __name__ == "__main__":
    db = ChaosClient(client=FakerClient())
    app.run(host="0.0.0.0", debug=True, port=5001)
