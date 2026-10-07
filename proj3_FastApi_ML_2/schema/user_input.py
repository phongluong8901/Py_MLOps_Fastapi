
# Pydantic model để validate dữ liệu đầu vào

from config.city_tier import tier_1_cities, tier_2_cities
from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal

class UserInput(BaseModel):
    
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the user")]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user in kg')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height of the user in meters')]
    income_lpa: Annotated[float, Field(..., gt=0, description='Annual income of the user in LPA')]
    smoker: Annotated[bool, Field(..., description='True if smoker, False otherwise')]
    city: Annotated[str, Field(..., description='City of the user')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]
       
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        # ✅ Đã sửa: dùng trực tiếp self.smoker và self.bmi thay vì dạng dictionary key
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker and self.bmi > 25:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3