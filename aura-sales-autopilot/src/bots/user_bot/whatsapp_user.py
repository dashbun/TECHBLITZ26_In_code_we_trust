from twilio.rest import Client
from flask import Flask, request
from dotenv import load_dotenv
import os
from src.database.supabase_client import SupabaseClient
from src.agents.lead_scorer import LeadScorer

load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
whatsapp_number = os.getenv('WHATSAPP_FROM_NUMBER')

db = SupabaseClient()
scorer = LeadScorer()

app = Flask(__name__)
client = Client(account_sid, auth_token)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    
    # Parse lead data
    lead_data = {
        "name": "Jane Doe",  # Extract
        "email": "jane@example.com",
        "phone": from_number,
        "company": "Sample Corp",
        "source": "whatsapp_user"
    }
    
    score = scorer.score_lead(lead_data)
    lead_data["score"] = score
    db.create_lead(lead_data)
    
    message = client.messages.create(
        body=f"Lead captured! Score: {score}/100",
        from_=whatsapp_number,
        to=from_number
    )
    return "OK"

if __name__ == "__main__":
    app.run(port=5000)
