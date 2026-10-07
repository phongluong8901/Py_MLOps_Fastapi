#not pydantic

# def insert_patient_data(name: str, age: int):
    
#     if type(name) == str and type(age) == int:
#         if age < 0:
#             raise ValueError("Age must be positive integer")
#         else:
#             print(name)
#             print(age)
#             print("inserted into database")
#     else:
#         raise TypeError("Name must be string and age must be integer")


# def update_patient_data(name: str, age: int):
    
#     if type(name) == str and type(age) == int:
#         print(name)
#         print(age)
#         print("inserted into database")
#     else:
#         raise TypeError("Name must be string and age must be integer")


# insert_patient_data("nitish", 30)

#pydantic
from pydantic import AnyUrl
from pydantic import EmailStr
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Annotated

# Định nghĩa một Pydantic Model có tên là 'Patient'
class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of patient', description='Give the name of the patient in less than 50 character')]
    email: EmailStr
    linkedin_url: AnyUrl
    age: Annotated[int, Field(gt=0, lt=120)]
    weight: Annotated[float, Field(gt=0)]
    married: Annotated[bool, Field(default=None, description="Is the patient married or not")]
    allergies: Annotated[Optional[List[str]], Field(max_length=5)]
    contact_details: Dict[str, str]


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted into database")

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.contact_details)
    print("updated into database")

# Tạo một dictionary chứa thông tin thô
patient_info = {
    'name': 'nitish', 
    'email': 'nitish@example.com',
    'linkedin_url': 'https://www.linkedin.com/in/nitish-kumar-354a1a192/',
    'age': 30, 
    'weight': '70.5', 
    'married': True, 
    'allergies': ['penicillin', 'peanuts'], 
    'contact_details': {'email': 'nitish@example.com', 'phone': '1234567890'}
}

#Khởi tạo một đối tượng Patient từ dictionary trên bằng kỹ thuật Unpacking(**)
# cú pháp ** dùng để "unpack" (phân rã) dictionary thành các keyword arguments. Dòng này tương đương với việc bạn viết: Patient(name='nitish', age=30).
patient1 = Patient(**patient_info)

print(patient1)

insert_patient_data(patient1)