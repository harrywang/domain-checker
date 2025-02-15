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
    
    # Get domains marked as checked in domains.txt
    try:
        with open('domains.txt', 'r') as f:
            for line in f:
                if '#' in line and '✓ checked on' in line:
                    base_name = line.split('#')[0].strip()
                    checked_domains.add(base_name)
    except Exception as e:
        print(f"Error reading domains.txt: {e}")
    
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

# Removed update_domains_file function as we don't need to update domains.txt anymore

def save_domain_status(domain_list, checked_domains):
    # Filter out already checked domains
    new_domains = [d for d in domain_list if d not in checked_domains]
    
    if not new_domains:
        print("No new domains to check!")
        return
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"domain_status_{timestamp}.md"
    
    # Group domains by base name
    base_name_results = {}
    
    for domain in new_domains:
        print(f"Checking {domain}...")
        base_name = domain.split('.')[0]
        if base_name not in base_name_results:
            base_name_results[base_name] = {}
            
        results = check_domain_status(domain)
        if results and 'status' in results:
            for status in results['status']:
                is_available = status.get('summary') != 'active'
                availability = "✅ AVAILABLE" if is_available else "❌ NOT AVAILABLE"
                ext = f".{domain.split('.')[-1]}"
                base_name_results[base_name][ext] = availability
        else:
            ext = f".{domain.split('.')[-1]}"
            base_name_results[base_name][ext] = "⚠️ ERROR"
    
    # Update domains.txt to mark checked domains
    domains_txt_lines = []
    checked_base_names = set(base_name_results.keys())
    
    try:
        with open('domains.txt', 'r') as f:
            for line in f:
                base_name = line.split('#')[0].strip()
                if base_name in checked_base_names:
                    check_date = datetime.now().strftime("%Y-%m-%d")
                    domains_txt_lines.append(f"{base_name:<30} # ✓ checked on {check_date}\n")
                else:
                    domains_txt_lines.append(line if line.endswith('\n') else line + '\n')
        
        with open('domains.txt', 'w') as f:
            f.writelines(domains_txt_lines)
    except Exception as e:
        print(f"Error updating domains.txt: {e}")
    
    with open(filename, 'w') as f:
        f.write("# Domain Status Check\n\n")
        f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        # Write header
        extensions = sorted(list({ext for results in base_name_results.values() for ext in results.keys()}))
        f.write("| Name | " + " | ".join(extensions) + " |\n")
        f.write("|---" + "|---" * len(extensions) + "|\n")
        
        # Write results for each base name
        for base_name in sorted(base_name_results.keys()):
            f.write(f"| {base_name} ")
            for ext in extensions:
                status = base_name_results[base_name].get(ext, "⚠️ N/A")
                f.write(f"| {status} ")
            f.write("|\n")
        
        # Add summary
        f.write(f"\n## Summary\n\n")
        f.write(f"- Total names checked: {len(base_name_results)}\n")
        f.write(f"- Extensions checked: {', '.join(extensions)}\n")
        
        # Add legend
        f.write(f"\n## Legend\n\n")
        f.write("- ✅ AVAILABLE: Domain is available for registration\n")
        f.write("- ❌ NOT AVAILABLE: Domain is already registered\n")
        f.write("- ⚠️ ERROR: Error occurred while checking domain\n")
        f.write("- ⚠️ N/A: Domain was not checked\n")
    
    print(f"\nResults saved to {filename}")
    print("domains.txt updated with check marks")

def main():
    # Define the domain extensions to check
    extensions = ['.ai', '.com']
    
    # Get previously checked domains
    checked_base_names = get_previously_checked_domains()
    
    # Read base names from file
    try:
        with open('domains.txt', 'r') as f:
            base_names = [line.split('#')[0].strip().lower() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading domains.txt: {e}")
        return
    
    # Filter out already checked base names
    base_names_to_check = [name for name in base_names if name not in checked_base_names]
    
    if not base_names_to_check:
        print("All domains have been checked! Check domains.txt for previous results.")
        return
    
    # Generate domain list with all extensions
    domains_to_check = []
    for base_name in base_names_to_check:
        for ext in extensions:
            domains_to_check.append(f"{base_name}{ext}")
    
    print(f"Found {len(base_names)} total names")
    print(f"Skipping {len(checked_base_names)} previously checked names")
    print(f"Checking {len(domains_to_check)} domains ({len(base_names_to_check)} names × {len(extensions)} extensions)...")
    
    # Check domains
    save_domain_status(domains_to_check, set())

if __name__ == "__main__":
    main()
