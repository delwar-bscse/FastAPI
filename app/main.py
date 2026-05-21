from fastapi import FastAPI, HTTPException, status, Response, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from . database import engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Connect to database
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='123456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(3)

# Define request body schema.
class Course(BaseModel):
    name:str
    instructor:str
    duration:float
    website:HttpUrl

# Define routes and functions for the API
@app.post("/")
def create_course(body:Course, db: Session = Depends(get_db)):
    new_course = models.Course(name=body.name, instructor=body.instructor, duration=body.duration, website=str(body.website))
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"data": new_course}

@app.get("/")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return {"Courses": courses}

@app.get("/{id}")
def get_course(id:int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    return {"Course details": course}

@app.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put('/{id}')
def update_post(id:int, body:Course, db: Session = Depends(get_db)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    update_course = body.model_dump()
    update_course["website"] = str(update_course["website"])
    course_query.update(update_course, synchronize_session=False)
    db.commit()
    db.refresh(course)
    return {"Updated course details": course}