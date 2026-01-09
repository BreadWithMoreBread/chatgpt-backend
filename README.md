# ChatGPT-style Chat Backend

A Flask backend for a chat application with an admin interface.

## Features
- REST API for chat messages
- Admin panel for managing responses
- Real-time message handling

## Deployment

### Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

### Run Locally
```bash
pip install -r requirements.txt
python fake_gpt_server.py
```

### Deploy to Render
1. Connect this repo to Render
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `gunicorn fake_gpt_server:app`

## API Endpoints
- `GET /` - Health check
- `POST /api/chat` - Send chat message
- `GET /admin` - Admin interface
- `GET /admin/pending` - Get pending messages
- `POST /admin/respond` - Submit response

## Environment Variables
- `PORT` - Server port (default: 10000)
