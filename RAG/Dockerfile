FROM nvidia/cuda:12.4.0-cudnn8-runtime-ubuntu22.04

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your code
COPY . .

# Default command
CMD ["python3", "your_script.py"]
