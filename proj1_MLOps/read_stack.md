# ---
1. MLOps
MLOps (Machine Learning Operations) là sự kết hợp giữa Machine Learning, Data Engineering và DevOps.   Nếu như DevOps giúp tự động hóa và tối ưu hóa vòng đời phát triển phần mềm truyền thống (từ viết code, build, test đến deploy), thì MLOps làm điều tương tự nhưng dành riêng cho các hệ thống Trí tuệ Nhân tạo và Học máy.   
Mục tiêu của MLOps: Tự động hóa, chuẩn hóa và quản lý toàn bộ vòng đời của mô hình ML — từ thu thập dữ liệu, huấn luyện, kiểm thử, đóng gói, triển khai cho đến giám sát sau khi lên sóng.   

2. MLflow
MLflow là một nền tảng mã nguồn mở phổ biến hàng đầu được phát triển bởi Databricks để quản lý toàn bộ vòng đời thí nghiệm và mô hình Machine Learning.

MLflow tập trung mạnh vào các kỹ sư dữ liệu và nhà khoa học dữ liệu (Data Scientists) thông qua 4 thành phần chính:MLflow Tracking: Theo dõi, ghi lại và so sánh các thông số (parameters), kết quả đánh giá (metrics) và mã nguồn của từng lần huấn luyện mô hình.   MLflow Projects: Tiêu chuẩn hóa cách đóng gói mã nguồn ML để bất kỳ ai cũng có thể chạy lại thí nghiệm đó một cách đồng nhất.   MLflow Models: Định dạng chuẩn để lưu trữ và phục vụ mô hình từ nhiều framework khác nhau (như Scikit-Learn, PyTorch, TensorFlow, XGBoost, Hugging Face,...).   Model Registry: Kho lưu trữ trung tâm để quản lý các phiên bản mô hình, phê duyệt trạng thái (ví dụ: chuyển từ Staging sang Production).   

3. ZenML
ZenML là một framework MLOps mã nguồn mở có khả năng mở rộng cao, được thiết kế dưới dạng Orchestrator (công cụ điều phối).   
Nếu MLflow mạnh về việc theo dõi và quản lý vòng đời/thí nghiệm mô hình, thì ZenML giúp bạn xây dựng và kết nối toàn bộ các bước trong một hệ thống MLOps thành một Pipeline hoàn chỉnh (từ bước lấy dữ liệu, tiền xử lý, huấn luyện, đánh giá đến triển khai).

Điểm nổi bật của ZenML:Cho phép viết code dưới dạng các Steps và Pipelines bằng Python thuần túy.Tính linh hoạt cao: Dễ dàng chuyển đổi hạ tầng từ máy cá nhân (local) sang các nền tảng đám mây lớn (AWS, GCP, Azure) hoặc các công cụ điều phối như Kubeflow, Airflow mà không cần sửa đổi nhiều mã nguồn.Tích hợp sâu với MLflow: ZenML thường đóng vai trò là khung kết nối bên trên, còn MLflow được tích hợp vào bên trong ZenML để làm kho lưu trữ mô hình hoặc công cụ theo dõi thí nghiệm.   

# --- dataset
Dữ liệu này được cung cấp bởi Olist – một nền tảng chuyên tích hợp các cửa hàng nhỏ (merchants) vào các sàn thương mại điện tử lớn tại Brazil. Bộ dữ liệu gồm khoảng 100.000 đơn hàng được thực hiện từ năm 2016 đến 2018 trên nhiều marketplace khác nhau.   

a. olist_customers_dataset.csv (Thông tin khách hàng)   Chứa thông tin về khách hàng thực hiện đơn hàng.customer_id: Khóa chính dùng trong bảng orders (mỗi đơn hàng có một customer_id riêng biệt để bảo mật định danh).   customer_unique_id: ID thực sự của khách hàng (dùng để tracking một người mua nhiều lần).customer_zip_code_prefix, customer_city, customer_state: Mã bưu chính, thành phố và bang của khách hàng.

