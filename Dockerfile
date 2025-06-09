# Stage 1: Build the Vue.js frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY qa-review-app/package*.json ./
RUN npm install
COPY qa-review-app/ ./
RUN npm run build

# Stage 2: Final image with Python, Nginx, and Supervisor
FROM python:3.10-slim-buster

# Set working directory for the backend
WORKDIR /app

# Install OS dependencies: Nginx and Supervisor
RUN apt-get update && apt-get install -y nginx supervisor

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend source code
COPY . .

# Copy the built frontend from the 'frontend-builder' stage
COPY --from=frontend-builder /app/dist /var/www/html

# Copy our custom Nginx and Supervisor configurations
COPY nginx-single-file.conf /etc/nginx/sites-available/default
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the port Nginx will listen on
EXPOSE 80

# Start Supervisor to manage both Nginx and Uvicorn
CMD ["/usr/bin/supervisord"]