#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""question file"""

from sqlalchemy import Column, String, Integer
from base import Base

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
