from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from hous_app.db.models import HouseFeatures
from hous_app.db.schema import HouseFeaturesSchema
from hous_app.db.database import SessionLocal
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


house_router = APIRouter(prefix='/house', tags=['HouseFeatures'])

BASE_DIR = Path(__file__).resolve().parent.parent.parent

model_path = BASE_DIR / 'house_price_model.joblib'
scaler_path = BASE_DIR / 'scaler.pkl'

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@house_router.post('/', response_model=HouseFeaturesSchema)
async def create_house(house: HouseFeaturesSchema, db: Session = Depends(get_db)):
    db_house = HouseFeatures(**house.dict())
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house


@house_router.get('/', response_model=List[HouseFeaturesSchema])
async def house_list(db: Session = Depends(get_db)):
    return db.query(HouseFeatures).all()


@house_router.get('/{house_id}', response_model=HouseFeaturesSchema)
async def house_detail(house_id: int, db: Session = Depends(get_db)):
    house = db.query(HouseFeatures).filter(HouseFeatures.id == house_id).first()
    if house is None:
        raise HTTPException(status_code=404, detail='House not found')
    return house


@house_router.put('/{house_id}', response_model=HouseFeaturesSchema)
async def house_update(house_id: int, house: HouseFeaturesSchema, db: Session = Depends(get_db)):
    house_db = db.query(HouseFeatures).filter(HouseFeatures.id == house_id).first()
    if house_db is None:
        raise HTTPException(status_code=404, detail='House not found')

    for field, value in house.dict().items():
        setattr(house_db, field, value)

    db.commit()
    db.refresh(house_db)
    return house_db


@house_router.delete('/{house_id}')
async def house_delete(house_id: int, db: Session = Depends(get_db)):
    house_db = db.query(HouseFeatures).filter(HouseFeatures.id == house_id).first()
    if house_db is None:
        raise HTTPException(status_code=404, detail='House not found')

    db.delete(house_db)
    db.commit()
    return {'message': 'House deleted successfully'}


model_columns = [
   'GrLivArea',
   'YearBuilt',
   'GarageCars',
   'TotalBsmtSF',
   'FullBath',
   'OverallQual'
]


@house_router.post('/predict')
async def predict_price(house: HouseFeaturesSchema, db: Session = Depends(get_db)):
    input_data = {
        'GrLivArea': house.area,
        'YearBuilt': house.year,
        'GarageCars': house.garage,
        'TotalBsmtSF': house.total_basement,
        'FullBath': house.bath,
        'OverallQual': house.overall_quality
    }
    input_df = pd.DataFrame([input_data])

    scaled_array = scaler.transform(input_df)
    scaled_df = pd.DataFrame(scaled_array, columns=input_df.columns)

    predicted_price = model.predict(scaled_df)[0]
    return {'predicted_price': round(predicted_price)}



