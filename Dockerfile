# MCU Cinematic Dashboard Dockerfile
# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip

# Copy all project files
COPY . .

# Expose Dash default port
EXPOSE 8050

# Set environment variables for production
ENV DASH_ENV=production
ENV PORT=8050

# Run the dashboard
# For production, use Gunicorn to serve the Dash app
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]
