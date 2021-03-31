from typing import List, Optional

from pydantic import BaseModel
from pydantic.schema import date


class RecordBase(BaseModel):
    reason: str
    makedate: date
    punish: str
    car_id: int


class RecordCreate(RecordBase):
    pass


class CarBase(BaseModel):
    carno: str
    owner: str


class CarCreate(CarBase):
    brand: str


class Car(CarBase):
    id: int

    class Config:
        orm_mode = True


# 这里car实现外键数据的Car化
class Record(RecordBase):
    id: int
    car: Car
    dealt: bool

    class Config:
        orm_mode = True


# latest是查询后接口返回的数据格式，recods这里获取到的数据是一个列表
class Latest(BaseModel):
    count: int
    currpage: int
    nexturl: str
    preurl: str
    records: List[Record]

    class Config:
        orm_mode = True


class Dealt(BaseModel):
    code: int
    msg: str
