#!/usr/bin/python
# coding:utf-8
import os
from datetime import datetime

from sqlalchemy import Column, Integer, String, create_engine, DateTime, JSON
from sqlalchemy.orm import declarative_base

base_dir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine(f'sqlite:///{os.path.join(base_dir, "../db.sqlite")}')
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False, unique=True)
    chat_id = Column(Integer, nullable=False, unique=True)
    username = Column(String(64), nullable=True)
    first_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)
    last_interaction = Column(DateTime, nullable=False, default=datetime.now)
    first_seen = Column(DateTime, nullable=False, default=datetime.now)
    current_dialog_id = Column(Integer, nullable=True, default=None)
    current_chat_mode = Column(String(64), nullable=True, default='assistant')
    n_used_tokens = Column(Integer, nullable=False, default=0)


class Dialog(Base):
    __tablename__ = 'dialog'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dialog_id = Column(String(32), nullable=False, unique=True)
    user_id = Column(Integer, nullable=False)
    chat_mode = Column(String(64), nullable=False, default='assistant')
    start_time = Column(DateTime, nullable=False, default=datetime.now)
    messages = Column(JSON(), nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # Base.metadata.drop_all(engine)
