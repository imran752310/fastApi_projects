from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel, Field
from typing import Annotated

class Patient(BaseModel):
    id : str
    name : str
    city: str
    gender : str
    address : str
    case : str


app = FastAPI()

def load_data():
    with open("patient.json") as f:
        data = json.load(f)
    return data

@app.get("/")
async def root():
    return {"Message" : "This is root method"}


@app.get("/patient")
async def view_patients():
    data = load_data()
    return data

@app.get("/patient/{p_id}")
async def view_patients(p_id: str):
   
    data = load_data()
   
    for patient in data:
        if patient["id"] == p_id:
            return patient
    return "not found"

def save_data(data):
    with open("patient.json","w") as f:
         json.dump(data,f, indent=4)
    



@app.post("/patient")
def add_patient(patient : Patient):

    data = load_data()

    #  if patient.id in data:
    #      raise HTTPException(status_code=400, detail="this patient is in record")
     
    #  data[patient.id] = patient.model_dump(exclude=["id"])

    data.append(patient.model_dump())
    save_data(data)
    return {"message": "Patient added successfully!", "patient": patient}
  