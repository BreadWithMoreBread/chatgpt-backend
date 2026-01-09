from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Store pending messages
pending_messages = []
responses = {}

@app.route('/')
def home():
    return jsonify({'status': 'Fake ChatGPT Backend Running'})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    # Create message ID
    msg_id = str(int(time.time() * 1000))

    # Store the message
    pending_messages.append({
        'id': msg_id,
        'message': user_message,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

    print(f"\n[NEW MESSAGE] {user_message}")

    # Wait for response from admin (you)
    timeout = 60  # 60 second timeout
    start_time = time.time()

    while msg_id not in responses:
        if time.time() - start_time > timeout:
            return jsonify({'response': 'I apologize, but I\'m experiencing high demand right now. Please try again.'})
        time.sleep(0.5)

    response_text = responses[msg_id]
    del responses[msg_id]

    return jsonify({'response': response_text})

@app.route('/admin')
def admin_panel():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>ChatGPT Admin Panel</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: monospace;
            background: #1a1a1a;
            color: #0f0;
            padding: 20px;
        }
        h1 {
            color: #0f0;
            margin-bottom: 20px;
            text-align: center;
        }
        .alert {
            background: #0a0;
            color: white;
            padding: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }
        .messages {
            background: #000;
            border: 2px solid #0f0;
            padding: 15px;
            margin-bottom: 20px;
            max-height: 400px;
            overflow-y: auto;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            background: #1a1a1a;
            border-left: 3px solid #0f0;
        }
        .timestamp {
            color: #666;
            font-size: 12px;
        }
        .user-msg {
            color: #fff;
            margin: 5px 0;
        }
        .response-box {
            background: #000;
            border: 2px solid #0f0;
            padding: 15px;
        }
        textarea {
            width: 100%;
            height: 100px;
            background: #1a1a1a;
            color: #0f0;
            border: 1px solid #0f0;
            padding: 10px;
            font-family: monospace;
            font-size: 14px;
        }
        button {
            background: #0f0;
            color: #000;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 10px;
            font-family: monospace;
        }
        button:hover {
            background: #0a0;
        }
        .no-messages {
            color: #666;
            text-align: center;
            padding: 20px;
        }
    </style>
</head>
<body>
    <h1>⚡ ChatGPT Admin Panel ⚡</h1>
    <div class="alert">Admin Control Panel - Respond to incoming messages</div>

    <div class="messages" id="messages">
        <div class="no-messages">Waiting for messages...</div>
    </div>

    <div class="response-box">
        <h3>Type Your Response:</h3>
        <textarea id="responseText" placeholder="Type your response here..."></textarea>
        <button onclick="sendResponse()">Send Response</button>
    </div>

    <script>
        let currentMessageId = null;

        async function checkMessages() {
            try {
                const response = await fetch('/admin/pending');
                const data = await response.json();

                const messagesDiv = document.getElementById('messages');

                if (data.messages.length === 0) {
                    messagesDiv.innerHTML = '<div class="no-messages">Waiting for messages...</div>';
                    currentMessageId = null;
                } else {
                    let html = '';
                    data.messages.forEach(msg => {
                        html += `
                            <div class="message">
                                <div class="timestamp">[${msg.timestamp}] Message ID: ${msg.id}</div>
                                <div class="user-msg">USER ASKED: "${msg.message}"</div>
                            </div>
                        `;
                    });
                    messagesDiv.innerHTML = html;

                    // Set current message to respond to
                    currentMessageId = data.messages[0].id;
                }
            } catch (error) {
                console.error('Error fetching messages:', error);
            }
        }

        async function sendResponse() {
            if (!currentMessageId) {
                alert('No message to respond to!');
                return;
            }

            const responseText = document.getElementById('responseText').value.trim();
            if (!responseText) {
                alert('Type a response first!');
                return;
            }

            try {
                await fetch('/admin/respond', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        id: currentMessageId,
                        response: responseText
                    })
                });

                document.getElementById('responseText').value = '';
                alert('Response sent successfully!');
                checkMessages();
            } catch (error) {
                alert('Error sending response!');
            }
        }

        // Check for new messages every second
        setInterval(checkMessages, 1000);
        checkMessages();
    </script>
</body>
</html>
    """

@app.route('/admin/pending')
def get_pending():
    return jsonify({'messages': pending_messages})

@app.route('/admin/respond', methods=['POST'])
def admin_respond():
    data = request.json
    msg_id = data.get('id')
    response_text = data.get('response')

    # Store response
    responses[msg_id] = response_text

    # Remove from pending
    global pending_messages
    pending_messages = [m for m in pending_messages if m['id'] != msg_id]

    print(f"[YOU RESPONDED]: {response_text}")

    return jsonify({'success': True})

if __name__ == '__main__':
    print("=" * 60)
    print("ChatGPT Server Starting")
    print("=" * 60)
    print("\nFrontend: http://localhost:5000")
    print("Admin Panel: http://localhost:5000/admin")
    print("=" * 60)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
