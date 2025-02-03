import requests
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dateutil import parser
import http.client
import urllib.parse

def send_email(slot_details):
    # Email configuration
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')  # Default to Gmail SMTP
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))  # Default to port 587
    use_tls = os.environ.get('SMTP_USE_TLS', 'true').lower() == 'true'  # Default to True
    
    if not all([sender_email, sender_password, receiver_email]):
        print("Email configuration missing. Please set SENDER_EMAIL, SENDER_PASSWORD, and RECEIVER_EMAIL environment variables.")
        return
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'US Visa Slot Available!'
    
    # Create email body
    body = "US Visa slots are available!\n\n"
    for slot in slot_details:
        # Parse the createdon string to a datetime object
        gmt_time = datetime.strptime(slot['createdon'], "%a, %d %b %Y %H:%M:%S %Z")
        
        # Convert to IST by adding 5 hours and 30 minutes
        ist_time = gmt_time + timedelta(hours=5, minutes=30)
        
        # Format the IST time back to a string
        ist_time_str = ist_time.strftime("%Y-%m-%d %H:%M:%S")
        
        body += f"Location: {slot['visa_location']}\n"
        body += f"Number of slots: {slot['slots']}\n"
        body += f"Start date: {slot['start_date']}\n"
        body += f"Last updated: {ist_time_str}\n\n"
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        print(f"Connecting to SMTP server {smtp_host}:{smtp_port}")
        server = smtplib.SMTP(smtp_host, smtp_port)
        if use_tls:
            server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_pushover_notification(slot_details):
    # Pushover configuration
    pushover_token = os.environ.get('PUSHOVER_TOKEN')
    pushover_user = os.environ.get('PUSHOVER_USER')
    
    if not all([pushover_token, pushover_user]):
        print("Pushover configuration missing. Please set PUSHOVER_TOKEN and PUSHOVER_USER environment variables.")
        return
    
    try:
        # Create message body
        message = "US Visa slots are available!\n\n"
        for slot in slot_details:
            # Parse the createdon string to a datetime object
            gmt_time = datetime.strptime(slot['createdon'], "%a, %d %b %Y %H:%M:%S %Z")
            
            # Convert to IST by adding 5 hours and 30 minutes
            ist_time = gmt_time + timedelta(hours=5, minutes=30)
            
            # Format the IST time back to a string
            ist_time_str = ist_time.strftime("%Y-%m-%d %H:%M:%S")
            
            message += f"Location: {slot['visa_location']}\n"
            message += f"Slots: {slot['slots']}\n"
            message += f"Start: {slot['start_date']}\n"
            message += f"Updated: {ist_time_str}\n\n"

        # Send notification via Pushover
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": pushover_token,
                "user": pushover_user,
                "message": message,
                "title": "US Visa Slots Available!",
                "priority": 1
            }), { "Content-type": "application/x-www-form-urlencoded" })
        
        response = conn.getresponse()
        if response.status == 200:
            print("Pushover notification sent successfully!")
        else:
            print(f"Failed to send Pushover notification. Status: {response.status}")
            
    except Exception as e:
        print(f"Error sending Pushover notification: {e}")

def is_within_duration(date_str):
    try:
        # Get duration in days from environment variable (default to 120 days / 4 months)
        duration_days = int(os.environ.get('VISA_DURATION_DAYS', '120'))
        
        # Parse the date string (e.g., "17 Feb 2026")
        start_date = parser.parse(date_str).date()
        current_date = datetime.now().date()
        end_date = current_date + timedelta(days=duration_days)
        return start_date <= end_date
    except Exception as e:
        print(f"Error parsing date: {e}")
        return False

def read_proxy():
    try:
        proxy_ip = os.environ.get('PROXY_IP')
        proxy_port = os.environ.get('PROXY_PORT')
        
        if proxy_ip and proxy_port:
            return {
                'http': f'http://{proxy_ip}:{proxy_port}',
                'https': f'https://{proxy_ip}:{proxy_port}'
            }
        else:
            print("Proxy configuration not found in environment variables")
    except Exception as e:
        print(f"Error reading proxy configuration: {e}")
    return None

def get_visa_locations():
    # Get locations from environment variables
    consulate_locations_str = os.environ.get('VISA_CONSULATE_LOCATIONS', 'NEW DELHI')
    vac_locations_str = os.environ.get('VISA_VAC_LOCATIONS', 'NEW DELHI VAC,MUMBAI VAC,KOLKATA VAC')
    
    # Split locations by comma and strip whitespace
    consulate_locations = [loc.strip() for loc in consulate_locations_str.split(',')]
    vac_locations = [loc.strip() for loc in vac_locations_str.split(',')]
    
    return consulate_locations, vac_locations

def check_visa_slots():
    url = "https://app.checkvisaslots.com/slots/v3"
    
    api_key = os.environ.get('API_KEY')
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "extversion": "4.6.1",
        "origin": "chrome-extension://beepaenfejnphdgnkmccjcfiieihhogl",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-api-key": api_key
    }

    try:
        # Get proxy configuration
        proxies = read_proxy()
        if proxies:
            print(f"Using proxy: {proxies['http']}")
            # print(f"Request Headers: {headers}")
            response = requests.get(url, headers=headers, proxies=proxies, verify=True)
        else:
            print("No proxy configuration found, connecting directly")
            # print(f"Request Headers: {headers}")
            response = requests.get(url, headers=headers, verify=True)
        response.raise_for_status()
        
        print(f"Status Code: {response.status_code}")
        data = response.json()
        # print("\nRaw Response:")
        # print(json.dumps(data, indent=2))
        
        # Display remaining activity info
        if 'userActivity' in data:
            activity = data['userActivity']
            print("\nUser Activity Status:")
            print(f"Remaining API calls: {activity.get('remaining', 'N/A')}")
            # print(f"Total slots checked: {activity.get('slots', 'N/A')}")
            # print(f"Total retrievals: {activity.get('retrieve', 'N/A')}")
            # print(f"Total uploads: {activity.get('upload', 'N/A')}\n")
        
        if 'slotDetails' in data:
            relevant_slots = []
            
            # First, collect available slots for consulate and VAC locations
            consulate_slots = []
            vac_slots = []
            
            # Get configured locations
            consulate_locations, vac_locations = get_visa_locations()
            
            for slot in data['slotDetails']:
                if slot['slots'] > 0 and 'start_date' in slot:
                    if is_within_duration(slot['start_date']):
                        if slot['visa_location'] in consulate_locations:
                            consulate_slots.append(slot)
                        elif slot['visa_location'] in vac_locations:
                            vac_slots.append(slot)
            
            # Only append slots if both New Delhi and any VAC location have available slots
            if consulate_slots and vac_slots:
                relevant_slots.extend(consulate_slots)
                relevant_slots.extend(vac_slots)
            
            if relevant_slots:
                print("\nFound relevant slots:")
                print(json.dumps(relevant_slots, indent=2))
                send_email(relevant_slots)
                send_pushover_notification(relevant_slots)
            else:
                duration_days = int(os.environ.get('VISA_DURATION_DAYS', '120'))
                duration_months = round(duration_days / 30)  # Approximate months
                print(f"\nNo relevant slots found within {duration_months} months ({duration_days} days)")
                
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    print(f"Checking visa slots at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    check_visa_slots()
