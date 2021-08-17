from flask import Flask, render_template
from flask import request
import json
import threading
from time import sleep


"""
This file facilitates the Flask backend routes and the interfacing with the pref_db json files to save new preferences.
"""


def synchronized(func):
    """
    Allows for the synchronization of functions that interface with the json database files. Necessary when multiple
    users may be giving feedback at once, since reading and writing to the database can take some time.
    """
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)
    return synced_func


@synchronized
def begin_save(pref_db, env):
    threading.Thread(target=save_pref_db, args=[pref_db, env]).start()


@synchronized
def add_pref(pref, prefs):
    prefs.append(pref)

@synchronized
def save_pref_db(pref_db, env):
    """
    Saves the given pref_db list into the pref_db file for the specified environment.
    """
    with open("preferences/"+env+'/pref_db.json', 'r') as json_file:
        try:
            old_pref_db = json.load(json_file)
        except Exception as e:
            raise e
        with open("preferences/" + env + '/pref_db.json', 'w') as json_file:
            old_pref_db.extend(pref_db)
            json.dump(old_pref_db, json_file)


def get_pref_db(env):
    """
    Pulls the appropriate pref_db file for the specified environment. Returns as a python list of the db
    """
    with open("preferences/"+env+"/pref_db.json", 'r') as f:
        try:
            pref_db = json.load(f)
        except Exception as e:
            raise e
        return pref_db if len(pref_db) > 0 else None


def get_webapp():
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
        new_email = False
        while not new_email:
            with open('data/email.json', 'r') as f:
                email = json.load(f)
            if len(email) > 0:
                return json.dumps(email)
            else:
                sleep(0.25)

    # called when a new feedback is submitted
    @app.route('/feedback', methods=['POST'])
    def update_text():
        user_feedback = request.json

        with open('data/feedback.json', 'w') as f:
            json.dump(user_feedback, f)

        return get_email()

    return app
