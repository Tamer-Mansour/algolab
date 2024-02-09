
```markdown
# My Django App

## Setup

### 1. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
```

### 2. Activate the virtual environment (Windows)
```bash
venv\Scripts\activate
```
or (Unix/macOS)
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations (if needed)
```bash
python manage.py migrate
```

## Run the App

### 1. Run the Django development server
```bash
python manage.py runserver
```

### 2. Run the app using Docker

#### Build the Docker image
```bash
docker-compose build
```

#### Run the Docker container
```bash
docker-compose up
```

## Usage

### Register a new user
```bash
curl -X POST -d "email=user@example.com&username=user&password=123456" http://localhost:8000/register/
```

### Login
```bash
curl -X POST -d "email=user@example.com&password=123456" http://localhost:8000/login/
```

### Retrieve all users
```bash
curl http://localhost:8000/users/
```

```
