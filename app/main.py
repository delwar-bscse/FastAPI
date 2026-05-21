from fastapi import FastAPI, HTTPException, status, Response, Depends
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
@app.get("/course")
def course(db: Session = Depends(get_db)):
    return {"status":"SQLAlchemy is Working"}

@app.post("/")
def create_post(body:Course):
    cursor.execute("""INSERT INTO course (name, instructor, duration, website) VALUES (%s, %s, %s, %s) RETURNING *""", (body.name, body.instructor, body.duration, str(body.website)))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/")
def get_courses():
    cursor.execute("SELECT * FROM course ORDER BY id ASC")
    data = cursor.fetchall()
    return {"data": data}

@app.get("/{id}")
def get_course(id:int):
    cursor.execute("SELECT * FROM course WHERE id = %s", (str(id),))
    data = cursor.fetchone()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    return {"data": data}

@app.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("DELETE FROM course WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT, content="Course deleted successfully")

@app.put('/{id}')
def update_post(id:int, body:Course):
    cursor.execute("UPDATE course SET name = %s, instructor = %s, duration = %s, website = %s WHERE id = %s RETURNING *", (body.name, body.instructor, body.duration, str(body.website), str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} not found")
    return {"data": updated_post}