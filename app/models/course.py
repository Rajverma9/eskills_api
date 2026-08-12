from typing import Optional
from sqlmodel import SQLModel, Field

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    course_id: str 
    course_name: str
    department: str
    instructor: str
    semester: str
    level: str
    credits: int
    fee: float