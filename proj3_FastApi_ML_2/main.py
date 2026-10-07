#1. Setup FastApi
#2. HTTP methods
#3. Path & Quey Params
#4. pydantic

# 1. Import các công cụ cần thiết từ thư viện fastapi và thư viện chuẩn json của Python
from typing import Literal, Optional
from pydantic import computed_field
from pydantic import Field
from typing import Annotated
from pydantic import BaseModel
from fastapi import Query
from fastapi import HTTPException
from fastapi import Path
from fastapi import FastAPI
import json
from fastapi.responses import JSONResponse

# 2. Khởi tạo một ứng dụng FastAPI và đặt tên đối tượng là 'app'
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

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

# 3. Định nghĩa hàm load_data để đọc dữ liệu bệnh nhân từ file json
def load_data():
    # Mở file 'patients.json' với chế độ đọc ('r')
    with open('patients.json', 'r') as f:
        # Đọc dữ liệu JSON và chuyển đổi thành dictionary trong Python
        data = json.load(f)
    # Trả về dữ liệu đã được tải
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

# 4. Định nghĩa route GET cho đường dẫn gốc ("/")
@app.get("/")
def hello():
    # Trả về thông điệp chào mừng khi người dùng truy cập trang chủ API
    return {"message": "Patient Management System API"}

# 5. Định nghĩa route GET cho đường dẫn '/about'
@app.get('/about')
def about():
    # Trả về thông tin giới thiệu ngắn gọn về chức năng của ứng dụng API
    return {
        'message': "A fully functional API to manage your patient records"
    }

# 6. Định nghĩa route GET cho đường dẫn '/view' để lấy toàn bộ danh sách bệnh nhân
@app.get('/view')
def view():
    # Gọi hàm load_data() để lấy toàn bộ dữ liệu từ file
    data = load_data()
    # Trả về toàn bộ danh sách bệnh nhân dưới dạng JSON
    return data

# 7. Định nghĩa route GET có tham số đường dẫn (Path Parameter) để xem chi tiết 1 bệnh nhân theo ID
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="ID of the patient in the DB", example="PT-94821")):
    # Tải toàn bộ danh sách bệnh nhân lên bộ nhớ
    data = load_data()

    # Kiểm tra xem ID bệnh nhân có tồn tại trong các khóa của dictionary không
    if patient_id in data:
        # Nếu tìm thấy, trả về thông tin chi tiết của bệnh nhân đó
        return data[patient_id]
    
    # Nếu không tìm thấy, chủ động ném ra ngoại lệ HTTPException với mã lỗi 404 (Not Found)
    raise HTTPException(
        status_code=404,
        detail='Patient not found'
    )

# 8. Định nghĩa route GET có tham số truy vấn (Query Parameter) để sắp xếp danh sách bệnh nhân
@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description="sort on the basis of height, weight or bmi"),
    order: str = Query('asc', description='sort in asc or desc order')
):
    # Khai báo danh sách các trường hợp lệ được phép sắp xếp
    valid_fields = ['height', 'weight', 'bmi']

    # Kiểm tra xem người dùng truyền 'sort_by' có nằm trong danh sách hợp lệ không
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid sort field. Sort by {", ".join(valid_fields)}'
        )
    
    # Kiểm tra chiều sắp xếp (thứ tự) chỉ chấp nhận 'asc' hoặc 'desc'
    if order not in ['asc', 'desc']:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Use 'asc' for ascending or 'desc' for descending order."
        )

    # Tải dữ liệu bệnh nhân từ file
    data = load_data()

    # Chuyển đổi chuỗi order thành giá trị boolean cho tham số reverse của hàm sorted() (desc = True, asc = False)
    sort_order = True if order == 'desc' else False

    # Xác định đường dẫn key nằm lồng bên trong cấu trúc JSON (đối tượng vitals) để lấy đúng dữ liệu sắp xếp
    if sort_by == 'height':
        key_func = lambda x: x.get('vitals', {}).get('height_cm', 0)
    elif sort_by == 'weight':
        key_func = lambda x: x.get('vitals', {}).get('weight_kg', 0)
    else:  # 'bmi'
        key_func = lambda x: x.get('vitals', {}).get('bmi', 0)

    # Sắp xếp danh sách các giá trị bệnh nhân dựa theo hàm key đã chọn và thứ tự đảo ngược (reverse)
    sorted_data = sorted(data.values(), key=key_func, reverse=sort_order)

    # Trả về kết quả thông báo kèm theo danh sách dữ liệu đã được sắp xếp
    return {
        'message': f'Patients sorted by {sort_by} ({order})',
        'data': sorted_data
    }

# ==========================================
# 7. ROUTE TẠO MỚI BỆNH NHÂN (POST)
# ==========================================
@app.post('/create') # (Lưu ý: Đã bổ sung dấu gạch chéo '/' trước 'create')
def create_patient(patient: Patient):
    # Tải dữ liệu hiện tại từ file
    data = load_data()

    # Kiểm tra xem bệnh nhân đã tồn tại trong hệ thống chưa bằng ID
    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient already exists" 
        )
    
    # Thêm bệnh nhân mới vào database (chuyển đổi object Pydantic thành dict và loại bỏ trường id thừa)
    data[patient.id] = patient.model_dump(exclude=['id'])

    # Lưu lại thay đổi vào file JSON
    save_data(data)

    # Trả về phản hồi thành công kèm mã trạng thái 201 (Created)
    return JSONResponse(
        status_code=201,
        content= {
            'message': 'Patient created successfully',
            'patient_id': patient.id
        }
    )


# ==========================================
# 8. ROUTE CẬP NHẬT THÔNG TIN BỆNH NHÂN (PUT)
# ==========================================
@app.put('/edit/{patient_id}')
def update_patient(
    patient_id: str, patient_update: PatientUpdate # (Lưu ý: Sửa dấu '=' thành ':' cho đúng cú pháp FastAPI)
):
    data = load_data()

    # Kiểm tra xem bệnh nhân cần sửa có tồn tại không
    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail='Patient not found'
        )

    # Lấy thông tin cũ của bệnh nhân
    existing_patient_info = data[patient_id]

    # Lọc ra những trường thực sự được người dùng gửi lên để sửa (bỏ qua các trường None nhờ exclude_unset=True)
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    # Ghi đè các trường mới vào thông tin cũ
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # Gắn lại ID vào dictionary thông tin để tiến hành tái cấu trúc Pydantic object
    existing_patient_info['id'] = patient_id
    
    # Khởi tạo lại đối tượng Patient để Pydantic tự động tính toán lại BMI và Verdict theo số liệu mới
    patient_pydantic_obj = Patient(**existing_patient_info)
    
    # Chuyển đổi ngược lại đối tượng Pydantic thành dict (loại bỏ trường id thừa ở cấp độ lưu trữ)
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    # Cập nhật vào dictionary tổng và lưu xuống file
    data[patient_id] = existing_patient_info
    save_data(data)

    return JSONResponse(
        status_code=200,
        content= {
            'message': 'Patient updated successfully',
            'patient_id': patient_id
        }
    )

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    #load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail='Patient not found'
        )

    del data[patient_id]
    save_data(data)

    return JSONResponse(
        status_code=200,
        content= {
            'message': 'Patient deleted successfully',
            'patient_id': patient_id
        }
    )