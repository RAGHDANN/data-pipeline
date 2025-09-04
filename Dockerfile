# ---- Base Stage ----
# Use a specific, slim version of the official Python image
FROM python:3.10-slim as base

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python output is sent straight to the terminal
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# ---- Builder Stage ----
# This stage installs dependencies
FROM base as builder

# Install build dependencies
RUN pip install --upgrade pip

# Copy only the requirements file to leverage Docker's cache
COPY requirements.txt .

# Install Python dependencies
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- Final Stage ----
# This stage builds the final, lean image
FROM base

# Copy installed dependencies from the builder stage
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy the application source code
COPY . .

# [OPTIONAL] Create a non-root user for security
RUN useradd --create-home appuser
USER appuser

# Define the command to run your application
# This assumes your main.py is designed to be executed directly.
# If it runs a web server (like Flask/FastAPI), you might use gunicorn instead.
CMD ["python", "main.py"]