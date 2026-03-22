# I'm using the official Python 3.11 slim image as the base
# Slim keeps the image size small which makes deployment faster
FROM python:3.11-slim

# I'm setting the working directory inside the container
WORKDIR /app

# I'm copying the requirements file first and installing dependencies
# Docker caches this layer so if requirements don't change it won't reinstall everything
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# I'm copying all the project files into the container
COPY . .

# I'm exposing port 8000 which is the default port FastAPI runs on
EXPOSE 8000

# I'm telling Docker to start the FastAPI app using uvicorn when the container runs
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]