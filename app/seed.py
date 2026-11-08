from sqlalchemy import select

from app.database import SessionLocal
from app.models import Category, Course, CourseModule, User
from app.security import hash_password


def run():
    db = SessionLocal()
    try:
        admin = db.scalar(
            select(User).where(User.email == "admin@skillbridge.id")
        )
        
        if admin is None:
            admin = User(
                full_name="Admin SkillBridge",
                email="admin@skillbridge.id",
                password_hash=hash_password("Admin123!"),
                role="admin",
            )
            db.add(admin)

        instructor = db.scalar(
            select(User).where(User.email == "instructor@skillbridge.id")
        )

        if instructor is None:
            instructor = User(
                full_name="Instruktur Satu",
                email="instructor@skillbridge.id",
                password_hash=hash_password("Instruktur123!"),
                role="instructor",
            )
            db.add(instructor)
        category = db.scalar(
            select(Category).where(Category.name == "Backend Development")
        )

        if category is None:
            category = Category(name="Backend Development")
            db.add(category)
            db.flush()

        course = db.scalar(
            select(Course).where(
                Course.title.startswith("REST API dengan FastAPI")
            )
        )

        if course is None:
            course = Course(
                category_id=category.id,
                instructor_id=instructor.id,
                title="REST API dengan FastAPI",
                description="Dari nol sampai API siap produksi.",
                price=150000,
            )
            db.add(course)
            db.flush()

        titles = [
            "Pengenalan REST",
            "Routing dan Validasi",
            "Database dan ORM",
            "Autentikasi JWT",
        ]

        for i, title in enumerate(titles, start=1):
            module = db.scalar(
                select(CourseModule).where(
                    CourseModule.course_id == course.id,
                    CourseModule.position == i,
                )
            )

            if module is None:
                db.add(
                    CourseModule(
                        course_id=course.id,
                        title=title,
                        position=i,
                    )
                )

        db.commit()
        print("Seed berhasil atau data yang hilang telah dilengkapi.")
        
    finally:
        db.close()


if __name__ == "__main__":
    run()
