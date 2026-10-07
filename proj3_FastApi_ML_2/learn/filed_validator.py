from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    #@field_validator('email'): Đây là decorator của Pydantic v2 dùng để chỉ định rằng hàm bên dưới sẽ dùng để tự kiểm tra và lọc dữ liệu riêng cho trường email (ngoài việc kiểm tra cú pháp email thông thường của EmailStr).
    @field_validator('email')
    @classmethod    #@classmethod: Bắt buộc phải có trong Pydantic v2 khi viết các hàm validator để biến phương thức này thành phương thức lớp.
    #Khi bạn dùng @classmethod, phương thức đó thuộc về cả lớp chứ không gắn liền với một đối tượng riêng lẻ nào cả. Lúc này tham số đầu tiên bắt buộc phải là cls (đại diện cho class).
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        #abc@gmail.com
        #để tách lấy phần đuôi của email (phần tên miền).
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError("Email domain is not valid")
        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @field_validator('age', mode='before') #Khi dùng mode='before', hàm validator sẽ chạy trước khi Pydantic ép kiểu dữ liệu.
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in beween 0 and 100')


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@icici.com', 'age': '30', 'weight': 75.2, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462'}}

patient1 = Patient(**patient_info) # validation -> type coercion

update_patient_data(patient1)