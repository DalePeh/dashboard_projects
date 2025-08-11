# MCU Cinematic Dashboard Dockerfile
# Use official Python image
FROM python:3.12-slim

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
# For production, use Gunicorn (uncomment next line)
# CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:app"]

# For development, use Dash's built-in server
CMD ["python", "app.py"]
