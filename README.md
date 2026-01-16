# FastAPI Task Manager

A RESTful API built with FastAPI for managing tasks and users with authentication and authorization.

## Features

- ✅ User registration and authentication (JWT)
- ✅ Role-based access control (Admin/User)
- ✅ CRUD operations for tasks
- ✅ Task assignment to users
- ✅ Database migrations with Alembic
- ✅ PostgreSQL database integration
- ✅ Password hashing with bcrypt

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Database
- **Alembic**: Database migration tool
- **Pydantic**: Data validation
- **JWT**: Token-based authentication
- **Uvicorn**: ASGI server

## Project Structure

```
fastapi-task-manager/
├── alembic/                  # Database migrations
├── app/
│   ├── core/                 # Core configuration
│   │   ├── config.py         # Settings and environment variables
│   │   └── security.py       # JWT and password hashing
│   ├── database/             # Database setup
│   │   └── connection.py     # SQLAlchemy engine and session
│   ├── dependencies/         # Dependency injection
│   │   └── auth.py           # Authentication dependencies
│   ├── models/               # SQLAlchemy models
│   │   ├── users.py
│   │   └── tasks.py
│   ├── routers/              # API endpoints
│   │   ├── users.py
│   │   └── tasks.py
│   ├── schemas/              # Pydantic schemas
│   │   ├── user.py
│   │   └── task.py
│   └── main.py               # Application entry point
├── .env                      # Environment variables (not in git)
├── .env.example              # Example environment variables
├── requirements.txt          # Python dependencies
└── README.md
```

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL
- pip and virtualenv

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-task-manager
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Set up the database**
   - Create a PostgreSQL database
   - Update `DATABASE_URL` in `.env`

6. **Run migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /users/register` - Register a new user
- `POST /users/login` - Login and get JWT token

### Users (Admin only)

- `GET /users/` - Get all users with their tasks

### Tasks

- `GET /tasks/` - Get all tasks for current user
- `POST /tasks/` - Create a new task
- `GET /tasks/{task_id}` - Get task by ID
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Environment Variables

See `.env.example` for required environment variables.

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Development

### Running Tests
```bash
# Add your test command here
pytest
```

### Code Style
```bash
# Format code
black .

# Lint code
flake8 .
```

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.