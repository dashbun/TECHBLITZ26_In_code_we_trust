import os
import json
import hashlib
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

from src.database.supabase_client import supabase
from src.knowledge.vector_store import ProductSearch
from src.agents.lead_scorer import score_lead
from src.utils.logger import log

# Load products
with open('src/knowledge/aura_products.json', 'r') as f:
    products_data = json.load(f)
product_search = ProductSearch(products_data['products'])

# User conversation state (simple dict for demo)
user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user = update.effective_user
    welcome_msg = (
        f"👋 Hello {user.first_name}! Welcome to Aura Fashion Assistant.\n\n"
        "I can help you find the perfect outfit. Tell me what you're looking for:\n"
        "• Casual wear\n• Party dresses\n• Footwear\n• Accessories\n\n"
        "Or just describe your style and occasion!"
    )
    await update.message.reply_text(welcome_msg)
    
    # Initialize user state
    user_state[user.id] = {
        'stage': 'browsing',
        'preferences': [],
        'cart': []
    }

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages"""
    user = update.effective_user
    message = update.message.text
    user_id = user.id
    
    # Initialize state if needed
    if user_id not in user_state:
        user_state[user_id] = {'stage': 'browsing', 'preferences': []}
    
    # Search products based on message
    results = product_search.search(message, limit=3)
    
    if results:
        # Create product cards
        response = "Based on what you said, here are some options:\n\n"
        keyboard = []
        
        for product in results:
            response += f"✨ *{product['brand']} - {product['title']}*\n"
            response += f"   ₹{product['price']} ({product['discount']}% off)\n"
            response += f"   ⭐ {product['rating']} | {product['category']}\n\n"
            
            # Add button for this product
            keyboard.append([
                InlineKeyboardButton(
                    f"🔍 View {product['brand']} {product['title'][:20]}",
                    callback_data=f"view_{product['id']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🛍️ Show More", callback_data="more")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            response,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # Store last search in context
        context.user_data['last_search'] = message
        context.user_data['last_results'] = results
        
    else:
        # No matches - ask clarifying questions
        await update.message.reply_text(
            "I couldn't find exact matches. Could you tell me more?\n"
            "• What occasion? (casual/party/work)\n"
            "• Preferred colors?\n"
            "• Budget range?"
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith('view_'):
        product_id = data.replace('view_', '')
        
        # Find product
        with open('src/knowledge/aura_products.json', 'r') as f:
            products = json.load(f)['products']
        
        product = next((p for p in products if p['id'] == product_id), None)
        
        if product:
            # Show product details
            detail_msg = (
                f"📦 *{product['brand']} - {product['title']}*\n\n"
                f"💰 Price: ₹{product['price']} "
                f"(was ₹{product['original_price']})\n"
                f"🏷️ Discount: {product['discount']}% OFF\n"
                f"⭐ Rating: {product['rating']} ({product['review_count']} reviews)\n"
                f"📂 Category: {product['category']} › {product['subcategory']}\n\n"
                f"📝 *Description:*\n{product['description']}\n\n"
                f"🏷️ Tags: {', '.join(product['tags'])}"
            )
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🛒 Interested - Contact Me", 
                                       callback_data=f"lead_{product_id}")
                ],
                [
                    InlineKeyboardButton("🔙 Back to Results", 
                                       callback_data="back_to_results")
                ]
            ])
            
            await query.edit_message_text(
                detail_msg,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
    elif data.startswith('lead_'):
        product_id = data.replace('lead_', '')
        
        # Create lead in database
        user = update.effective_user
        
        # Get product details
        with open('src/knowledge/aura_products.json', 'r') as f:
            products = json.load(f)['products']
        
        product = next((p for p in products if p['id'] == product_id), None)
        
        # Generate lead hash
        lead_hash = hashlib.sha256(
            f"{user.id}_{product_id}_{datetime.now().date()}".encode()
        ).hexdigest()
        
        # Store lead
        lead_data = {
            'lead_hash': lead_hash,
            'name': user.full_name or user.first_name,
            'phone': None,  # Will ask later
            'source': 'telegram_user',
            'conversation_history': [{'time': str(datetime.now()), 'msg': f"Interested in {product['title']}"}],
            'preferred_categories': [product['category']],
            'interested_products': [product_id],
            'purchase_intent': 35,  # Base score
            'lot_size': 1,  # Assuming single item initially
            'est_profit': product['price'] * (product.get('profit_margin', 30)/100),
            'customer_value_score': 20,
            'status': 'queued'
        }
        
        try:
            result = supabase.table('leads').insert(lead_data).execute()
            
            # Queue for scoring
            await query.edit_message_text(
                "✅ Thanks for your interest! Our team will contact you shortly.\n"
                "In the meantime, feel free to explore more products!"
            )
            
            # Log to rep channel
            log('info', 'new_lead_from_telegram', 
                user=user.first_name, 
                product=product['title'])
            
        except Exception as e:
            await query.edit_message_text(
                "⚠️ There was an error. Please try again or contact support."
            )
            log('error', 'lead_creation_failed', error=str(e))
    
    elif data == "more":
        # Show more results from last search
        last_search = context.user_data.get('last_search', '')
        if last_search:
            results = product_search.search(last_search, limit=10)
            # Format and send...
            await query.edit_message_text("More results feature coming soon!")
    
    elif data == "back_to_results":
        # Show last results again
        await query.edit_message_text("Returning to results...")

async def collect_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect phone number for follow-up"""
    # Implementation for collecting contact info
    pass

def main():
    """Start the bot"""
    token = os.getenv('TELEGRAM_USER_BOT_TOKEN')
    application = Application.builder().token(token).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start
    application.run_polling()

if __name__ == '__main__':
    main()
