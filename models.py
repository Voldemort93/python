__author__ = 'vladimir'
import logging
from sqlalchemy import Column, String, Text, Boolean, Enum, Integer
from db.backend import SQLAlchemyModelBase, Backend


class Ir_remote_record(SQLAlchemyModelBase):
    __tablename__ = 'remote_record'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    frequency = Column(Integer)
    period = Column(Integer)
    command = Column(Text)


class Ir_remote_add_id(SQLAlchemyModelBase):
    __tablename__ = 'remote_id_add'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    vendorId = Column(String)
    modelId = Column(String)


class Ir_remote_add_commands(SQLAlchemyModelBase):
    __tablename__ = 'remote_command_add'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    commands = Column(Text)

