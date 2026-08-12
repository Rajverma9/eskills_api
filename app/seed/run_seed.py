import os
import pandas as pd
from sqlmodel import Session, select
from app.database import engine
from app.models.course import Course

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCEL_FILE = os.path.join(BASE_DIR,"Course_Data.xlsx")


def import_courses():
    df = pd.read_excel(EXCEL_FILE,sheet_name="Course Data")
    with Session(engine) as session:
        for _, row in df.iterrows():

            course_id = str(row["Course ID"])
            existing_course = session.exec(select(Course).where(Course.course_id == course_id)).first()

            if existing_course:
                continue

            course = Course(
                course_id=course_id,
                course_name=str(row["Course Name"]),
                department=str(row["Department"]),
                instructor=str(row["Instructor"]),
                semester=str(row["Semester"]),
                level=str(row["Level"]),
                credits=int(row["Credits"]),
                fee=float(row["Fee ($)"])
            )

            session.add(course)
        session.commit()


if __name__ == "__main__":
    import_courses()
    print("Courses imported successfully!")