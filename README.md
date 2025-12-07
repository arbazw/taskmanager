# Task Manager API

A RESTful Task Manager API built using **Django** and **Django REST Framework**.
The application supports **JWT-based authentication**, full **CRUD operations on tasks**, pagination, filtering, role-based authorization, automated API documentation, and unit testing.

---

## Features

* User registration and JWT authentication
* Create, read, update, and delete tasks
* Pagination for task listings
* Filter tasks by completion status
* Role-based access control (admin vs regular user)
* Swagger and ReDoc API documentation
* Unit tests for authentication and task endpoints

---

## Tech Stack

* Python
* Django
* Django REST Framework
* JWT Authentication (SimpleJWT)
* SQLite
* Swagger / ReDoc (drf-yasg)

---

## Project Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd taskmanager
```

---

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

---

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

### 6. Run the Development Server

```bash
python manage.py runserver
```

The application will start at:

```text
http://127.0.0.1:8000/
```

---

## Authentication

### Register a New User

`POST /api/register/`

```json
{
  "username": "ahmad",
  "email": "ahmad@example.com",
  "password": "ahmad123"
}
```

---

### Obtain JWT Tokens (Login)

`POST /api/token/`

```json
{
  "username": "ahmad",
  "password": "ahmad123"
}
```

Response:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

Include the access token in all authenticated requests:

```http
Authorization: Bearer <access_token>
```

---

## Task API Endpoints

All task endpoints are prefixed with `/api/`.

---

### List Tasks (Paginated)

`GET /api/tasks/`

Query Parameters:

* `page` – page number
* `completed` – `true` or `false`

Example:

```http
GET /api/tasks/?completed=true&page=1
```

---

### Retrieve a Task

`GET /api/tasks/{id}/`

---

### Create a Task

`POST /api/tasks/`

Authentication required.

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "completed": false
}
```

---

### Update a Task

`PUT /api/tasks/{id}/`

Authentication required.
Only the task owner or an admin can update.

```json
{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples",
  "completed": true
}
```

---

### Delete a Task

`DELETE /api/tasks/{id}/`

Authentication required.
Only the task owner or an admin can delete.

---

## Roles & Permissions

* **Regular User**

  * Can create tasks
  * Can view only their own tasks
  * Can update or delete only their own tasks

* **Admin User (`is_staff=True`)**

  * Full access to all tasks
  * Can manage all users’ tasks

---

## API Documentation

Auto-generated API documentation is available at:

* **Swagger UI**

  ```
  http://127.0.0.1:8000/swagger/
  ```

* **ReDoc**

  ```
  http://127.0.0.1:8000/redoc/
  ```

---

## Testing

To run unit tests:

```bash
python manage.py test
```

Tests cover:

* User registration
* JWT authentication
* Task creation
* Task listing with pagination
* Filtering by completion status
* Permission enforcement

