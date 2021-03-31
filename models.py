from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, MetaData
from sqlalchemy.orm import relationship

from database import Base, engine

metadata = MetaData(engine)


class Car(Base):
    # 定义表名
    __tablename__ = "car"
    # 定义字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    carno = Column(String(15), index=True, )
    owner = Column(String(20), index=True, )
    brand = Column(String(20))

    records = relationship('Record', back_populates='car')


class Record(Base):
    # 定义表名
    __tablename__ = "record"
    # 定义字段
    id = Column(Integer, primary_key=True, autoincrement=True)
    reason = Column(String(255))
    makedate = Column(Date)
    punish = Column(String(255))
    dealt = Column(Boolean, default=False)
    car_id = Column(Integer, ForeignKey('car.id'))

    car = relationship("Car", back_populates="records")
