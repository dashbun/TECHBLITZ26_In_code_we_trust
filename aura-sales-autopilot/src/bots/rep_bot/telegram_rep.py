import os
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from src.database.supabase_client import supabase
from src.utils.logger import log
from src.agents.sequence_engine import start_sequence

# Constants
REP_CHAT_ID = os.getenv('TELEGRAM_REP_CHAT_ID')
SCORE_HIGH = int(os.getenv('SCORE_HIGH', 70))
SCORE_MEDIUM = int(os.getenv('SCORE_MEDIUM', 40))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command for rep bot"""
    if str(update.effective_chat.id) != REP_CHAT_ID:
        await update.message.reply_text("Unauthorized")
        return
    
    await update.message.reply_text(
        "📊 *Aura Sales Commander*\n\n"
        "Commands:\n"
        "/pipeline - View lead pipeline\n"
        "/top - Show top 5 hottest leads\n"
        "/stats - Conversion stats\n"
        "/pending - Leads awaiting approval\n\n"
        "I'll notify you instantly when hot leads come in! 🔥",
        parse_mode='Markdown'
    )

async def pipeline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show pipeline summary"""
    if str(update.effective_chat.id) != REP_CHAT_ID:
        return
    
    # Query leads by status
    today = datetime.now().date().isoformat()
    
    result = supabase.table('leads')\
        .select('status', count='exact')\
        .gte('created_at', today)\
        .execute()
    
    # Count manually (simplified)
    counts = {
        'queued': 0,
        'pending_approval': 0,
        'approved': 0,
        'in_sequence': 0,
        'converted': 0,
        'rejected': 0
    }
    
    for lead in result.data:
        status = lead['status']
        if status in counts:
            counts[status] += 1
    
    msg = (
        "📈 *Today's Pipeline*\n\n"
        f"🕒 Queued: {counts['queued']}\n"
        f"⏳ Pending Approval: {counts['pending_approval']}\n"
        f"✅ Approved: {counts['approved']}\n"
        f"🔄 In Sequence: {counts['in_sequence']}\n"
        f"🎉 Converted: {counts['converted']}\n"
        f"❌ Rejected: {counts['rejected']}\n\n"
        "Type /pending to see leads needing approval"
    )
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show pending approvals"""
    if str(update.effective_chat.id) != REP_CHAT_ID:
        return
    
    pending = supabase.table('leads')\
        .select('*')\
        .eq('status', 'pending_approval')\
        .order('score', desc=True)\
        .limit(10)\
        .execute()
    
    if not pending.data:
        await update.message.reply_text("No pending approvals! ✅")
        return
    
    for lead in pending.data[:5]:  # Show top 5
        msg = (
            f"👤 *{lead['name']}*\n"
            f"📊 Score: {lead['score']}/100 ({lead['icp_fit']} fit)\n"
            f"💰 Est Profit: ₹{lead.get('est_profit', 'N/A')}\n"
            f"📦 Lot Size: {lead.get('lot_size', 1)} items\n"
            f"📱 Source: {lead['source']}\n"
            f"🆔 `{lead['id'][:8]}...`"
        )
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"app_{lead['id']}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"rej_{lead['id']}"),
                InlineKeyboardButton("⏰ Snooze", callback_data=f"snooze_{lead['id']}")
            ],
            [InlineKeyboardButton("📋 Details", callback_data=f"detail_{lead['id']}")]
        ])
        
        await update.message.reply_text(msg, reply_markup=keyboard, parse_mode='Markdown')

async def top_leads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show top leads by score"""
    if str(update.effective_chat.id) != REP_CHAT_ID:
        return
    
    top = supabase.table('leads')\
        .select('*')\
        .in_('status', ['pending_approval', 'approved'])\
        .order('score', desc=True)\
        .limit(5)\
        .execute()
    
    if not top.data:
        await update.message.reply_text("No leads yet!")
        return
    
    msg = "🔥 *TOP 5 HOTTEST LEADS*\n\n"
    for i, lead in enumerate(top.data, 1):
        msg += (
            f"{i}. *{lead['name']}* - {lead['score']}/100\n"
            f"   💰 ₹{lead.get('est_profit', 'N/A')} | {lead.get('lot_size', 1)} items\n"
            f"   🏷️ {lead.get('preferred_categories', ['N/A'])[0] if lead.get('preferred_categories') else 'N/A'}\n\n"
        )
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def handle_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle approve/reject callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith('app_'):
        lead_id = data.replace('app_', '')
        
        # Transition in DB
        result = supabase.rpc(
            'transition_lead',
            {
                'p_lead_id': lead_id,
                'p_new_status': 'approved',
                'p_actor': 'rep_telegram'
            }
        ).execute()
        
        if result.data:
            await query.edit_message_text(
                f"{query.message.text}\n\n✅ *APPROVED* - Sequence will start shortly",
                parse_mode='Markdown'
            )
            
            # Trigger sequence (async)
            asyncio.create_task(start_sequence(lead_id))
            
            log('ok', 'lead_approved', lead_id=lead_id[:8], rep='telegram')
        else:
            await query.edit_message_text(
                f"{query.message.text}\n\n❌ *Transition failed* - Already processed",
                parse_mode='Markdown'
            )
    
    elif data.startswith('rej_'):
        lead_id = data.replace('rej_', '')
        
        result = supabase.rpc(
            'transition_lead',
            {
                'p_lead_id': lead_id,
                'p_new_status': 'rejected',
                'p_actor': 'rep_telegram'
            }
        ).execute()
        
        if result.data:
            await query.edit_message_text(
                f"{query.message.text}\n\n❌ *REJECTED*",
                parse_mode='Markdown'
            )
            log('info', 'lead_rejected', lead_id=lead_id[:8])

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show conversion stats"""
    if str(update.effective_chat.id) != REP_CHAT_ID:
        return
    
    # Get last 30 days stats
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
    
    result = supabase.table('state_transitions')\
        .select('*')\
        .gte('created_at', thirty_days_ago)\
        .execute()
    
    transitions = result.data
    
    total_approved = sum(1 for t in transitions if t['to_state'] == 'approved')
    total_converted = sum(1 for t in transitions if t['to_state'] == 'converted')
    
    conversion_rate = (total_converted / total_approved * 100) if total_approved > 0 else 0
    
    msg = (
        "📊 *30-Day Stats*\n\n"
        f"✅ Approved: {total_approved}\n"
        f"🎉 Converted: {total_converted}\n"
        f"📈 Conversion Rate: {conversion_rate:.1f}%\n"
        f"💰 Est. Revenue: ₹{total_converted * 1500}"  # Rough estimate
    )
    
    await update.message.reply_text(msg, parse_mode='Markdown')

def main():
    """Start rep bot"""
    token = os.getenv('TELEGRAM_REP_BOT_TOKEN')
    application = Application.builder().token(token).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pipeline", pipeline))
    application.add_handler(CommandHandler("pending", pending))
    application.add_handler(CommandHandler("top", top_leads))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CallbackQueryHandler(handle_approval))
    
    # Start polling
    application.run_polling()

if __name__ == '__main__':
    main()
