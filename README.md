# Domain Checker

A Python tool to check domain availability using the Domainr API, specifically designed to check `.ai` domain names.

## Features

- Check domain availability using the Domainr API
- Save domain status results with timestamps
- Track previously checked domains to avoid redundant API calls
- Update domain status in a master list (`domains.txt`)
- Handle rate limiting and API errors gracefully

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/domain-checker.git
cd domain-checker
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your RapidAPI credentials:
```
RAPIDAPI_KEY=your_api_key_here
RAPIDAPI_HOST=domainr.p.rapidapi.com
```

To get your API credentials:
1. Sign up at [RapidAPI](https://rapidapi.com)
2. Subscribe to the [Domainr API](https://rapidapi.com/domainr/api/domainr)
3. Copy your API key from the RapidAPI dashboard

## Usage

### Checking Domain Availability

1. Add domains to check in `domains.txt`, one per line:
```
example.ai
test.ai
myapp.ai
```

2. Run the domain status checker:
```bash
python domain_status.py
```

The script will:
- Check each domain's availability
- Save results to a timestamped file (e.g., `domain_status_20241211_084738.txt`)
- Update `domains.txt` with availability status as comments

### Understanding Results

Domain statuses can be:
- `active, NOT AVAILABLE`: Domain is in use
- `inactive, AVAILABLE`: Domain might be available for registration
- `parked, AVAILABLE`: Domain might be available for purchase

Results are saved in two formats:
1. Timestamped results file (e.g., `domain_status_20241211_084738.txt`)
2. Updated `domains.txt` with status comments

Example `domains.txt` with status:
```
example.ai           # Status: active, NOT AVAILABLE
test.ai             # Status: inactive, AVAILABLE
myapp.ai            # Status: parked, AVAILABLE
```

## Files

- `domain_status.py`: Main script for checking domain availability
- `domain_search.py`: Helper functions for API interactions
- `domains.txt`: Master list of domains to check
- `requirements.txt`: Python dependencies
- `.env`: API credentials (not tracked in git)

## Dependencies

- python-dotenv
- requests

## Notes

- The Domainr API has rate limits based on your subscription plan
- The script includes error handling and rate limit management
- Previously checked domains are skipped to avoid redundant API calls
- Results are always saved with timestamps for historical tracking
