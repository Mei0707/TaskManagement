# Task Manager API
A simple RESTful API for managing tasks. This API allows users to create, update, delete tasks, and log their actions (create, update, delete) using JWT authentication. The project is built using Flask and SQLAlchemy.

## Features

- **User Authentication**: Secure user authentication using JWT.
- **Task Management**: Users can create, update, delete tasks.
- **Task Logs**: Records and retrieves task actions such as task creation, updates, and deletions.
- **Priority Levels**: Users can assign priorities to tasks (e.g., High, Medium, Low).

## Endpoints

- `POST /tasks`: Create a new task.
- `PUT /tasks/<task_id>`: Update an existing task.
- `DELETE /tasks/<task_id>`: Delete a task.
- `GET /task_logs`: Retrieve logs of task actions for the logged-in user.

## Tech Stack

- **Backend**: Flask
- **Database**: SQLAlchemy (SQLite for development)
- **Authentication**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy
- **API Documentation**: Postman or Swagger can be used for testing and documenting API endpoints.

## Instructions to Run the Project
1. **Install Dependencies**: Run the following command to install the required packages:
```
pip install -r requirements.txt
```

2. **Set Up Database**: Initialize the database and create the tables:
```
from app import db
db.create_all()
```

3. **Run the Application**: Start the Flask application:
```
python app.py
```

4. **Test the Endpoints**: You can use Postman or curl to test the API endpoints for registration, login, and task management.

## API Documentation

## Task Endpoints
1. ### Create a Task
- **Endpoint**: `POST /tasks`
- **Authorization**: Requires JWT token
- **Body Parameters**:
```
{
  "title": "Task title",
  "description": "Task description",
  "priority": "High"
}
```
- **Response**:
```
{
  "msg": "Task created",
  "id": 1
}
```
2. ### Update a Task
- **Endpoint**: PUT /tasks/<task_id>
- **Authorization**: Requires JWT token
- **Body Parameters** (Partial update allowed):
```
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "priority": "Low"
}
```
- **Response**:
```
{
  "msg": "Task updated"
}
```
3. ### Delete a Task
- **Endpoint**: DELETE /tasks/<task_id>
- **Authorization**: Requires JWT token
- **Response**:
```
{
  "msg": "Task deleted"
}
```

## Task Log Endpoint
1. ### Get Task Logs
- **Endpoint**: GET /task_logs
- **Authorization**: Requires JWT token
- **Response**:
```
[
  {
    "id": 1,
    "task_id": 1,
    "action": "create",
    "timestamp": "2024-09-20T12:34:56"
  },
  {
    "id": 2,
    "task_id": 1,
    "action": "update",
    "timestamp": "2024-09-20T13:34:56"
  }
]
```

## Authentication

### User Login
- Use any JWT login method to generate the token.
- Ensure that the token is passed in the `Authorization` header of every API request as:
```
Authorization: Bearer <your_jwt_token>
```

## Future Improvements

- **Task Completion**: Add the ability for users to mark tasks as completed.
- **Task Reminders**: Allow users to set reminders for tasks with a due date.
- **Pagination**: Add pagination to task logs for better performance with large datasets.
- **Frontend Integration**: Develop a frontend for users to interact with the API.