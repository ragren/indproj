#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""main handler file"""
from test import Test
from question import Question
from answer import Answer
from link import Link
import re
import string
import random
from flask import request
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
engine = create_engine("sqlite:///db/database.sqlite")
Session = sessionmaker(bind=engine)
session = Session()

class Handler():
    """Creates a new results instance"""
    def cleanse(self, mytext):
        nstr = re.sub(r'[|$|;|>|<|]',r' ',mytext)
        return nstr


    def getQuestion(self, code):
        myLink = session.query(Link).filter(Link.code == code).first()
        myTest = session.query(Test).filter(Test.id == myLink.testID).first()
        myQuestions = session.query(Question).filter(Question.testID == myLink.testID).all()
        progress = myLink.progress
        if progress < myTest.questions:
            question = myQuestions[progress]
        else:
            return False

        end = myTest.questions
        return [question.text, progress + 1, end, question.id]
    def getAnswers(self, questionID):
        myAnswers = session.query(Answer).filter(Answer.questionID == questionID).all()
        return myAnswers
    def checkAnswer(self, code, userAnswer):
        myLink = session.query(Link).filter(Link.code == code).first()
        myAnswer = session.query(Answer).filter(Answer.id == userAnswer).first()
        if myAnswer.correct == "checked":
            myLink.points = myLink.points + 1
        myLink.progress = myLink.progress + 1
        session.commit()

    def create(self, name, version, testID=0, correct=0):
        """creates new"""
        if version == "test":
            new = Test(
                name=name,
                questions=0
                )
        if version == "question":
            new = Question(
                text=name,
                answers=0,
                testID=testID
                )
            test = session.query(Test).filter(Test.id == testID).first()
            test.questions = test.questions + 1
        if version == "answer":
            new = Answer(
                sentence=name,
                correct=correct,
                questionID=testID
                )
            question = session.query(Question).filter(Question.id == testID).first()
            question.answers = question.answers + 1
        if version == "link":
            new = Link(
                name=name,
                testID=testID,
                points=0,
                progress=0,
                code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
                )

        session.add(new)
        session.commit()

    def ID(self, version):
        """retrieve latest id"""
        highest = 0
        if version == "test":
            all_ID = session.query(Test).all()
        if version == "question":
            all_ID = session.query(Question).all()
        if version == "answer":
            all_ID = session.query(Answer).all()
        for ID in all_ID:
            if ID.id > highest:
                highest = ID.id

        return highest

    def name(self, version, testID):
        """retrieve name"""
        if version == "question":
            name = session.query(Test).filter(Test.id == testID).first()
            return name.name
        if version == "answer":
            name = session.query(Question).filter(Question.id == testID).first()
            return name.text




    def remove(self, remove, version):
        """removes mission"""
        if version == "test":
            group = session.query(Question).filter(Question.testID == remove).all()
            for single in group:
                session.query(Answer).filter(Answer.questionID == single.id).delete()
            session.query(Test).filter(Test.id == remove).delete()
            session.query(Question).filter(Question.testID == remove).delete()
            session.query(Link).filter(Link.testID == remove).delete()
        if version == "question":
            question = session.query(Question).filter(Question.id == remove).first()
            question = question.testID
            test = session.query(Test).filter(Test.id == question).first()
            test.questions = test.questions - 1

            session.query(Question).filter(Question.id == remove).delete()
            session.query(Answer).filter(Answer.questionID == remove).delete()
        if version == "answer":
            answer = session.query(Answer).filter(Answer.id == remove).first()
            answer = answer.questionID
            question = session.query(Question).filter(Question.id == answer).first()
            question.answers = question.answers - 1
            session.query(Answer).filter(Answer.id == remove).delete()
        if version == "link":
            session.query(Link).filter(Link.id == remove).delete()
        session.commit()

    def validate(self, username):
        check = session.query(Link).filter(Link.code == username).all()
        if check:
            return True

    def table(self, version, testID=0):
        table = ""
        if version == "test":
            group = session.query(Test).all()
            for single in group:
                table += """<tr>

                            <td style="display:none;">{id}</td>
                                        <td><a class="btn btn-default glyphicon glyphicon-ok" href='?use={id}'></a><td><a class="btn btn-default glyphicon glyphicon-pencil" href='?edit={id}'></a></td><td class="main">{name}</td><td>{questions}</td>
                                        <td><a class="btn btn-default glyphicon glyphicon-remove" href='?del={id}'></a></td>
                                        </tr>""".format(id=single.id, name=single.name, questions=single.questions)

        if version == "link":
            group = session.query(Link).filter(Link.testID == testID).all()
            value = session.query(Test).filter(Test.id == testID).first()
            for single in group:
                table += """<tr>

                            <td style="display:none;">{id}</td>
                                        <td class="main">{name}</td><td>{points}/{total}</td><td><a href={link}>{link}</a></td>
                                        <td><a class="btn btn-default glyphicon glyphicon-remove" href='?del={id}'></a></td>
                                        </tr>""".format(id=single.id, name=single.name, points=single.points, total=value.questions, link=request.url_root + "en/" + single.code)

        if version == "question":
            group = session.query(Question).filter(Question.testID == testID).all()
            for single in group:
                table += """<tr>

                            <td style="display:none;">{id}</td>
                                        <td><a class="btn btn-default glyphicon glyphicon-pencil" href='?edit={id}'></a></td><td class="main">{text}</td>
                                        <td><a class="btn btn-default glyphicon glyphicon-remove" href='?del={id}'></a></td>
                                        </tr>""".format(id=single.id, text=single.text)

        if version == "answer":
            group = session.query(Answer).filter(Answer.questionID == testID).all()
            for single in group:
                table += """<tr>

                            <td style="display:none;">{id}</td>
                            <td class="main">{text}</td><td><input id="checkBox" type="checkbox" disabled="disabled" {correct}></td>
                                        <td><a class="btn btn-default glyphicon glyphicon-remove" href='?del={id}'></a></td>
                                        </tr>""".format(id=single.id, text=single.sentence, correct=single.correct)

        return table
