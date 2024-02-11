# Use the official Python image as a base image
FROM python:3.9-slim

# Set environment variables for Python to run in unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Run migrations and collect static files (if applicable)
RUN python manage.py makemigrations
RUN python manage.py migrate

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
