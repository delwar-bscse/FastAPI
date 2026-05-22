from fastapi import  HTTPException, status, Response, Depends, HTTPException, APIRouter
from .. import models, schemas
from .. database import get_db
from sqlalchemy.orm import Session
from .. import oauth2
from typing import Optional

router = APIRouter(
  prefix="/courses"
)


# Create course route
@router.post("/", response_model=schemas.CourseResponse)
def create_course(body:schemas.CourseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    course_data = body.model_dump()
    course_data["website"] = str(body.website)

    new_course = models.Course(
        **course_data,
        creator_id=current_user.id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# Get all courses route
@router.get("/", response_model=list[schemas.CourseResponse])
def get_courses(search:Optional[str] = None, limit:int = 10, page:int = 1, db: Session = Depends(get_db)):
    courses = db.query(models.Course).filter(models.Course.name.contains(search)).limit(limit).offset((page-1)*limit).all()
    return courses

# Get course route
@router.get("/{id}", response_model=schemas.CourseResponse)
def get_course(id:int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    return course

# Delete course route
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id:int, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    db.delete(course)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# Update course route
@router.put('/{id}', response_model=schemas.CourseResponse)
def update_course(id:int, body:schemas.CourseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    update_course = body.model_dump()
    update_course["website"] = str(update_course["website"])
    course_query.update(update_course, synchronize_session=False)
    db.commit()
    return course_query.first()