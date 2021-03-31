from fastapi import Depends, FastAPI, HTTPException, Form, Request
from pydantic.schema import date
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

import crud
import models
import schemas
from database import SessionLocal, engine

from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount("/static", StaticFiles(directory="static"))


@app.get("/")
async def index(request: Request):
    """

    :param request:
    :return:
    """
    return FileResponse('./static/index.html')


@app.post("/api/create_car/", response_model=schemas.Car, name="添加车辆信息", description="添加车辆信息")
async def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    """

    :param car:
    :param db:
    :return:
    """
    # 判断carno是不是已经在数据库中
    db_car = crud.get_car_by_carno(db, carno=car.carno)
    if db_car:
        car=crud.read_car(db)
        raise HTTPException(status_code=400, detail="carno already registered")
    return crud.create_car(db=db, car=car)


@app.get("/api/car/carno", response_model=schemas.Car, name="获取车牌信息", description="获取车牌信息")
async def read_car(carno: str, db: Session = Depends(get_db)):
    """

    :param carno:
    :param db:
    :return:
    """
    db_car = crud.get_car(db, carno=carno)
    if db_car is None:
        raise HTTPException(status_code=404, detail="car not found")
    return db_car


@app.post("/api/create_record/", response_model=schemas.Record, name="添加车辆违章信息", description="添加车辆违章信息")
async def create_record_for_car(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    """

    :param record:
    :param db:
    :return:
    """
    return crud.create_car_record(db=db, record=record)


@app.get("/api/car/", name="获取车辆信息", description="获取所有车辆信息")
async def get_car(db: Session = Depends(get_db)):
    """

    :param db:
    :return:
    """
    car = crud.read_car(db)
    return car


@app.get("/api/record/", name="获取所有违章记录", description="获取所有违章记录", response_model=schemas.Latest)
async def get_all_record(page: int = 1, carno: str = None, start: date = None, end: date = None,
                         db: Session = Depends(get_db)):
    """
    :param page:
    :param carno:
    :param start:
    :param end:
    :param db:
    :return:
    """
    latest = crud.read_all_record(carno=carno, start=start, end=end, page=page, db=db)
    return latest


@app.patch("/api/record/{record_id}", name="update car record", description="处理违章记录", response_model=schemas.Dealt)
async def dealt_record(record_id: int, db: Session = Depends(get_db)):
    """
    :param record_id:
    :param db:
    :return:
    """
    dealt = crud.update_dealt(db=db, record_id=record_id)
    return dealt


@app.delete("/api/record/{record_id}", name="del car record", description="删除违章记录", response_model=schemas.Dealt)
async def dealt_record(record_id: int, db: Session = Depends(get_db)):
    """
    :param record_id:
    :param db:
    :return:
    """
    dealt = crud.del_record(db=db, record_id=record_id)
    return dealt


if __name__ == '__main__':
    import uvicorn

    # uvicorn main: app --reload
    uvicorn.run(app, host='127.0.0.1', port=8000)
