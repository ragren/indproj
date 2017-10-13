#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""link file"""

from sqlalchemy import Column, String, Integer
from base import Base

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
