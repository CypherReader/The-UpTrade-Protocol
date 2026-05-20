# Autonomous Bartering Agent

This is an autonomous trading AI agent inspired by the "One Red Paperclip" story. It utilizes Google Gemini, Google Universal Commerce Protocol (UCP), and Agent Payment Protocol 2 (AP2) to autonomously search for trade opportunities, evaluate them, and reach out to sellers to negotiate trades up to a final target goal.

## Setup Instructions

### 1. Configure the Environment
1. In the root directory, create a `.env` file by copying the example:
   `cp .env.example .env`
2. Open the `.env` file and fill in your actual credentials:
   - `GEMINI_API_KEY`: Your API key from Google AI Studio.
   - `SMTP_USERNAME` / `SMTP_PASSWORD`: If using Gmail to send emails, provide your Gmail address and a generated "App Password".
   - `DRY_RUN`: Keep this set to `True` for simulation mode.

### 2. Run via Python (Local)
Ensure you have Python 3.11+ installed.
1. Create a virtual environment and install dependencies:
   `virtualenv venv`
   `source venv/bin/activate`
   `pip install -r requirements.txt`
2. Run the main agent script:
   `python main.py`
   *The database (`agent.db`) will be automatically initialized with the starting and target items on the first run.*

### 3. Run via Docker
1. Build the Docker image:
   `docker build -t bartering-agent .`
2. Run the container, passing in your environment variables:
   `docker run --env-file .env bartering-agent`
