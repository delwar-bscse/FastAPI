from fastapi import  HTTPException, status, Response, Depends, HTTPException, APIRouter
from .. import models, schemas
from .. database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/courses"
)


@router.post("/", response_model=schemas.CourseResponse)
def create_course(body:schemas.CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(**body.model_dump())
    new_course.website = str(body.website)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.get("/", response_model=list[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses

@router.get("/{id}", response_model=schemas.CourseResponse)
def get_course(id:int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    return course

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put('/{id}', response_model=schemas.CourseResponse)
def update_post(id:int, body:schemas.CourseCreate, db: Session = Depends(get_db)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    update_course = body.model_dump()
    update_course["website"] = str(update_course["website"])
    course_query.update(update_course, synchronize_session=False)
    db.commit()
    db.refresh(course)
    return course
