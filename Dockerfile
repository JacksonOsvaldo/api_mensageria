# Pull base image
FROM python:3.11

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy full code project
COPY . .

# Update and install python dependence
RUN pip install -U pip
RUN pip install -r /app/requirements.txt

# Specify the default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]