# --- lib
1. from fastapi import Path
Trong FastAPI, from fastapi import Path dùng để khai báo, validate (kiểm tra tính hợp lệ) và mô tả cho các Path Parameters (tham số trên đường dẫn URL).

Khi bạn định nghĩa một route có biến trên đường dẫn, ví dụ: /patient/{patient_id}, FastAPI cần biết biến patient_id đó có quy tắc gì không (độ dài tối thiểu, kiểu dữ liệu, giá trị mặc định, hay thông tin mô tả cho tài liệu API). Path giúp bạn làm việc đó:

Mô tả chi tiết (Metadata): Thêm thông tin mô tả (description) hoặc ví dụ (example / examples) để khi bạn truy cập vào trang tài liệu tự động của FastAPI (/docs hoặc /redoc), người dùng hoặc lập trình viên khác sẽ hiểu rõ tham số này dùng để làm gì.

Validate dữ liệu (Validation): Bạn có thể giới hạn giá trị của tham số, ví dụ:

Số nguyên phải lớn hơn 0 (gt=0), hoặc nhỏ hơn hoặc bằng 100 (le=100).

Chuỗi ký tự phải có độ dài tối thiểu/tối đa (min_length, max_length), hoặc khớp với một biểu thức chính quy (regex).

2. from fastapi import Query
Tương tự như Path, from fastapi import Query là một công cụ mạnh mẽ trong FastAPI dùng để khai báo, validate (kiểm tra tính hợp lệ) và mô tả cho các Query Parameters (tham số truy vấn nằm sau dấu hỏi chấm ? trên URL, ví dụ: /sort?sort_by=bmi&order=desc).

Khi người dùng gửi request kèm theo các tham số trên URL (như ?sort_by=height&order=asc), Query giúp bạn kiểm soát chặt chẽ các tham số đó ngay từ đầu vào:

Xác định tính bắt buộc hoặc mặc định:

Nếu dùng Query(...) với dấu ... (Ellipsis), tham số đó trở thành bắt buộc. Nếu người dùng gọi API mà quên truyền tham số này, FastAPI sẽ tự động báo lỗi 422 Unprocessable Entity.

Nếu bạn đặt giá trị mặc định (ví dụ: Query('asc')), tham số đó sẽ là tùy chọn (optional). Nếu người dùng không truyền, FastAPI sẽ tự lấy giá trị mặc định ('asc').

Cung cấp Metadata cho tài liệu API (/docs): Giúp hiển thị phần description (mô tả) trực quan trên giao diện Swagger UI để lập trình viên khác biết tham số này dùng để làm gì.

Validate dữ liệu nâng cao: Bạn có thể giới hạn giá trị của Query Parameters tương tự như Path, ví dụ như độ dài chuỗi, biểu thức chính quy (regex), hoặc giới hạn số (ví dụ: ge=1, le=100 cho phân trang).

3. 
Path Parameter (Tham số đường dẫn)	Query Parameter (Tham số truy vấn)
Nằm trực tiếp bên trong cấu trúc đường dẫn URL.	Nằm ở cuối URL, bắt đầu sau dấu chấm hỏi (?) và cách nhau bởi dấu và (&).
/patient/{patient_id}


def get_patient(patient_id: str = Path(...))

/patients/search


def search_patients(name: str = Query(...))

Luôn luôn bắt buộc. Nếu thiếu, URL sẽ không khớp route và trả về lỗi 404 Not Found.	Có thể bắt buộc hoặc tùy chọn (thường là tùy chọn, có giá trị mặc định).

Dùng để định danh một tài nguyên cụ thể (resource identification).	Dùng để lọc, sắp xếp, tìm kiếm hoặc phân trang danh sách tài nguyên.

4. allergies: Optional[List[str]] = None
List[str]: Chỉ định rằng đây là một danh sách (list) mà các phần tử bên trong bắt buộc phải là chuỗi (string).
Optional[...]: Ký hiệu này (được import từ thư viện typing) có nghĩa là trường này có thể nhận kiểu dữ liệu bên trong hoặc có thể là None.
= None: Đặt giá trị mặc định cho nó là None.

