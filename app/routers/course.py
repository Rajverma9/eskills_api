from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.course import Course
from app.routers.auth import get_current_user
from app.seed.run_seed import run_seed

router = APIRouter(prefix="/courses",tags=["Courses"])

# 1. Get all courses
@router.get("/")
def get_courses(session: Session = Depends(get_session)):
    course =  session.exec(select(Course)).all()
    
    if len(course) == 0:
        run_seed()
        destination =  session.exec(select(Course)).all()
    return destination


# 2. Create course
@router.post("/")
def create_course(course: Course,session: Session = Depends(get_session),username:str = Depends(get_current_user)):
    existing_course = session.exec(select(Course).where(Course.course_id == course.course_id)).first()
    if existing_course:
        raise HTTPException(status_code=409,detail="Course already exists")
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


# 3. Get courses by department
@router.get("/department/{department}")
def get_by_department(department: str,session: Session = Depends(get_session)):
    return session.exec(select(Course).where(Course.department == department)).all()


# 4. Get courses by instructor
@router.get("/instructor/{instructor}")
def get_by_instructor(instructor: str,session: Session = Depends(get_session)):
    return session.exec(select(Course).where(Course.instructor == instructor)).all()


# 5. Get courses by level
@router.get("/level/{level}")
def get_by_level(level: str,session: Session = Depends(get_session)):
    return session.exec(select(Course).where(Course.level == level)).all()


# 6. Get expensive courses
@router.get("/expensive")
def get_expensive(min_fee: float,session: Session = Depends(get_session)):
    return session.exec(select(Course).where(Course.fee >= min_fee)).all()


# 7. Search courses
@router.get("/search")
def search(name: str,session: Session = Depends(get_session)):
    return session.exec(select(Course).where(Course.course_name.ilike(f"%{name}%"))).all()


# 8. Get course by ID
@router.get("/{course_id}")
def get_course(course_id: str,session: Session = Depends(get_session)):

    course = session.exec(select(Course).where(Course.course_id == course_id)).first()

    if not course:
        raise HTTPException(status_code=404,detail="Course not found")
    return course


# 9. Update course
@router.put("/{course_id}")
def update_course(course_id: str,course_data: Course,session: Session = Depends(get_session),username:str = Depends(get_current_user)):

    course = session.exec(select(Course).where(Course.course_id == course_id)).first()

    if not course:
        raise HTTPException(status_code=404,detail="Course not found")

    course.course_name = course_data.course_name
    course.department = course_data.department
    course.instructor = course_data.instructor
    course.semester = course_data.semester
    course.level = course_data.level
    course.credits = course_data.credits
    course.fee = course_data.fee

    session.add(course)
    session.commit()
    session.refresh(course)
    return course


# 10. Delete course
@router.delete("/{course_id}")
def delete_course(course_id: str,session: Session = Depends(get_session),username:str = Depends(get_current_user)):

    course = session.exec(select(Course).where(Course.course_id == course_id)).first()

    if not course:
        raise HTTPException(status_code=404,detail="Course not found")
    session.delete(course)
    session.commit()
    return {
        "message": "Course deleted successfully"
    }