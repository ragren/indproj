#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""test file"""

from sqlalchemy import Column, String, Integer
from base import Base

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
