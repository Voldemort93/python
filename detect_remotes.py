# coding=utf-8
import base64
import zlib
import json
from sqlalchemy import Column, ForeignKey, Integer, String
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Tables:
    def __init__(self):
        pass

    class CommandCode(Base):
        __tablename__ = 'codes'
        _id = Column(Integer, primary_key=True, nullable=False)
        codedata = Column(String, nullable=False)

        def __init__(self, **kwargs):
            self.__periodTolerance = kwargs.get('periodTolerance')
            self.__frame = kwargs.get('frame')
            self.__frequency = kwargs.get('frequency')
            self.__period = kwargs.get('period')
            self.__repeatCount = kwargs.get('repeatCount')

        @sqlalchemy.orm.reconstructor
        def initialize(self):
            coded = base64.b64decode(self.codedata)
            data = json.loads(zlib.decompress(coded))
            self.__periodTolerance = data['periodTolerance']
            self.__frame = data['frame']
            self.__frequency = data['frequency']
            self.__period = data['period']
            self.__repeatCount = data['repeatCount']

        @property
        def frame(self):
            return self.__frame

        @property
        def frequency(self):
            return self.__frequency

        @property
        def period(self):
            return self.__period

        @property
        def periodTolerance(self):
            return self.__periodTolerance

        @property
        def repeatCount(self):
            return self.__repeatCount

        def __cmp__(self, other):
            global result
            assert isinstance(other, Tables.CommandCode)
            if self.frame is not None:
                # in Command Code is only frame
                if self.period is None and self.frequency is None and self.periodTolerance is None and \
                                self.repeatCount is None:
                    result = cmp((self.frame,), (other.frame,))

                # in Command Code is frame and one of the other parameters
                elif self.period is not None and self.frequency is None and self.periodTolerance is None and \
                                self.repeatCount is None:
                    result = cmp((self.frame, self.period),
                                 (other.frame, other.period))
                elif self.period is None and self.frequency is not None and self.periodTolerance is None and \
                                self.repeatCount is None:
                    result = cmp((self.frame, self.frequency),
                                 (other.frame, other.frequency))
                elif self.period is None and self.frequency is None and self.periodTolerance is not None and \
                                self.repeatCount is None:
                    result = cmp((self.frame, self.periodTolerance),
                                 (other.frame, other.periodTolerance))
                elif self.period is None and self.frequency is None and self.periodTolerance is None and \
                                self.repeatCount is not None:
                    result = cmp((self.frame, self.repeatCount),
                                 (other.frame, other.repeatCount))

                # in Command Code is frame and two of the other parameters
                elif self.period is not None and self.frequency is not None and self.periodTolerance is None and \
                                self.repeatCount is None:
                    result = cmp((self.frame, self.period, self.frequency),
                                 (other.frame, other.period, other.frequency))
                elif self.period is not None and self.frequency is None and self.periodTolerance is not None and \
                                self.repeatCount is None:
                    result = cmp((self.frame, self.period, self.periodTolerance),
                                 (other.frame, other.period, other.periodTolerance))
                elif self.period is not None and self.frequency is None and self.periodTolerance is None and \
                                self.repeatCount is not None:
                    result = cmp((self.frame, self.period, self.repeatCount),
                                 (other.frame, other.period, other.repeatCount))
                elif self.period is None and self.frequency is not None and self.periodTolerance is not None and \
                                self.repeatCount is None:
                    result = cmp((self.frame, self.frequency, self.periodTolerance),
                                 (other.frame, other.frequency, other.periodTolerance))
                elif self.period is None and self.frequency is not None and self.periodTolerance is None and \
                                self.repeatCount is not None:
                    result = cmp((self.frame, self.frequency, self.repeatCount),
                                 (other.frame, other.frequency, other.repeatCount))
                elif self.period is None and self.frequency is None and self.periodTolerance is not None and \
                                self.repeatCount is not None:
                    result = cmp((self.frame, self.periodTolerance, self.repeatCount),
                                 (other.frame, other.periodTolerance, other.repeatCount))

                # in Command Code is frame and two of the other parameters
                elif self.period is not None and self.frequency is not None and self.periodTolerance is not None and \
                                self.repeatCount is None:
                    result = cmp((self.frame, self.period, self.frequency, self.periodTolerance),
                                 (other.frame, other.period, other.frequency, other.periodTolerance))
                elif self.period is not None and self.frequency is not None and self.periodTolerance is None and \
                                self.repeatCount is not None:
                    result = cmp((self.frame, self.period, self.frequency, self.repeatCount),
                                 (other.frame, other.period, other.frequency, other.repeatCount))

                # in Command Code are all parameters
                else:
                    result = cmp(
                        (self.frame, self.period, self.frequency, self.periodTolerance, self.repeatCount,),
                        (other.frame, other.period, other.frequency, other.periodTolerance, other.repeatCount,))
            return result

        def __repr__(self):
            return "period: {}, freq: {}, frame: {}, periodTolerance: {}, repeatCount: {}".format(self.__period,
                                                                                                  self.__frequency,
                                                                                                  self.__frame,
                                                                                                  self.__periodTolerance,
                                                                                                  self.__repeatCount)

    class CodeAllocation(Base):
        __tablename__ = 'codeallocations'
        # columns
        _id = Column(Integer, nullable=False, primary_key=True)
        model_id = Column(Integer, ForeignKey('models._id'), nullable=False)
        code_id = Column(Integer, ForeignKey('codes._id'), nullable=False)
        codetype_id = Column(Integer, ForeignKey('codetypes._id'), nullable=False)
        model = relationship('Model')

    class Model(Base):
        __tablename__ = 'models'
        # columns
        _id = Column(Integer, nullable=False, primary_key=True)
        vendor_id = Column(Integer, ForeignKey('vendors._id'), nullable=False)
        devicetype_id = Column(Integer, nullable=False)
        name = Column(String, nullable=False)
        vendor = relationship('Vendor')

        def __repr__(self):
            return "(Model: vendor: {}, name: {})".format(self.vendor_id, self.name)

    class Vendor(Base):
        __tablename__ = 'vendors'
        # columns
        _id = Column(Integer, nullable=False, primary_key=True)
        name = Column(String, nullable=False)

    class CodeType(Base):
        __tablename__ = 'codetypes'
        # columns
        _id = Column(Integer, nullable=False, primary_key=True)
        name = Column(String, nullable=False)

    class CodeTypeMapping(Base):
        __tablename__ = 'codetypesmapping'
        # columns
        _id = Column(Integer, nullable=False, primary_key=True)
        devicetypes_id = Column(Integer, ForeignKey('devicetypes._id'), nullable=False)
        codetype_id = Column(Integer, ForeignKey('codetypes._id'), nullable=False)

    class DeviceType(Base):
        __tablename__ = 'devicetypes'
        # columns
        _id = Column(Integer, nullable=False, primary_key=True)
        name = Column(String, nullable=False)


