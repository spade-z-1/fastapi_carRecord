from typing import List, Any

from pydantic.schema import date
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

import pagnation

from models import Car, Record
import schemas

PAGE_SIZE = 5


def get_car_by_carno(db: Session, carno: str):
    """

    :param db:
    :param carno:
    :return:
    """
    return db.query(Car).filter(Car.carno == carno).first()


def create_car(db: Session, car: schemas.CarCreate):
    """

    :param db:
    :param car:
    :return:
    """
    db_car = Car(owner=car.owner, carno=car.carno, brand=car.brand)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def create_car_record(db: Session, record: schemas.RecordCreate):
    """

    :param db:
    :param record:
    :return:
    """
    db_record = Record(
        reason=record.reason,
        makedate=record.makedate,
        punish=record.punish,
        car_no=record.car_no)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


# 查询所有车辆信息
def read_car(db: Session):
    """

    :param db:
    :return:
    """
    cars: List[Any] = db.query(Car).all()
    return cars


# 查询所有记录信息，不包含车辆信息
def read_search_record(db: Session):
    """
    :param db:
    :return:
    """
    return db.query(Record).all()


# 按照条件进行查询
def read_all_record(db: Session, carno: str = '', start: date = None, end: date = None, page: int = 1):
    """
    :param db:
    :param carno:
    :param start:
    :param end:
    :param page:
    :return:
    """
    url = "/api/record/?"
    records = db.query(Record)
    if carno:
        records = records.join(Car).filter(or_(
            Car.carno.like("%" + carno + "%"),
            Car.owner.like("%" + carno + "%")))
        url += f"carno={carno}&"
    if all([start, end]):
        records = records.filter(and_(Record.makedate <= end, Record.makedate >= start))
        url += f"start={start}&end={end}"
    count = int((len(records.all()) + PAGE_SIZE - 1) / PAGE_SIZE)
    if page:
        records = records.limit(PAGE_SIZE).offset((page - 1) * PAGE_SIZE)
    records = records.all()
    return pagnation.pagenation(records, url, page, count)


# 更新record中的 dealt字段为True
def update_dealt(db: Session, record_id: int):
    """
    :param db:
    :param record_id:
    :return:
    """
    try:
        record = db.query(Record).get(record_id)
        record.dealt = True
        db.add(record)
        db.commit()
        return {'code': 10000, 'msg': "Success update car's record "}
    except Exception as e:
        print(e)
    return {'code': 10001, 'msg': " Fail update car's record "}


# 删除一条已受理的record记录
def del_record(db: Session, record_id: int):
    """
    :param db:
    :param record_id:
    :return:
    """
    try:
        record = db.query(Record).get(record_id)
        if record.dealt:
            db.delete(record)
            db.commit()
            return {'code': 10000, 'msg': " Success del car's record "}
    except Exception as e:
        print(e)
    return {'code': 10001, 'msg': " Fail del car's record "}
