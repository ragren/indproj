#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Main file for creating python objects"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Test(Base):
    """creates new test object"""

    __tablename__ = "tests"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    questions = Column(Integer)

    def __init__(self, name, questions):
        """ init method """
        self.name = name
        self.questions = questions

class Question(Base):
    """creates new question object"""

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    answers = Column(Integer)
    testID = Column(Integer)

    def __init__(self, text, answers, testID):
        """ init method """
        self.text = text
        self.answers = answers
        self.testID = testID

class Answer(Base):
    """creates new answer object"""

    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    sentence = Column(String)
    correct = Column(String)
    questionID = Column(Integer)
    def __init__(self, sentence, correct, questionID):
        """ init method """
        self.sentence = sentence
        self.correct = correct
        self.questionID = questionID

class Link(Base):
    """creates new link object"""

    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    testID = Column(Integer)
    points = Column(Integer)
    progress = Column(Integer)
    code = Column(String)

    def __init__(self, name, testID, points, progress, code):
        """ init method """
        self.name = name
        self.testID = testID
        self.points = points
        self.progress = progress
        self.code = code