5. contact_details: Dict[str, str]
Dict[str, str]: Định nghĩa đây là một kiểu dữ liệu Từ điển (dict), trong đó cả Key và Value đều bắt buộc phải là kiểu chuỗi (str).

6. email: EmailStr
EmailStr: Là một kiểu dữ liệu chuyên biệt được cung cấp bởi Pydantic (thường cần cài thêm gói bổ trợ pydantic[email]).

Vai trò & Xác thực: Nó kiểm tra xem chuỗi do người dùng truyền vào có đúng định dạng cấu trúc của một địa chỉ email hợp lệ hay không (phải có ký tự @, có tên miền phía sau, không có ký tự lạ không hợp lệ...).

í dụ thực tế:'nitish@example.com' $\rightarrow$ Hợp lệ, Pydantic chấp nhận.'nitish-at-example.com' hoặc 'abc' $\rightarrow$ Không hợp lệ, Pydantic sẽ tự động ném ra lỗi ValidationError ngay lập tức từ chối request.

7. linkedin_url: AnyUrl
AnyUrl: Là một kiểu dữ liệu kiểm tra định dạng URL/đường dẫn web (Universal Resource Locator).

Vai trò & Xác thực: Nó đảm bảo chuỗi được truyền vào phải là một đường dẫn URL hợp lệ theo chuẩn (phải bắt đầu bằng giao thức như http:// hoặc https://, có tên miền đàng hoàng). 

Ví dụ thực tế:'[https://www.linkedin.com/in/nitish](https://www.linkedin.com/in/nitish)' $\rightarrow$ Hợp lệ.'[www.linkedin.com](https://www.linkedin.com)' (thiếu https://) hoặc 'abcxyz' $\rightarrow$ Không hợp lệ, Pydantic sẽ báo lỗi.

8. @field_validator('name', mode='after')
 So sánh nhanh các chế độ mode trong Pydantic v2:
Pydantic v2 cung cấp 3 chế độ (mode) chính cho validator:

mode='after' (Mặc định):

Chạy sau khi Pydantic đã ép kiểu xong.

Dữ liệu truyền vào hàm validator lúc này đã đúng kiểu dữ liệu Python cơ bản (ví dụ: str, int, float).

Thường dùng nhất để kiểm tra nghiệp vụ (ví dụ: kiểm tra xem tuổi có lớn hơn 0 không, email có đúng domain không).

mode='before':

Chạy trước khi Pydantic làm bất cứ điều gì (trước cả bước ép kiểu hay kiểm tra kiểu).

Dữ liệu truyền vào hàm validator vẫn đang ở trạng thái thô sơ ban đầu (có thể là string, dict, hay bất cứ thứ gì người dùng gửi lên).

Thường dùng khi: Bạn muốn làm sạch dữ liệu thô trước (ví dụ: loại bỏ khoảng trắng thừa strip(), viết hoa toàn bộ chữ cái, hoặc tiền xử lý dữ liệu đầu vào).

mode='plain':

Thay thế hoàn toàn logic kiểm tra mặc định của Pydantic cho trường đó bằng hàm của riêng bạn.

9. Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the ')]
    weight: float

Literal (được import từ thư viện chuẩn typing của Python) là một công cụ cực kỳ mạnh mẽ dùng để giới hạn giá trị cố định mà một trường dữ liệu được phép nhận.

Ép buộc chọn đúng danh sách có sẵn: Thay vì cho phép người dùng nhập tự do bất kỳ chuỗi str nào (dẫn đến lỗi dữ liệu như nhập "Male", "MALE", "m", "nam", "nu"... mỗi người nhập một kiểu), Literal giới hạn bắt buộc giá trị của trường gender chỉ được phép khớp chính xác với một trong các phần tử nằm bên trong danh sách: 'male', 'female', hoặc 'others'.

Cơ chế xác thực của Pydantic:Nếu người dùng gửi lên gender: "male" $\rightarrow$ Hợp lệ, Pydantic chấp nhận.Nếu người dùng gửi lên gender: "unknown" hoặc gender: "Male" (viết hoa chữ M) $\rightarrow$ Lỗi ngay lập tức (vì phân biệt chữ hoa/thường), Pydantic sẽ từ chối request.