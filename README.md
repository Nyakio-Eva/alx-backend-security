# alx-backend-security
# IP Tracking & Security for Django

## Overview
This project adds request tracking, IP-based security, and anomaly detection features to a Django application.  
It demonstrates middleware, logging, blacklisting, geolocation, rate limiting, and background task processing with Celery.

---

## Features
- **Request Logging**: Middleware records IP address, timestamp, and path for every request.  
- **IP Blacklisting**: Block requests from blacklisted IPs, returning `403 Forbidden`.  
- **Geolocation Analytics**: Enrich logs with country and city (using IP geolocation).  
- **Rate Limiting**: Prevent abuse with per-IP request limits (via `django-ratelimit`).  
  - Anonymous users: **5 requests/minute**  
  - Authenticated users: **10 requests/minute**  
- **Anomaly Detection**: Celery task runs hourly to flag suspicious IPs:  
  - >100 requests/hour  
  - Access to sensitive paths (`/admin`, `/login`)  
- **Suspicious IP Database**: Store and review flagged IPs for further action.

---

## Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone <repo-url>
   cd backend_security

2. **Create and activate a virtual environment**
   ```bash
   python -m venv djangoenv
   source djangoenv/bin/activate

3. **Install dependencies**   
   ```bash
    pip install -r requirements.txt

4. **Run migrations**
    ```bash
    python manage.py migrate

5. **Start Redis (for Celery)**
   ```bash
   redis-server

6. **Start Celery worker & beat (in separate terminals)**
   ```bash
   celery -A backend_security worker -l info
   celery -A backend_security beat -l info

7. **Run the server**
   ```bash
    python manage.py runserver

### Models

    RequestLog: Stores request metadata (IP, path, timestamp, geolocation).

    BlockedIP: Stores blacklisted IPs.

    SuspiciousIP: Stores flagged IPs with reasons.

### Security Enhancements

    Middleware for IP tracking and blocking.

    Rate limiting to reduce brute-force attacks.

    Geolocation for traffic insights.

    Automated anomaly detection with Celery.    

## Tech Stack

    Django (web framework)

    Celery + Redis (task scheduling & background jobs)

    django-ratelimit (rate limiting)

    IP geolocation library    

### Next Steps

    Integrate automatic blocking of suspicious IPs.

    Add Django admin views for easier IP management.

    Expand anomaly detection rules.   



    