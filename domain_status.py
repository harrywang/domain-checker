import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime
import glob

# Load environment variables
load_dotenv()

def get_previously_checked_domains():
    checked_domains = set()
    # Find all domain status files
    for status_file in glob.glob("domain_status_*.txt"):
        try:
            with open(status_file, 'r') as f:
                for line in f:
                    if line.startswith("Domain: "):
                        domain = line.strip().replace("Domain: ", "")
                        checked_domains.add(domain)
        except Exception as e:
            print(f"Error reading {status_file}: {e}")
    return checked_domains

def check_domain_status(domain):
    url = "https://domainr.p.rapidapi.com/v2/status"
    
    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
        "x-rapidapi-host": os.getenv('RAPIDAPI_HOST')
    }
    
    params = {
        "domain": domain
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def update_domains_file(domain_results):
    # Read existing domains and their comments
    existing_domains = {}
    try:
        with open('domains.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('#', 1)
                domain = parts[0].strip()
                comment = parts[1].strip() if len(parts) > 1 else ""
                existing_domains[domain] = comment
    except Exception as e:
        print(f"Error reading domains.txt: {e}")
        return

    # Update with new results
    with open('domains.txt', 'w') as f:
        for domain in existing_domains:
            if domain in domain_results:
                status = domain_results[domain]
                f.write(f"{domain:<20} # {status}\n")
            else:
                comment = existing_domains[domain]
                f.write(f"{domain:<20} {f'# {comment}' if comment else ''}\n")

def save_domain_status(domain_list, checked_domains):
    # Filter out already checked domains
    new_domains = [d for d in domain_list if d not in checked_domains]
    
    if not new_domains:
        print("No new domains to check!")
        return
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"domain_status_{timestamp}.txt"
    
    # Store results for updating domains.txt
    domain_results = {}
    
    with open(filename, 'w') as f:
        f.write(f"Food-related .ai Domain Status Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 50 + "\n\n")
        f.write(f"Checking {len(new_domains)} new domains\n")
        f.write(f"Skipped {len(domain_list) - len(new_domains)} previously checked domains\n\n")
        
        for domain in new_domains:
            results = check_domain_status(domain)
            if results and 'status' in results:
                for status in results['status']:
                    is_available = status.get('summary') != 'active'
                    availability = "AVAILABLE" if is_available else "NOT AVAILABLE"
                    f.write(f"Domain: {status['domain']}\n")
                    f.write(f"Status: {status['summary']}\n")
                    f.write(f"Availability: {availability}\n")
                    f.write("-" * 30 + "\n")
                    # Store result for updating domains.txt
                    domain_results[domain] = f"Status: {status['summary']}, {availability}"
            else:
                f.write(f"Error checking domain: {domain}\n")
                f.write("-" * 30 + "\n")
                domain_results[domain] = "Error checking domain"
    
    print(f"Results saved to {filename}")
    
    # Update domains.txt with results
    update_domains_file(domain_results)
    print("Updated domains.txt with availability information")

def main():
    # Read domains from file
    try:
        with open('domains.txt', 'r') as f:
            domains_to_check = [line.split('#')[0].strip() for line in f if line.strip() and not line.strip().startswith('#')]
    except Exception as e:
        print(f"Error reading domains.txt: {e}")
        return

    # Get previously checked domains
    checked_domains = get_previously_checked_domains()
    
    # Check domains
    save_domain_status(domains_to_check, checked_domains)

if __name__ == "__main__":
    main()