# --- source
Khóa học này hướng dẫn học viên xây dựng một hệ thống Machine Learning hoàn chỉnh từ khâu thu thập dữ liệu (data ingestion) cho đến khi đưa mô hình lên môi trường sản xuất (deployment), áp dụng các công cụ và framework tiêu chuẩn công nghiệp hiện đại.

1. Mục tiêu cốt lõi của Repository
Xây dựng Pipeline MLOps chuẩn Production: Không chỉ dừng lại ở việc huấn luyện mô hình (Model Training) trên Jupyter Notebook, repository này hướng dẫn cách tổ chức code theo hướng phần mềm kỹ thuật phần mềm sạch (Clean Code / Modular Code).

Ứng dụng các Framework MLOps hiện đại: Sử dụng các công cụ chuyên nghiệp để quản lý vòng đời dữ liệu và mô hình thay vì lưu file thủ công.

2. Các công nghệ và công cụ chính được sử dụngZenML: Framework chính để xây dựng các pipeline MLOps (Data Ingestion $\rightarrow$ Processing $\rightarrow$ Training $\rightarrow$ Evaluation $\rightarrow$ Deployment). ZenML giúp đóng gói các bước thành các steps và pipelines có thể tái sử dụng dễ dàng.

MLflow: Công cụ theo dõi thực nghiệm (Experiment Tracking) và quản lý Model Registry. Giúp ghi lại các thông số (parameters), độ đo (metrics) và lưu trữ artifact (file weights của mô hình) qua các lần chạy.

Scikit-Learn / Machine Learning Libraries: Dùng để xây dựng các bài toán dự đoán (ví dụ: dự đoán độ hài lòng của khách hàng - Customer Satisfaction dựa trên dataset thương mại điện tử Olist mà bạn vừa hỏi ở trên).

4. Quy trình vận hành một Pipeline mẫu (Workflow)
Khi chạy source code này, quy trình vận hành một bài toán MLOps thường diễn ra như sau:

Ingest Data: Đọc dữ liệu từ file hoặc database và đưa vào ZenML Artifact Store.

Handle Missing Values / Cleaning: Tiền xử lý dữ liệu, tách tập huấn luyện (train) và kiểm thử (test).

Train Model: Huấn luyện mô hình và tự động ghi nhận (log) các chỉ số hiệu năng lên MLflow.

Evaluate: Kiểm tra xem mô hình có đạt ngưỡng chất lượng (accuracy/RMSE) yêu cầu hay không.

Deploy: Đóng gói và đẩy mô hình lên môi trường phục vụ dự đoán (Model Deployment Endpoint) nếu vượt qua bài kiểm tra.

# --- lib
1. logging
Thư viện logging là một module có sẵn trong thư viện chuẩn (built-in library) của Python, dùng để ghi lại các sự kiện, thông báo lỗi, cảnh báo hoặc thông tin trạng thái khi chương trình chạy.

So với việc dùng hàm print(), sử dụng logging mang lại nhiều ưu điểm vượt trội:

Phân loại mức độ quan trọng: Dễ dàng lọc xem thông điệp nào là thông tin thông thường, thông điệp nào là lỗi nghiêm trọng.

Định hướng đầu ra linh hoạt: Có thể in ra màn hình (console), ghi vào file, gửi qua email hoặc chuyển đến các hệ thống giám sát từ xa.

Cung cấp metadata tự động: Tự động gắn kèm thời gian (timestamp), tên module, số dòng code gây ra sự kiện.

2. from abc import ABC, abstractmethod
Dòng lệnh from abc import ABC, abstractmethod dùng để nhập (import) các công cụ xây dựng Abstract Base Class (Lớp cơ sở trừu tượng) trong Python.

Modul abc (Abstract Base Classes) giúp bạn định nghĩa ra các "khuôn mẫu" hoặc "giao diện" (interface) chung cho một nhóm các lớp con, từ đó ép buộc các lớp con phải tuân theo cấu trúc nhất định.

ABC (Abstract Base Class): Là một lớp cơ sở đặc biệt. Khi một lớp kế thừa từ ABC, nó trở thành một lớp trừu tượng. Bạn không thể khởi tạo trực tiếp đối tượng từ lớp trừu tượng này (ví dụ: gọi obj = TenLopTruuTuong() sẽ báo lỗi). Nó chỉ dùng làm lớp cha để các lớp khác kế thừa.

