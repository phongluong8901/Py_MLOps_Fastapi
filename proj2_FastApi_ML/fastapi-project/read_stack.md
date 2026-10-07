# --- overall
Mục tiêu chính của dự án và khóa học này là hướng dẫn cách đưa các mô hình Machine Learning (đã train xong) vào ứng dụng thực tế bằng cách đóng gói và triển khai chúng dưới dạng API sử dụng FastAPI.

Các nội dung chính trong video/dự án bao gồm:

Xây dựng API với FastAPI: Thiết kế các endpoint (đường dẫn URL như /predict) để nhận dữ liệu đầu vào (ví dụ: thông tin đặc trưng của nhà đất, dữ liệu tài chính,...) từ người dùng hoặc hệ thống khác,.

Tích hợp Model Machine Learning: Kết nối các model AI/ML để xử lý dữ liệu và trả về kết quả dự đoán (như dự đoán giá nhà, phân tích rủi ro, v.v.),.

Xử lý tệp (File Upload/Download): Hướng dẫn tính năng cho phép người dùng tải lên các file dữ liệu (CSV/Excel) để hệ thống chạy hàng loạt (batch prediction) và cho phép tải file kết quả về máy,.

# --- lib
1. fastapi
Nó là gì: FastAPI là một hiện đại, siêu nhanh (high-performance) web framework dùng để xây dựng các RESTful API bằng Python dựa trên tiêu chuẩn type hints (kiểu dữ liệu chuẩn của Python).

2. uvicorn
Nó là gì: Uvicorn là một ASGI (Asynchronous Server Gateway Interface) server siêu nhanh dành cho Python, được xây dựng dựa trên uvloop và httptools.

FastAPI chỉ là một framework giúp bạn viết code API, nhưng nó không có khả năng tự chạy thành một máy chủ web trực tuyến. Uvicorn chính là máy chủ (server) nhận các yêu cầu HTTP từ bên ngoài (từ trình duyệt, ứng dụng mobile, Postman,...) rồi chuyển tiếp vào ứng dụng FastAPI của bạn và trả kết quả về.

3. from pydantic import BaseModel
dùng để nhập lớp cơ sở BaseModel từ thư viện Pydantic. Trong FastAPI, đây là dòng code nền tảng dùng để định nghĩa Data Model (Cấu trúc dữ liệu) cho các yêu cầu (requests) và phản hồi (responses) của API.

Tác dụng chính:
Kiểm tra kiểu dữ liệu tự động (Data Validation): Pydantic tự động kiểm tra, ép kiểu và báo lỗi chi tiết nếu dữ liệu đầu vào từ client không đúng định dạng (ví dụ: yêu cầu số nhưng lại gửi chữ).

Hỗ trợ tài liệu tự động (Swagger/OpenAPI): FastAPI dựa vào các model này để tự động tạo giao diện tài liệu trực quan tại /docs.

Gợi ý code (IDE Autocomplete): Giúp lập trình viên làm việc với các thuộc tính của dữ liệu một cách an toàn và nhanh chóng nhờ hệ thống type hints của Python.

# --- stack