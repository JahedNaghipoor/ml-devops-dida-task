# Use a base image with necessary dependencies
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the trained model file(s) into the container
COPY trained_model.pkl /app/

# Copy any additional dependencies or scripts required for running the model
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy your model inference script (e.g., inference.py) into the container
COPY inference.py /app/

# Set the command to run your inference script when the container starts
CMD ["python", "inference.py"]
