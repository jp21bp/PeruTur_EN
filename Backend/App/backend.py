"""
Este archivo es el backend
Servira las predicciones del modelo
"""

#### Import libraries
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib, os, uvicorn

#### Read model pipeline and scaler
try:
    pipeline = joblib.load('App/pipeline.pkl')
    scaler = joblib.load('App/scaler.pkl')
except Exception as e:
    raise RuntimeError(f'Loading error: {e}')

#### Initialize API
app = FastAPI(title='Model API')

#### CORS
origins = [
    "http://localhost:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#### Setup data entry validation
class DataInput(BaseModel):
    month: int
    region: str
    name: str

#### API endpoints
@app.get('/')
def homepage():
    return {'home': 'page'}

@app.post('/predict')
def predict(data: DataInput):
    try:
        input = [[data.month, data.region, data.name]]
        prediction_norm = pipeline.predict(input)
        prediction = scaler.inverse_transform(
            prediction_norm.reshape(1,-1)
        )
        return {'prediction': f'{int(prediction[0][0])}'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)







