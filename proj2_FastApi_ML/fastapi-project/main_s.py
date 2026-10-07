#handling exception

from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import FastAPI

app = FastAPI()

students = {
    "S001": {"name": "A", "marks": 95, "grade": "A"},
    "S002": {"name": "B", "marks": 75, "grade": "B"},
    "S003": {"name": "C", "marks": 55, "grade": "C"},
}

#input schema
class MarkSubmission(BaseModel):
    student_id: str
    marks: int
    subject: str

@app.get("/student/{student_id}")
def get_student(student_id: str):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail=f"student with ID {student_id} does not exists"
        )

    return students[student_id]

#Body
# {
#   "student_id": "S001",
#   "marks": 100,
#   "subject": "maths"
# }
@app.post("/submit-marks")  # Đã thêm dấu / ở đầu đường dẫn
def submit_marks(submission: MarkSubmission):
    #error 1: student does not exist
    if submission.student_id not in students:
        raise HTTPException(
            status_code=404,
            detail=f"student with ID {submission.student_id} does not exists"
        )
        
    #error 2: valid range 0-120 (Đã sửa từ ranks thành marks)
    if submission.marks < 0 or submission.marks > 120:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "marks must be between 0 and 120",
                "marks_received": submission.marks,
                "fix": "enter a valid value between 0 and 120"
            }
        )
        
    #error 3: subject name empty
    if submission.subject.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Subject name cannot be empty"
        )
    
    # Cập nhật điểm mới vào database giả lập
    students[submission.student_id]["marks"] = submission.marks

    return {
        "message": "marks submitted successfully",
        "student": students[submission.student_id]["name"],
        "subject": submission.subject,
        "marks": submission.marks
    }