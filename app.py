#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
My first Flask app
"""
import time
import os
from flask import Flask, redirect, render_template, request, session, url_for, send_from_directory
app = Flask(__name__)
@app.route("/")
def main():
    """ Secret route """
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/login', methods=["POST", "GET"])
def login():
    """hej"""
    error = None
    if request.method == 'POST':
        if request.form['username'] != "admin" or request.form['password'] != "password":
            error = "Wrong username/password."
            time.sleep(2)
        else:
            session['username'] = request.form['username']
            return redirect(url_for('main'))

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """logging out with sessions"""
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


app.secret_key = os.urandom(24)

if __name__ == "__main__":
    app.debug = True
    app.run()
