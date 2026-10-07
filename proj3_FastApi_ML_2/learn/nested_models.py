from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'nitish', 'gender': 'male', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

# Chỉ lấy ra 'name' và 'age', bỏ qua 'gender' và 'address'
temp = patient1.model_dump(include={'name', 'age'})

print(type(temp))






# 1. Hàm model_dump() trong Pydantic v2 là gì?
# Chuyển đổi Model thành Dictionary chuẩn của Python: Mặc dù patient1 là một đối tượng Pydantic, nhưng khi làm việc với API (như trả về qua FastAPI) hoặc lưu trữ, bạn thường cần chuyển nó về dạng Dictionary (dict) thô. Hàm model_dump() sinh ra để làm việc này.

# Sự khác biệt với phiên bản cũ: Ở Pydantic v1, hàm này có tên là .dict(). Sang Pydantic v2, người ta đã đổi tên thành .model_dump() để chuẩn hóa và tối ưu hiệu suất.