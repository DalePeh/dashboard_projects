# MCU Cinematic Dashboard Dockerfile
# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Dash default port
EXPOSE 8050

# Set environment variables for production
ENV DASH_ENV=production
ENV PORT=8050

# Run the dashboard
CMD ["python", "app.py"]