@abstractmethod (Decorator): Dùng để đánh dấu một phương thức là phương thức trừu tượng. Phương thức này không có phần thân (thường chỉ để pass hoặc ...). Bất kỳ lớp con nào kế thừa từ lớp cha bắt buộc phải viết lại (override) phương thức này, nếu không Python sẽ báo lỗi ngay khi bạn cố gắng khởi tạo đối tượng của lớp con.

3. from typing import Union
Dòng lệnh from typing import Union dùng để nhập công cụ khai báo kiểu dữ liệu kết hợp (Union types) trong cơ chế gợi ý kiểu dữ liệu (Type Hinting) của Python.

Nó cho phép bạn chỉ định rằng một biến, tham số hàm hoặc giá trị trả về có thể nhận một trong nhiều kiểu dữ liệu khác nhau.

Khi bạn viết Union[int, str], điều đó có nghĩa là giá trị được phép là hoặc là số nguyên (int) hoặc là chuỗi (str).

Lưu ý trong các phiên bản Python hiện đại (từ Python 3.10 trở lên):
Bạn có thể thay thế Union[int, str] bằng cú pháp gọn hơn là int | str sử dụng toán tử gạch đứng (|). Tuy nhiên, Union vẫn được dùng rất phổ biến trong các codebase cũ hoặc khi cần tương thích ngược.

4. from typing_extensions import Annotated
Dòng lệnh from typing_extensions import Annotated dùng để nhập công cụ gắn siêu dữ liệu (metadata) vào các gợi ý kiểu dữ liệu (Type Hints) trong Python.

Annotated[Kieu_du_lieu, Metadata_1, Metadata_2, ...]

Annotated được sử dụng rộng rãi để gắn các quy tắc validate vào tham số:

5. from typing import Tuple

Dòng lệnh from typing import Tuple dùng để nhập công cụ khai báo kiểu dữ liệu Tuple (bộ dữ liệu cố định) trong cơ chế gợi ý kiểu dữ liệu (Type Hinting) của Python.

Tuple thuần nhất không giới hạn độ dài (Tuple[int, ...]):
Nếu bạn thêm dấu ba chấm ..., nó có nghĩa là tuple này có thể chứa số lượng phần tử tùy ý, nhưng tất cả các phần tử đó đều phải cùng một kiểu dữ liệu (trong ví dụ này là int).

# Hàm trả về tọa độ và tên (độ dài cố định 3 phần tử với các kiểu cụ thể)
def get_location() -> Tuple[int, int, str]:
    return (10, 20, "Hà Nội")

# Hàm tính tổng danh sách số truyền vào dưới dạng tuple tùy ý
def calculate_total(numbers: Tuple[int, ...]) -> int:
    return sum(numbers)


# --- lib ML
1. from sklearn.base import RegressorMixin
chuyên được sử dụng khi bạn muốn tự xây dựng một mô hình máy học hồi quy (custom regressor) tích hợp mượt mà vào hệ sinh thái của scikit-learn.

Trong scikit-learn, các "mixin" là những lớp phụ (mix-in classes) không đứng độc lập mà dùng để bổ sung các tính năng định sẵn cho lớp chính thông qua đa kế thừa (multiple inheritance).Khi bạn tạo một mô hình hồi quy tùy chỉnh và cho nó kế thừa từ RegressorMixin, bạn nhận được các lợi ích sau:Tự động có phương thức .score(): Lớp này cung cấp sẵn hàm .score(X, y) để tính toán hệ số xác định $R^2$ (coefficient of determination) cho mô hình của bạn mà bạn không cần phải tự viết lại code tính toán.Tương thích với hệ sinh thái scikit-learn: Giúp các công cụ như GridSearchCV, RandomizedSearchCV, Pipeline, hoặc các hàm kiểm tra loại mô hình (như is_regressor()) nhận diện chính xác đối tượng của bạn là một mô hình hồi quy.