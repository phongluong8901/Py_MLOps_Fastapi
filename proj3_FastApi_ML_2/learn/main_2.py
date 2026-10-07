from pydantic import computed_field
from typing import Literal
from pydantic import Field
from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel
import json
from typing import Annotated

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='ID of the patient', example='PT-12345')] #dấu ... (Ellipsis) mang ý nghĩa định nghĩa đây là một trường bắt buộc phải có (Required field) và không có giá trị mặc định.
    name: Annotated[str, Field(..., description='Name of the patien')]
    city: Annotated[str, Field(..., description='City where the patient  is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obesity'

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data