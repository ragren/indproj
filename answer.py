#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""answer file"""

from sqlalchemy import Column, String, Integer
from base import Base

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
