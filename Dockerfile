# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /AI_API

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI project files into the container
COPY . .

# Expose the port that FastAPI will run on (default is 8000)
EXPOSE 8000

# Command to run the FastAPI application using uvicorn (change 'main:app' to your app's file and instance)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
