# 1. Use an official Python runtime as a parent image
FROM python:3.9-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the requirements file into the container at /app
COPY requirements.txt .

# 4. Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code into the container at /app
# This will copy train.py and any other files in the build context
COPY . .

# 6. (Optional) Define environment variables, e.g., for model path (already in train.py)
# ENV MODEL_DIR=/app/model # We've hardcoded this in train.py as /app/model

# 7. Specify the command to run when the container starts
# This will execute our training script
CMD ["python", "train.py"]