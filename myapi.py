from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# API Endpoint - like a path for url ()
# ex.
# amazon.com/create-user
#localhost/delete-user
# GET - GET SOME INFORMATION
# POST - CREATE SOMETHING NEW (LIKE NEW OBJECT IN DATABASE)
# PUT - UPDATE SOMETHING
# DELETE - DELETE SOMETHING


# HOW WE CREATE A NEW API

# python dictionary called 'students'
students = {
    1: {
        "name": "john",
        "age": 17,
        "year": "year 12"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[int] = None


@app.get("/") # just a slash is our home page
def index():
    return {"name": "First Data"} # will return JSON data

@app.get("/get-student/{student_id}") # studentID is a parameter
def get_student(student_id: int = Path(..., description="The ID of the student you want to view.", gt=0, lt=3)): # Path(None) describes the input, gt will limit input and will return error with feedback if condiiton not met
    return students[student_id]

# ex. google.com/get-student/1  ---> gets user with id = 1, or 2, this is a parameter

# gt,lt, ge, le (size constraints)


# Query parameters - a query is used to pass a value into the URL

# ? denotes a query attached to an endpoint 
# ex. google.com/results?search=Python  --> the query parameter here is 'search (the key)' = 'Python (the value)'

# @app.get("/get-by-name")
# # note that python does not allow us to have an optioinal argumetn before a required one --> adding *, at the beginging of the parameters fixes this
# def get_student(*, name : Optional[str] = None, test : int): # adding Optional[str] = None make this a non-required field. Note needed optional library for this
#     for student_id in students:
#         if  students[student_id]['name'] == name:
#             return students[student_id]
#     return {"Data": "Not found"} 



# we can also combine a path pareametr and a query parameter togetehr
@app.get("/get-by-name/{student_id}")
# note that python does not allow us to have an optioinal argumetn before a required one --> adding *, at the beginging of the parameters fixes this
def get_student(*, student_id : int, name : Optional[str] = None, test : int): # adding Optional[str] = None make this a non-required field. Note needed optional library for this
    for student_id in students:
        if  students[student_id]['name'] == name:
            return students[student_id]
    return {"Data": "Not found"} 


# creating a new path (new object in DB) using POST method 

@app.post("/create-student/{student_id}")
# takes in the id alongside all student details
def create_student(student_id : int, student : Student):
    if student_id in students: 
        return {"Error": "Student exists"}
    
    # create new student object
    students[student_id] = student
    return students[student_id]

# PUT METHOD - used to update something that already exists

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent): # update is good as if the student changes a singular value, the other values will remain the same
    if student_id not in students:
        return {"Error": "Student does not exist"}


    # Essentially if the new value input by the user is not NULL we want to update it
    if student.name != None: 
        students[student_id].name = student.name

    if student.age != None: 
        students[student_id].age = student.age

    if student.year != None: 
        students[student_id].year = student.year


    return students[student_id]


@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error" : "Student does not exist"}
    
    del students[student_id]
    return {"Message": "Student deleted successfully"}