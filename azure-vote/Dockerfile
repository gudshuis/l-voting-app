# Use a lightweight Python image with Flask support
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=80
ENV PATH=${PATH}:/home/site/wwwroot

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server vim curl wget supervisor && \
    pip install --no-cache-dir flask redis && \
    rm -rf /var/lib/apt/lists/*

# Copy application code to container
COPY azure-vote /app

# Set working directory
WORKDIR /app

# Copy Supervisor configuration for SSH
COPY app_init.supervisord.conf /etc/supervisor/conf.d/

# Expose ports (SSH and Flask app)
EXPOSE 2222 80

# Run Supervisor as the main process
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
