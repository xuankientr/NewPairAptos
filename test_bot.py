#!/usr/bin/env python3
"""
Script test để kiểm tra bot Telegram hoạt động
"""

import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

async def test_bot():
    """Test kết nối và gửi tin nhắn test"""
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN không tìm thấy trong .env")
        return False
    
    if not chat_id:
        print("❌ TELEGRAM_CHAT_ID không tìm thấy trong .env")
        return False
    
    print("🤖 Testing Telegram Bot...")
    print(f"Bot Token: {bot_token[:10]}...")
    print(f"Chat ID: {chat_id}")
    
    try:
        bot = Bot(token=bot_token)
        
        # Test 1: Get bot info
        print("\n📋 Test 1: Getting bot info...")
        bot_info = await bot.get_me()
        print(f"✅ Bot Name: {bot_info.first_name}")
        print(f"✅ Bot Username: @{bot_info.username}")
        
        # Test 2: Send test message
        print("\n📤 Test 2: Sending test message...")
        test_message = """
🧪 **TEST MESSAGE**

✅ Bot đang hoạt động bình thường!
🔄 Aptos Pool Monitor sẵn sàng theo dõi pool mới.

⏰ Thời gian test: {time}
        """.format(time=asyncio.get_event_loop().time())
        
        message = await bot.send_message(
            chat_id=chat_id,
            text=test_message,
            parse_mode='Markdown'
        )
        
        print(f"✅ Message sent successfully!")
        print(f"✅ Message ID: {message.message_id}")
        
        # Test 3: Send sample pool notification
        print("\n📊 Test 3: Sending sample pool notification...")
        sample_notification = """
🆕 **NEW APTOS POOL DETECTED** (TEST)

🏷️ **Pool Name:** APT/USDC
🔗 **Contract:** `0x1234567890abcdef1234567890abcdef12345678`
🆔 **Pool ID:** `aptos_0x1234567890abcdef1234567890abcdef12345678`
💱 **Tokens:** APT / USDC
🏪 **DEX:** PancakeSwap
⏰ **Created:** 2024-01-01 12:00:00 UTC

🔍 **View on GeckoTerminal:**
https://www.geckoterminal.com/aptos/pools/0x1234567890abcdef1234567890abcdef12345678

⚠️ *Đây là tin nhắn test*
        """
        
        await bot.send_message(
            chat_id=chat_id,
            text=sample_notification,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        
        print("✅ Sample notification sent successfully!")
        
        print("\n🎉 TẤT CẢ TEST THÀNH CÔNG!")
        print("✅ Bot sẵn sàng để chạy monitor")
        return True
        
    except TelegramError as e:
        print(f"\n❌ Telegram Error: {e}")
        if "chat not found" in str(e).lower():
            print("💡 Chat ID có thể không đúng. Hãy chạy get_chat_id.py để lấy Chat ID mới.")
        elif "unauthorized" in str(e).lower():
            print("💡 Bot Token có thể không đúng. Hãy kiểm tra lại Bot Token.")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

async def main():
    print("🧪 Telegram Bot Test")
    print("=" * 40)
    
    success = await test_bot()
    
    if success:
        print("\n" + "=" * 40)
        print("✅ Bot test hoàn tất!")
        print("🚀 Bạn có thể chạy: python aptos_pool_monitor.py")
    else:
        print("\n" + "=" * 40)
        print("❌ Bot test thất bại!")
        print("💡 Hãy kiểm tra lại cấu hình trong file .env")

if __name__ == "__main__":
    asyncio.run(main())
