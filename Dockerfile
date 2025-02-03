FROM python:3.10-alpine

# Install cron and tzdata
RUN apk add --no-cache dcron tzdata supervisor

# Set timezone
ENV TZ=Asia/Kolkata

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY visa_slot_checker.py .
COPY crontab /etc/crontabs/root

# Configure supervisord
COPY supervisord.conf /etc/supervisord.conf


# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
