#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Main Flask file
"""
import time
import os
from flask import Flask, redirect, render_template, request, session, url_for, send_from_directory
from handler import Handler
app = Flask(__name__)
hand = Handler()
@app.route("/")
def main():
    """ Secret route """
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=["POST", "GET"])
def login():
    """ login route """
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


@app.route('/test', methods=["POST", "GET"])
def test():
    """ Test route """
    if 'username' in session:
        if request.method == "POST":
            if request.form['btn'] == 'create':
                name = request.form['name']
                name = str(name)
                name.strip()
                if len(name) - name.count(' ') > 2:
                    hand.create(hand.cleanse(name), "test")
                    session['testID'] = hand.ID("test")
                    return redirect(url_for('question'))
                else:
                    return render_template("test.html", test_table=hand.table("test"), error=True)
        if request.method == "GET":
            delete = request.args.get("del")
            if delete != None:
                hand.remove(delete, "test")

            edit = request.args.get("edit")
            if edit != None:
                session['testID'] = edit
                return redirect(url_for('question'))
        return render_template("test.html", test_table=hand.table("test"))
    return redirect(url_for('login'))

@app.route('/test/new', methods=["POST", "GET"])
def question():
    """working with new test"""
    if 'username' in session:
        if session.get('testID'):
            if request.method == "POST":
                if request.form['btn'] == 'create':
                    question = request.form['question']
                    question.strip()
                    if len(question) > 2:
                        hand.create(hand.cleanse(question), "question", session['testID'])
                        session['questionID'] = hand.ID("question")
                        return redirect(url_for('answer'))
                    else:
                        return render_template("question.html", test_name=hand.name("question", session['testID']), question_table=hand.table("question", session['testID']), error=True)
                if request.form['btn'] == 'return':
                    return redirect(url_for('test'))

            if request.method == "GET":
                delete = request.args.get("del")
                if delete != None:
                    hand.remove(delete, "question")
                edit = request.args.get("edit")
                if edit != None:
                    session['questionID'] = edit
                    return redirect(url_for('answer'))
            return render_template("question.html", test_name=hand.name("question", session['testID']), question_table=hand.table("question", session['testID']))
        else:
            return redirect(url_for('test'))
    return redirect(url_for('login'))
@app.route('/test/new/answer', methods=["POST", "GET"])
def answer():
    """working with new test"""
    if 'username' in session:
        if session.get('questionID'):
            if request.method == "POST":
                if request.form['btn'] == 'create':
                    answer = request.form['answer']
                    selected = request.form.getlist('check')
                    selected = bool(selected)
                    if selected:
                        selected = "checked"
                    else:
                        selected = ""
                    answer.strip()
                    if len(answer) > 1:
                        hand.create(hand.cleanse(answer), "answer", session['questionID'], selected)
                        session['questionID'] = hand.ID("question")
                        return redirect(url_for('answer'))
                    else:
                        return render_template("answer.html", question_name=hand.name("answer", session['questionID']), answer_table=hand.table("answer", session['questionID']), error=True)
                if request.form['btn'] == 'return':
                    return redirect(url_for('question'))

            if request.method == "GET":
                delete = request.args.get("del")
                if delete != None:
                    hand.remove(delete, "answer")
            return render_template("answer.html", question_name=hand.name("answer", session['questionID']), answer_table=hand.table("answer", session['questionID']))
        else:
            return redirect(url_for('test'))
    return redirect(url_for('login'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#app.secret_key = os.urandom(24)
app.secret_key = "mysecretkey"
if __name__ == "__main__":
    app.debug = True
    app.run()
