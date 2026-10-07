from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float # kg
    height: float # mtr
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi



def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('BMI', patient.bmi)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@icici.com', 'age': '65', 'weight': 75.2, 'height': 1.72, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462', 'emergency':'235236'}}

patient1 = Patient(**patient_info) 

update_patient_data(patient1)

# Trường ảo tự động sinh ra: Bình thường, các trường như name, age, weight là những dữ liệu do người dùng truyền vào (Input). Nhưng đôi khi bạn cần một trường dữ liệu được tính toán dựa trên các trường có sẵn (ví dụ: tính BMI từ cân nặng và chiều cao, tính tổng tiền, tính khoảng cách...), thay vì bắt người dùng phải gửi lên.

# @computed_field kết hợp với @property:

# Giúp bạn tạo ra một thuộc tính mới (bmi) gắn liền với đối tượng model Pydantic.

# Khi đối tượng được khởi tạo hoặc chuyển đổi sang định dạng JSON (ví dụ trả về qua API FastAPI), trường bmi này sẽ tự động xuất hiện như một trường dữ liệu bình thường của model.

# @computed_field: Đánh dấu để Pydantic hiểu rằng đây là một trường dữ liệu cần được bao gồm khi serialization (xuất dữ liệu ra JSON/dict).

# @property: Biến phương thức bmi(self) thành một thuộc tính (property). Nhờ vậy, khi gọi ra sử dụng, bạn chỉ cần viết patient.bmi mà không cần thêm cặp dấu ngoặc tròn () (không cần viết patient.bmi()), giống hệt như các trường dữ liệu thông thường (patient.name, patient.age).

# self.weight và self.height: Lấy trực tiếp cân nặng và chiều cao đã được Pydantic chuẩn hóa và ép kiểu từ đối tượng hiện tại (self).