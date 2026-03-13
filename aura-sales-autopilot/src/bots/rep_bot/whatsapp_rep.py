from twilio.rest import Client
from flask import Flask, request
from dotenv import load_dotenv
import os
from src.database.supabase_client import SupabaseClient

load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
whatsapp_number = os.getenv('WHATSAPP_REP_NUMBER')

db = SupabaseClient()
client = Client(account_sid, auth_token)

app = Flask(__name__)

@app.route("/whatsapp_rep", methods=['POST'])
def whatsapp_rep_webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    
    if "leads" in incoming_msg:
        leads = db.get_leads(status="new")
        msg_body = "\\n".join([f"{l['name']}: {l['score']}" for l in leads])
        resp_msg = f"Your leads:\\n{msg_body}"
    else:
        resp_msg = "Commands: 'leads', 'assign [lead_id]'"
    
    message = client.messages.create(
        body=resp_msg,
        from_=whatsapp_number,
        to=from_number
    )
    return "OK"

if __name__ == "__main__":
    app.run(port=5001)
