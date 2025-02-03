# 🔍 US Visa Appointment Slot Checker | Automated Notification System

[![Docker Support](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated monitoring tool that checks for available US visa appointment slots at Indian consulates and VAC (Visa Application Center) locations. Get instant notifications when slots become available for US visa appointments in India.

## 🌟 Key Features

- **Real-time Monitoring**: Checks US visa slots every 3 minutes automatically
- **Multi-location Support**: Monitors multiple Indian consulates and VAC locations simultaneously
- **Smart Notifications**:
  - 📧 Email alerts (Gmail, Yahoo, Outlook, custom SMTP)
  - 📱 Mobile push notifications via Pushover
- **Flexible Configuration**:
  - Customizable time window for slot checking
  - Multiple location monitoring
  - IST (Indian Standard Time) timezone support
- **Enterprise Features**:
  - Proxy support for reliable API access
  - Detailed logging system
  - Docker-based deployment
  - Automatic restart on failure

## 🚀 Quick Start Guide

### Prerequisites

- 🐳 Docker and Docker Compose installed on your system
- 🔑 [checkvisaslots.com](https://checkvisaslots.com) account
  - Free registration required for API key access
  - While this tool works without a paid subscription, please consider subscribing to support checkvisaslots.com if you find this tool useful
  - Get your API key from the dashboard
- 📱 Pushover account for mobile notifications (optional)
  - Sign up at [pushover.net](https://pushover.net)
  - Create an application to get your application token
  - Get your user key from the dashboard
- 📧 SMTP email account (Gmail/Yahoo/Outlook/Custom SMTP)

## Environment Variables

Create a `.env` file with the following variables:

```env
# Required
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-email-password
RECEIVER_EMAIL=recipient@email.com
API_KEY=your-checkvisaslots-api-key

# Optional
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
PROXY_IP=your-proxy-ip
PROXY_PORT=your-proxy-port
PUSHOVER_TOKEN=your-pushover-token
PUSHOVER_USER=your-pushover-user
VISA_CONSULATE_LOCATIONS=NEW DELHI
VISA_VAC_LOCATIONS=NEW DELHI VAC,MUMBAI VAC,KOLKATA VAC
VISA_DURATION_DAYS=120
```

## Installation & Deployment

1. Clone the repository:
```bash
git clone <repository-url>
cd us-visa-slot-checker
```

2. Create and configure the `.env` file with your settings

3. Build and start the Docker container:
```bash
docker-compose up -d
```

4. Check the logs:
```bash
docker-compose logs -f
```

## How It Works

1. The script runs every 3 minutes via cron
2. It checks for available slots at configured consulate and VAC locations
3. When slots are available at both a consulate AND a VAC location within the configured time window:
   - Sends an email notification
   - Sends a Pushover notification (if configured)
4. The script converts all timestamps to IST for easier tracking

## 🔧 Configuration Options

### 📍 Visa Locations
Configure which locations to monitor:
- `VISA_CONSULATE_LOCATIONS`: Consulate locations (default: "NEW DELHI")
- `VISA_VAC_LOCATIONS`: VAC locations (default: "NEW DELHI VAC,MUMBAI VAC,KOLKATA VAC")

### ⏰ Time Window
- `VISA_DURATION_DAYS`: Search window in days (default: 120 days)

### 📧 Email Configuration
- Compatible with major email providers
- Secure SMTP support with TLS
- App-specific password support for enhanced security

### 🔒 Proxy Settings
- Enterprise-grade proxy support
- Configurable proxy host and port
- Improved reliability for API requests

## 📝 Logging

- Structured logs in `./logs` directory
- IST timestamp format
- Detailed API response tracking
- Notification delivery status

## 🐳 Docker Deployment

Built on:
- Python 3.10 Alpine for minimal footprint
- Supervisor for process management
- Automatic container health checks
- Volume-based log persistence

## 🤝 Contributing

We welcome:
- Bug reports
- Feature requests
- Pull requests
- Documentation improvements

## 📄 License

This project is open source and available under the MIT License.

## 🔍 Keywords
us visa appointment, visa slot checker, us visa slots india, visa appointment tracker, us visa booking, consulate appointment, vac appointment, automated visa checker, us visa notification, visa slot availability

---
*Built with ❤️ for the US visa applicant community in India* 