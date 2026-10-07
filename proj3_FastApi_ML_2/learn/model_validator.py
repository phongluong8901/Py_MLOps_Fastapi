from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must be have emergency contact')
        return model


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@icici.com', 'age': '65', 'weight': 75.2, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462', 'emergency':'235236'}}

patient1 = Patient(**patient_info) 

update_patient_data(patient1)

@model_validator(mode='after')

# Ý nghĩa: Đây là một decorator của Pydantic. Chữ mode='after' nghĩa là hàm bên dưới sẽ được kích hoạt chạy sau khi Pydantic đã hoàn tất việc kiểm tra, xác thực và ép kiểu cho tất cả các trường đơn lẻ (như name, age, contact_details,...) có trong model Patient.

# def validate_emergency_contact(cls, model):

# Ý nghĩa: Định nghĩa tên hàm kiểm tra tùy chỉnh (bạn đặt tên gì cũng được).

# cls: Đại diện cho chính lớp Patient.

# model: Đại diện cho toàn bộ đối tượng bệnh nhân vừa được khởi tạo xong. Nhờ có tham số này, bạn có thể truy cập vào nhiều trường dữ liệu cùng một lúc (ở đây ta dùng được cả model.age và model.contact_details trong cùng một chỗ).

# if model.age > 60 and 'emergency' not in model.contact_details:

# Ý nghĩa: Đây là điều kiện nghiệp vụ kết hợp chéo giữa 2 trường:

# model.age > 60: Kiểm tra xem bệnh nhân có lớn hơn 60 tuổi hay không.

# 'emergency' not in model.contact_details: Kiểm tra xem trong từ điển thông tin liên lạc (contact_details) có chứa khóa (key) nào tên là 'emergency' hay chưa.

# Dấu and có nghĩa là: Cả hai điều kiện trên phải đồng thời xảy ra thì câu lệnh if mới đúng. Tức là: "Bệnh nhân trên 60 tuổi VÀ KHÔNG có số liên lạc khẩn cấp".

# raise ValueError('Patients older than 60 must be have emergency contact')

# Ý nghĩa: Nếu lọt vào trong if (tức là phạm luật: trên 60 tuổi mà quên điền thông tin khẩn cấp), chương trình sẽ ngay lập tức ném ra lỗi ValueError kèm theo thông báo giải thích. Việc này làm quá trình tạo đối tượng bị hủy bỏ và báo lỗi về cho người dùng/client.