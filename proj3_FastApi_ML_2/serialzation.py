from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = 'Male'
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'nitish', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

# exclude_unset=True có nghĩa là gì? Nó yêu cầu Pydantic: "Hãy loại bỏ (exclude) tất cả những trường mà người dùng không thực sự truyền vào (unset) lúc khởi tạo, ngay cả khi trường đó có giá trị mặc định".
temp = patient1.model_dump(exclude_unset=True)

print(temp)
print(type(temp))