class Connection:
    def __init__(self):
        pass

    engine = create_engine('sqlite:///otrta.sqldb')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

class Detector:
    def __init__(self, connection):
        self.connection = connection

    def detect(self, command_codes):
        """
        Detects an IR remote model by one or more of its commands.
        :param command_codes: a list of IrCommand-s recorded from somewhere
        :type command_codes: IrCommand
        :return: A list of IrRemotes matching these ir_commands.
        :rtype: IrRemote
        """

        return self.__find_models(1, command_codes)

    def __find_models(self, device_type, command_codes):
        all_devices = self.connection.session.query(
            Tables.CommandCode, Tables.CodeAllocation, Tables.Model,
        ).join(
            Tables.CodeAllocation
        ).join(
            Tables.Model
        ).filter(Tables.Model.devicetype_id == device_type).all()

        result = []
        for command_code, code_alloc, model in all_devices:
            first_command = command_codes[0]
            if first_command == command_code:
                result.append(model)

        return result

#
# class CheckBtnPower:
#    def __init__(self):
#        pass
#
#    @staticmethod
#    def find_one_command(button_id=1, device_type_id=1):
#        # #########################################
#        # 1st filter: only button POWER
#        # 2nd filter: only device TV
#        # result    : all TV's with button power
#        # #########################################
#        opensession = Connection()
#        power_tuple = opensession.session.query(Tables.CodeAllocation, Tables.Model,
#                                                Tables.Vendor,
#                                                Tables.CodeType).join(Tables.Model).join(
#            Tables.Vendor).join(
#            Tables.CodeType) \
#            .filter(Tables.CodeAllocation.codetype_id == button_id) \
#            .filter(Tables.Model.devicetype_id == device_type_id) \
#            .first()
#
#        # onlyOneButton = power_btn.find_one_button(1, 1)
#        # print onlyOneButton.Vendors.name, onlyOneButton.Models.name
#
#        # return power_tuple.Vendors.name, power_tuple.Models.name
#        return power_tuple
#
#    def find_all_commands(self, button_id=1, device_id=1):
#        all_power_id = openSession.session.query(Tables.CodeAllocation, Tables.Model,
#                                                 Tables.Vendor,
#                                                 Tables.CodeType).join(Tables.Model).join(Tables.Vendor).join(
#            Tables.CodeType) \
#            .filter(Tables.CodeAllocation.codetype_id == button_id) \
#            .filter(Tables.Model.devicetype_id == device_id) \
#            .all()
#
#        return all_power_id


#
# class DecodedFrame:
# def __init__(self, POWER_ID, DEVICE_TV):
# self.DEVICE_TV = DEVICE_TV
# self.POWER_ID = POWER_ID
#
#
# def printing_results(self):
# power = CheckBtnPower()
# allocations = power.find_button(1, 1)
# for alloc, model, vend, command in allocations:
# print alloc.code_id, vend.name, model.name, command.name
# codes_table = openSession.session.query(Tables.CommandCode).all()
# for code in codes_table:
# if code._id == alloc.code_id:
# coded = base64.b64decode(code.codedata)
# decoded = json.loads(zlib.decompress(coded))
# print "codedata: {}".format(decoded)
# return decoded
#
# # frame = DecodedFrame(1, 1)
# #frame.printing_results()

if __name__ == '__main__':
    # logging.basicConfig()
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    openSession = Connection()

    #POWER_ID = 1
    #DEVICE_TV = 1
    #power_btn = CheckBtnPower()
#
#onlyOneButton = power_btn.find_one_command(1, 1)
## print onlyOneButton
#allocations = power_btn.find_all_commands(1, 1)
