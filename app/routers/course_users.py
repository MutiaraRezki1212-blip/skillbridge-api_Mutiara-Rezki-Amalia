
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Course, Enrollment, User

router = APIRouter(
    prefix="/skillbridge",
    tags=["SkillBridge Users"]
)


@router.get("/course/{course_id}/users")
def get_course_users(
    course_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(404, "Kursus tidak ditemukan")

    users = db.scalars(
        select(User)
        .join(Enrollment, Enrollment.student_id == User.id)
        .where(Enrollment.course_id == course_id)
        .order_by(User.full_name)
    ).all()

    return {
        "message": "Daftar user berhasil diambil",
        "data": [
            {
                "id": str(user.id),
                "full_name": user.full_name,
                "email": user.email,
            }
            for user in users
        ],
        "errors": None,
    }
