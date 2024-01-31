FROM python:3.9-slim

# Set environment varibles
# Reduce image size
ENV PYTHONDONTWRITEBYTECODE 1
# Force stdout/stderr to be unbuffered, directly send to terminal
ENV PYTHONUNBUFFERED 1

# Set the working directory in docker
WORKDIR /app

# Copy requirements.txt to the workdir
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy code files
COPY ./app /app/app

# Specify the command to run on container start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]