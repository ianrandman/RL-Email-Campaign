from flask import Flask, render_template
from flask import request
import json
import threading
from time import sleep


def get_webapp(env):
    app = Flask(__name__)

    ####################################################################################
    # PAGE ROUTES

    @app.route("/")
    def main():
        return render_template('env.html')

    ####################################################################################
    # API ROUTES

    # called to generate a new email for feedback
    @app.route("/getemail")
    def get_email():
        while env.email is None:
            sleep(0.1)
        return json.dumps({'email': env.email})

    # called when a new feedback is submitted
    @app.route('/feedback', methods=['POST'])
    def update_text():
        user_feedback = request.json
        env.human_feedback = user_feedback['feedback']

        return get_email()

    return app
