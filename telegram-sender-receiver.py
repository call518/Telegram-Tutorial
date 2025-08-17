import asyncio
import signal
import sys
from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv
import os

load_dotenv()

## Bot-Name: chatbot
## Bot-Username: @call518Bot
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
ALLOWED_CHAT_IDS = {TELEGRAM_CHAT_ID}

## Bot-Name: Perplexis
## Bot-Username: @Perplexis_Bot
async def send_message(msg: str) -> None:
    msg = escape_markdown(msg, version=2)
    bot = Bot(token=TELEGRAM_TOKEN)
    async with bot:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=msg,
            parse_mode=ParseMode.MARKDOWN_V2,
        )

### 콘솔에 출력
async def log_and_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 디버깅을 위해 전체 업데이트 정보 출력
    print(f"[DEBUG] Received update: {update}")
    
    # 메시지가 없는 경우 처리
    if not update.message:
        print("[DEBUG] No message in update")
        return
        
    chat_title = update.effective_chat.title or "No Title"
    chat_id = update.effective_chat.id
    user = update.effective_user.username or update.effective_user.id
    message = update.message.text
    chat_type = update.effective_chat.type
    
    print(f"[DEBUG] Chat Type: {chat_type}")
    print(f"[DEBUG] Chat ID: {chat_id}, Allowed: {ALLOWED_CHAT_IDS}")
    
    if chat_id not in ALLOWED_CHAT_IDS:
        print(f"[Telegram - Ignored message]\nChat-Title: {chat_title}\nChat-ID: {chat_id}\nUser: {user}\nMessage: {message}\nChat-Type: {chat_type}\n", flush=True)
        return # 응답하지 않고 무시
    
    print(f"[Telegram - Received message]\nChat-Title: {chat_title}\nChat-ID: {chat_id}\nUser: {user}\nMessage: {message}\nChat-Type: {chat_type}\n", flush=True)
    
    ### 메세지 발송 사용자를 특정해서 응답
    await update.message.reply_text(f"특정 사용자 응답: {message}")
    
    ### reply 대신 전체 채팅 대상 메시지 전송
    await context.bot.send_message(
        # chat_id=update.effective_chat.id,
        chat_id=chat_id,
        text=f"전체 사용자 응답: {message}",
        parse_mode=ParseMode.MARKDOWN_V2
        # parse_mode, disable_web_page_preview 등 추가 옵션도 필요 시 설정 가능
    )

### 그룹에서 멘션된 메시지 처리
async def handle_mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """봇이 멘션된 경우 처리"""
    chat_title = update.effective_chat.title or "No Title"
    chat_id = update.effective_chat.id
    user = update.effective_user.username or update.effective_user.id
    message = update.message.text
    chat_type = update.effective_chat.type
    
    print(f"[Telegram - Mention Received]\nChat-Title: {chat_title}\nChat-ID: {chat_id}\nUser: {user}\nMessage: {message}\nChat-Type: {chat_type}\n", flush=True)
    
    if chat_id in ALLOWED_CHAT_IDS:
        await update.message.reply_text(f"멘션 응답: {message}")

### 모든 업데이트 로깅 (디버깅용)
async def log_all_updates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """모든 업데이트를 로깅 (디버깅 목적)"""
    if update.message:
        chat_title = update.effective_chat.title or "No Title"
        chat_id = update.effective_chat.id
        user = update.effective_user.username or str(update.effective_user.id)
        message = update.message.text or "[Non-text message]"
        chat_type = update.effective_chat.type
        
        print(f"[ALL UPDATES]\nChat-Title: {chat_title}\nChat-ID: {chat_id}\nUser: {user}\nMessage: {message}\nChat-Type: {chat_type}\n", flush=True)

### /start 명령 액션
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_type = update.effective_chat.type
    print(f"[DEBUG] Start command from {chat_type} chat")
    await update.message.reply_text("Bot is alive! Send me messages.")

### 에러 핸들러 추가
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """에러 발생 시 로그 출력"""
    print(f"Update {update} caused error {context.error}")

def main():    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    ### 핸들러는 등록 순서대로 매칭되며, 매칭된 첫 번째 핸들러만 실행되는 "first match wins" 방식

    # (1) /start 명령 핸들러 등록 : /start 명령 왔을 때 start_command 함수 호출
    app.add_handler(CommandHandler("start", start_command))

    # (2) 봇 멘션 처리 핸들러 (그룹에서 @봇이름으로 멘션된 경우)
    app.add_handler(MessageHandler(filters.Entity("mention"), handle_mention))

    # (3) 일반 텍스트 메시지 핸들러 (모든 메시지 - 개인 채팅 및 그룹)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_and_reply))

    # (4) 모든 업데이트 로깅 (디버깅용 - 가장 마지막에)
    app.add_handler(MessageHandler(filters.ALL, log_all_updates))

    # (5) 에러 핸들러 등록
    app.add_error_handler(error_handler)

    # 시그널 핸들러 설정 (안전한 종료)
    def signal_handler(signum, frame):
        print("\nBot stopping gracefully...")
        app.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # 종료 신호

    # 백그라운드에서 Polling 시작
    print("Bot started. Press Ctrl+C to stop.")
    try:
        app.run_polling()
    except Exception as e:
        print(f"Bot stopped with error: {e}")
    finally:
        print("Bot stopped.")


if __name__ == "__main__":
    main()