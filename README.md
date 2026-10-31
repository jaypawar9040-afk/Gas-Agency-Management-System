# Gas Agency Management System

A Python Flask-based web application designed to simplify gas cylinder booking and customer management.

## Project Overview

The Gas Agency Management System is a web application that provides customers with an online platform to register, log in, book gas cylinders and view their booking history.

The application aims to reduce manual booking processes and make customer information and booking management easier.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Relational database |
| Flask-SQLAlchemy | Database ORM |
| HTML5 | Webpage structure |
| CSS3 | Styling and layout |
| JavaScript | Client-side validation |
| Jinja2 | Dynamic HTML templates |
| Werkzeug | Password hashing |

## Features

- Customer registration and login
- Password hashing
- Session-based login management
- Domestic and commercial cylinder booking
- Booking information management
- Mock payment workflow
- Booking history
- Customer profile page
- Contact and information pages
- Form validation

## Project Structure

```text
Gas-Agency-Management-System/
│
├── app.py
├── init_db.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
├── templates/
└── static/
    ├── css/
    └── js/
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/jaypawar9040-afk/Gas-Agency-Management-System.git
```

### 2. Navigate to the project directory

```bash
cd Gas-Agency-Management-System
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Flask secret key

Set a local environment variable in PowerShell:

```powershell
$env:SECRET_KEY="your-own-random-secret"
```

### 7. Run the application

```bash
python app.py
```

### 8. Open the application

```text
http://127.0.0.1:5000/
```

## Database

The application uses SQLite with Flask-SQLAlchemy to manage customer and booking records.

The database is generated locally when the application initializes.

## Learning Outcomes

- Python backend development
- Flask routing and request handling
- Database integration using SQLAlchemy
- CRUD-related database operations
- Password hashing and session management
- Frontend and backend integration
- Form validation

## Limitations

- Payment is a demonstration workflow and does not process real transactions.
- A complete administrative management workflow is not yet implemented.
- The application is an academic portfolio project and is not intended for production use.

## Future Enhancements

- Integrate a real payment gateway.
- Implement complete admin functionality.
- Add booking status tracking.
- Improve database security and validation.
- Migrate to MySQL or PostgreSQL.

## Author

## Jay Pawar


GitHub: [jaypawar9040-afk](https://github.com/jaypawar9040-afk)

