# ESKILLS – Course Management API

A **FastAPI-based Course Management API** with **JWT authentication**, **PostgreSQL database**, **SQLModel ORM**, and **Excel-based course data seeding**.

This project allows authenticated users to manage and retrieve course information stored in PostgreSQL.

---

## 🚀 Features

* FastAPI REST API
* JWT-based authentication
* User registration and login
* Password hashing using bcrypt
* PostgreSQL database
* SQLModel ORM
* Course CRUD operations
* Excel (`.xlsx`) course data import
* Seed course data from Excel
* Environment variable configuration using `.env`
* Service and router based project structure
* Automatic API documentation with Swagger UI

---

## 🛠️ Technologies Used

| Technology       | Purpose                 |
| ---------------- | ----------------------- |
| Python           | Backend programming     |
| FastAPI          | REST API framework      |
| SQLModel         | ORM and database models |
| PostgreSQL       | Database                |
| JWT              | Authentication          |
| Passlib / bcrypt | Password hashing        |
| Pandas           | Reading Excel data      |
| OpenPyXL         | Excel file support      |
| Uvicorn          | ASGI server             |
| python-dotenv    | Environment variables   |

---

## 📁 Project Structure

```text
ESKILLS/
│
├── app/
│   ├── models/
│   │   ├── __pycache__/
│   │   ├── course.py
│   │   └── user.py
│   │
│   ├── routers/
│   │   ├── __pycache__/
│   │   ├── auth.py
│   │   └── course.py
│   │
│   ├── seed/
│   │   ├── __pycache__/
│   │   ├── Course_Data.xlsx
│   │   └── run_seed.py
│   │
│   ├── services/
│   │   ├── __pycache__/
│   │   ├── auth_service.py
│   │   └── course_service.py
│   │
│   ├── database.py
│   └── main.py
│
├── venv/
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 📌 Folder Explanation

### `app/models/`

Contains SQLModel database models.

* `user.py` – User database model
* `course.py` – Course database model

### `app/routers/`

Contains API endpoints.

* `auth.py` – Registration and login APIs
* `course.py` – Course-related APIs

### `app/services/`

Contains business logic.

* `auth_service.py` – Password hashing, password verification and JWT token creation
* `course_service.py` – Course-related database operations

### `app/seed/`

Contains the Excel file and seeding script.

* `Course_Data.xlsx` – Course source data
* `run_seed.py` – Imports Excel data into PostgreSQL

### `database.py`

Handles:

* PostgreSQL connection
* SQLModel engine
* Database session
* Database configuration

### `main.py`

Main FastAPI application.

It:

* Creates the FastAPI application
* Includes routers
* Creates database tables
* Starts the API application

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd ESKILLS
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

If PowerShell gives an execution-policy error, you can use:

```bash
venv\Scripts\activate.bat
```

or activate the environment from Command Prompt.

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ PostgreSQL Configuration

Create a PostgreSQL database.

For example:

```sql
CREATE DATABASE eskills;
```

Create a `.env` file in the project root.

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=eskills

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Important

Do **not** commit `.env` to GitHub.

Make sure `.env` is included in `.gitignore`.

---

# ▶️ Run the Application

Start the FastAPI server with:

```bash
uvicorn app.main:app --reload
```

The API will normally run at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically provides Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

---

# 🔐 Authentication Flow

The authentication flow is:

```text
Register
   ↓
Login
   ↓
Verify Username & Password
   ↓
Generate JWT Access Token
   ↓
Send Token with Protected Requests
   ↓
Validate JWT
   ↓
Access Course APIs
```

The JWT token should be sent in the request header:

```text
Authorization: Bearer <access_token>
```

---

# 👤 Authentication APIs

## Register User

```http
POST /auth/register
```

Creates a new user account.

Example request:

```json
{
    "username": "raj",
    "email": "raj@example.com",
    "password": "password123"
}
```

---

## Login

```http
POST /auth/login
```

Authenticates the user and returns an access token.

Example:

```text
username: raj
password: password123
```

Response:

```json
{
    "access_token": "your-jwt-token",
    "token_type": "bearer"
}
```

Use this token to access protected course APIs.

---

# 📚 Course APIs

The course router contains endpoints for working with course data.

Typical operations include:

```text
GET     /course
GET     /course/{course_id}
POST    /course
PUT     /course/{course_id}
DELETE  /course/{course_id}
```

The exact available endpoints depend on the implementation in:

```text
app/routers/course.py
```

---

# 📊 Excel Data Seeding

The project supports importing course information from:

```text
app/seed/Course_Data.xlsx
```

The seeding script reads the Excel file and inserts course records into PostgreSQL.

Run:

```bash
python app/seed/run_seed.py
```

The basic process is:

```text
Course_Data.xlsx
       ↓
   Pandas
       ↓
Read Excel Data
       ↓
Validate / Transform Data
       ↓
SQLModel
       ↓
PostgreSQL
```

---

# 🧪 Testing the API

After starting the server:

```bash
uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Recommended testing sequence:

### Step 1 – Register

Call:

```text
POST /auth/register
```

### Step 2 – Login

Call:

```text
POST /auth/login
```

Copy the returned JWT token.

### Step 3 – Authorize

In Swagger, click **Authorize** and enter:

```text
Bearer <your-token>
```

### Step 4 – Test Course APIs

Now test the protected course endpoints.

---

# 🔒 Security

This project uses:

* JWT access tokens
* Password hashing
* Environment variables for database credentials
* Protected API endpoints

Never store passwords as plain text.

Passwords should be hashed before being stored in PostgreSQL.

---

# 🗃️ Database Architecture

The application follows this architecture:

```text
FastAPI
   │
   ├── Routers
   │      ├── Auth
   │      └── Course
   │
   ├── Services
   │      ├── Auth Service
   │      └── Course Service
   │
   ├── Models
   │      ├── User
   │      └── Course
   │
   └── Database
          │
          ↓
      PostgreSQL
```

---

# 🔄 Course Data Flow

```text
Excel File
    ↓
Pandas
    ↓
Seed Script
    ↓
SQLModel
    ↓
PostgreSQL
    ↓
FastAPI
    ↓
Course API
    ↓
Client / Swagger
```

---

# 🧩 Environment Variables

The application uses environment variables for configuration.

Example:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=eskills

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# 📦 Requirements

Install all required packages using:

```bash
pip install -r requirements.txt
```

To generate/update the requirements file:

```bash
pip freeze > requirements.txt
```

---

# 🐛 Common Issues

## Database Connection Error

Check:

* PostgreSQL is running
* Database name is correct
* Username is correct
* Password is correct
* Port is correct
* `.env` is configured correctly

---

## Excel File Not Found

Make sure the Excel file exists at:

```text
app/seed/Course_Data.xlsx
```

Run the seed script from the project root:

```bash
python app/seed/run_seed.py
```

---

## ModuleNotFoundError

Make sure the virtual environment is activated:

```bash
venv\Scripts\activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

---

## API Not Starting

Run:

```bash
uvicorn app.main:app --reload
```

Make sure you are running the command from the project root directory.

---

# 🚀 Future Improvements

Possible improvements include:

* Pagination for course APIs
* Search and filtering
* Course category filtering
* Role-based authentication
* Admin user functionality
* Course enrollment API
* API rate limiting
* Automated testing using Pytest
* Docker support
* PostgreSQL migrations using Alembic
* Deployment to Render or other cloud platforms

---

# 👨‍💻 Author

**ESKILLS Course Management API**

Built using **Python, FastAPI, SQLModel, PostgreSQL, JWT Authentication, and Pandas**.
