# Telephonic AI Agent

A real-time AI voice agent built using **LiveKit**, **VoBiz SIP trunk** and **Google Gemini Realtime** for handling phone conversations.

The agent can make outbound calls using an **Indian phone number** through the configured **VoBiz SIP trunk** and have a real-time conversation with the caller.

## Tech Stack

* Python
* LiveKit Agents
* LiveKit SIP
* Google Gemini Realtime
* VoBiz SIP Trunk

## Project Structure

```text
.
├── agent.py
├── test_outbound.py
├── .env
├── requirements.txt
└── README.md
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add the required LiveKit and Google API credentials.

## Run Agent

```bash
python agent.py dev
```

## Make an Outbound Call

Configure the trunk ID and Indian phone number in `test_outbound.py`:

```python
AGENT_NAME = "telephonic-agent"
TRUNK_ID = "your_trunk_id"
PHONE_NUMBER = "+91XXXXXXXXXX"
```

Run:

```bash
python test_outbound.py
```

## SIP Configuration

The project uses a **LiveKit outbound SIP trunk with VoBiz** to make calls from an Indian phone number.

### Call Flow

```text
test_outbound.py
       ↓
LiveKit API
       ↓
LiveKit SIP
       ↓
VoBiz SIP Trunk
       ↓
Indian Phone Number
       ↓
AI Voice Agent
```
