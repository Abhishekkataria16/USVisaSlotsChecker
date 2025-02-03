# US Visa Slot Checker

An automated tool to monitor and notify about available US visa appointment slots across different consulates and VAC (Visa Application Center) locations in India.

## Features

- Monitors US visa appointment slots every 3 minutes
- Supports multiple consulate and VAC locations
- Dual notification system:
  - Email notifications (supports Gmail and custom SMTP servers)
  - Pushover mobile notifications
- Configurable time window for slot checking
- Docker-based deployment for easy setup
- Timezone set to IST (India Standard Time)
- Proxy support for API requests
- Detailed logging

## Prerequisites

- Docker and Docker Compose
- Account on [checkvisaslots.com](https://checkvisaslots.com) to obtain API key
  - Register and subscribe to their service
  - Get your API key from the dashboard
- Pushover account for mobile notifications (optional)
  - Register at [pushover.net](https://pushover.net)
  - Create an application to get your application token
  - Get your user key from the dashboard
- SMTP email account (Gmail/Yahoo/zoho etc)

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

## Configuration Options

### Visa Locations
- `VISA_CONSULATE_LOCATIONS`: Comma-separated list of consulate locations (default: "NEW DELHI")
- `VISA_VAC_LOCATIONS`: Comma-separated list of VAC locations (default: "NEW DELHI VAC,MUMBAI VAC,KOLKATA VAC")

### Time Window
- `VISA_DURATION_DAYS`: Number of days to look ahead for slots (default: 120 days)

### Email Settings
- Supports both Gmail and custom SMTP servers
- For Gmail, enable "Less secure app access" or use App Password

### Proxy Configuration
- Optional proxy support for API requests
- Configure using `PROXY_IP` and `PROXY_PORT`

## Logging

- Logs are stored in the `./logs` directory
- All times are in IST (India Standard Time)
- Includes API response details and notification status

## Docker Support

The application runs in a Docker container with:
- Python 3.10 Alpine base image
- Automatic restart on failure
- Volume mapping for logs
- Supervisor for process management

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License. 