# --- lib
1. from pydantic import BaseModel, Field
BaseModel:

Dùng để định nghĩa cấu trúc dữ liệu (Data Schema) cho các request/response trong FastAPI. Mọi class dữ liệu bạn tạo ra đều phải kế thừa (inherit) từ BaseModel.

Field:

Dùng để cấu hình và ràng buộc chi tiết (Validation & Metadata) cho từng thuộc tính bên trong Model.

Thay vì chỉ khai báo kiểu dữ liệu đơn thuần (như age: int), Field cho phép bạn đặt thêm các quy tắc kiểm tra nâng cao ngay trong code Python.

from pydantic import BaseModel, Field

class HouseFeatures(BaseModel):
    # Dùng Field để đặt ràng buộc:
    # - ge=0: Giá trị phải lớn hơn hoặc bằng 0 (Greater than or Equal)
    # - description: Thêm mô tả để hiện lên trang tài liệu Swagger UI tự động của FastAPI
    # - examples: Cung cấp dữ liệu mẫu gợi ý sẵn
    MedInc: float = Field(..., ge=0, description="Median income in block group", example=8.3252)
    HouseAge: float = Field(..., ge=0, le=100, description="Median house age in years")
    AveRooms: float = Field(..., gt=0, description="Average number of rooms per household")

Các tác dụng phổ biến của Field:
Kiểm tra giới hạn số: ge (lớn hơn hoặc bằng), gt (lớn hơn hẳn), le (nhỏ hơn hoặc bằng), lt (nhỏ hơn hẳn).

Kiểm tra độ dài chuỗi: min_length, max_length, regex (định dạng biểu thức chính quy).

Cung cấp giá trị mặc định: default=... hoặc default_factory.

Tài liệu hóa API: Thêm title, description, và example để giao diện Swagger (/docs) hiển thị rõ ràng cho người dùng biết cần nhập dữ liệu gì.

2. UploadFile (từ fastapi)
Nó là gì: Lớp đại diện cho một tệp tin (file) được người dùng tải lên (upload) thông qua yêu cầu HTTP (thường dùng trong các form multipart/form-data).

Vai trò: Giúp FastAPI xử lý các tệp tin lớn (như file CSV, hình ảnh, video,...) một cách hiệu quả thông qua bộ nhớ đệm (spooled files) mà không làm tràn RAM của server. Bạn có thể dùng nó để đọc nội dung file dòng bằng dòng hoặc lưu file vào ổ cứng

3. File (từ fastapi)
Nó là gì: Hàm đánh dấu (parameter function) được dùng trong các hàm xử lý API để thông báo cho FastAPI rằng tham số truyền vào là một file được đính kèm từ request của người dùng.

Vai trò: Đi kèm với UploadFile (ví dụ: file: UploadFile = File(...)) để bắt buộc client phải gửi file lên thì hàm API mới được phép thực thi.

4. StreamingResponse (từ fastapi.responses)
Nó là gì: Phản hồi dạng dòng chảy (stream).

Vai trò: Cho phép server trả về dữ liệu cho client theo từng phần (chunk) thay vì phải chờ xử lý xong toàn bộ rồi mới gửi một cục. Rất hữu ích khi bạn muốn trả về các file có dung lượng lớn (như file kết quả dự đoán dạng CSV/Excel) để client có thể tải xuống trực tiếp mà không tốn nhiều bộ nhớ RAM của server.
