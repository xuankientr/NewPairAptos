#!/usr/bin/env python3
"""
Script để lấy Chat ID từ Telegram Bot
Chạy script này sau khi đã tạo bot và gửi tin nhắn cho bot
"""

import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def get_chat_id(bot_token):
    """Lấy Chat ID từ Telegram Bot API"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("ok"):
            print(f"❌ API Error: {data.get('description', 'Unknown error')}")
            return None
        
        updates = data.get("result", [])
        
        if not updates:
            print("❌ Không tìm thấy tin nhắn nào.")
            print("💡 Hãy gửi tin nhắn cho bot trước khi chạy script này.")
            return None
        
        print("📱 Danh sách Chat ID tìm thấy:")
        print("-" * 50)
        
        chat_ids = set()
        for update in updates:
            message = update.get("message", {})
            chat = message.get("chat", {})
            
            if chat:
                chat_id = chat.get("id")
                chat_type = chat.get("type", "unknown")
                chat_title = chat.get("title", chat.get("first_name", "Unknown"))
                
                if chat_id:
                    chat_ids.add((chat_id, chat_type, chat_title))
        
        for chat_id, chat_type, chat_title in sorted(chat_ids):
            print(f"Chat ID: {chat_id}")
            print(f"Type: {chat_type}")
            print(f"Name/Title: {chat_title}")
            print("-" * 30)
        
        if len(chat_ids) == 1:
            chat_id = list(chat_ids)[0][0]
            print(f"✅ Sử dụng Chat ID này: {chat_id}")
            return chat_id
        else:
            print("💡 Có nhiều chat, hãy chọn Chat ID phù hợp.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi kết nối: {e}")
        return None
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return None

def main():
    print("🤖 Telegram Chat ID Finder")
    print("=" * 40)
    
    # Lấy bot token từ environment hoặc input
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        bot_token = input("Nhập Bot Token: ").strip()
    
    if not bot_token:
        print("❌ Bot Token không được để trống!")
        sys.exit(1)
    
    print(f"🔍 Đang tìm Chat ID cho bot...")
    
    chat_id = get_chat_id(bot_token)
    
    if chat_id:
        print("\n" + "=" * 40)
        print("✅ THÀNH CÔNG!")
        print(f"📋 Thêm dòng này vào file .env:")
        print(f"TELEGRAM_CHAT_ID={chat_id}")
        
        # Tự động cập nhật .env nếu file tồn tại
        if os.path.exists('.env'):
            try:
                with open('.env', 'r') as f:
                    content = f.read()
                
                if 'TELEGRAM_CHAT_ID=' in content:
                    # Update existing
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith('TELEGRAM_CHAT_ID='):
                            lines[i] = f'TELEGRAM_CHAT_ID={chat_id}'
                            break
                    content = '\n'.join(lines)
                else:
                    # Add new
                    content += f'\nTELEGRAM_CHAT_ID={chat_id}'
                
                with open('.env', 'w') as f:
                    f.write(content)
                
                print("✅ Đã tự động cập nhật file .env")
                
            except Exception as e:
                print(f"⚠️ Không thể tự động cập nhật .env: {e}")
    else:
        print("\n❌ Không thể lấy Chat ID.")
        print("💡 Hướng dẫn:")
        print("1. Đảm bảo bot token đúng")
        print("2. Gửi tin nhắn cho bot trước")
        print("3. Chạy lại script này")

if __name__ == "__main__":
    main()
