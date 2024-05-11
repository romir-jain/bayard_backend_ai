# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 10000

RUN wandb login 1bdbac3dfcb8032804408d746c8bd5276db82e4e

# Run the Flask application with Gunicorn
CMD ["gunicorn", "app:app"]