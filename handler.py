#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""main handler file"""
import re
from flask import request
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
engine = create_engine("sqlite:///db/database.sqlite")
Session = sessionmaker(bind=engine)
session = Session()
from test import Test
from question import Question
from answer import Answer

class Handler():
    """Creates a new results instance"""
    def cleanse(self, mytext):
        nstr = re.sub(r'[|$|;|>|<|]',r' ',mytext)
        return nstr

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
        session.commit()


    def table(self, version, testID=0):
        table = ""
        if version == "test":
            group = session.query(Test).all()
            for single in group:
                table += """<tr>

                            <td style="display:none;">{id}</td>
                                        <td><a class="btn btn-default" href='?edit={id}'>edit</a></td><td class="main">{name}</td><td>{questions}</td>
                                        <td><a class="btn btn-default" href='?del={id}'>delete</a></td>
                                        </tr>""".format(id=single.id, name=single.name, questions=single.questions)

        if version == "question":
            group = session.query(Question).filter(Question.testID == testID).all()
            for single in group:
                table += """<tr>

                            <td style="display:none;">{id}</td>
                                        <td><a class="btn btn-default" href='?edit={id}'>edit</a></td><td class="main">{text}</td>
                                        <td><a class="btn btn-default" href='?del={id}'>delete</a></td>
                                        </tr>""".format(id=single.id, text=single.text)

        if version == "answer":
            group = session.query(Answer).filter(Answer.questionID == testID).all()
            for single in group:
                table += """<tr>

                            <td style="display:none;">{id}</td>
                            <td class="main">{text}</td><td><input id="checkBox" type="checkbox" disabled="disabled" {correct}></td>
                                        <td><a class="btn btn-default" href='?del={id}'>delete</a></td>
                                        </tr>""".format(id=single.id, text=single.sentence, correct=single.correct)

        return table
