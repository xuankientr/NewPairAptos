# Aptos Pool Monitor Bot

Bot Telegram tự động thông báo khi có pool mới được tạo trên mạng Aptos.

## Tính năng

- 🔄 Tự động theo dõi pool mới trên Aptos mỗi 60 giây
- 📱 Gửi thông báo qua Telegram khi phát hiện pool mới
- 📊 Hiển thị thông tin chi tiết: tên pool, contract address, tokens, DEX, thời gian tạo
- 🔗 Link trực tiếp đến GeckoTerminal để xem chi tiết
- 📝 Ghi log hoạt động và lỗi
- 🚫 Tránh thông báo trùng lặp

## Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd NewPairAptos
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Tạo Telegram Bot

1. Mở Telegram và tìm @BotFather
2. Gửi `/newbot` và làm theo hướng dẫn
3. Lưu lại Bot Token

### 4. Lấy Chat ID

**Cách 1: Sử dụng bot để lấy Chat ID**
1. Thêm bot vào group/channel hoặc chat riêng
2. Gửi tin nhắn bất kỳ cho bot
3. Truy cập: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Tìm `chat.id` trong response

**Cách 2: Sử dụng @userinfobot**
1. Tìm @userinfobot trên Telegram
2. Gửi `/start` để lấy User ID của bạn

### 5. Cấu hình Environment Variables

1. Copy file `.env.example` thành `.env`:
```bash
cp .env.example .env
```

2. Chỉnh sửa file `.env`:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token
TELEGRAM_CHAT_ID=your_actual_chat_id
```

## Sử dụng

### Chạy bot
```bash
python aptos_pool_monitor.py
```

### Chạy trong background (Linux/Mac)
```bash
nohup python aptos_pool_monitor.py &
```

### Chạy với systemd (Linux)
Tạo file service:
```bash
sudo nano /etc/systemd/system/aptos-monitor.service
```

Nội dung:
```ini
[Unit]
Description=Aptos Pool Monitor Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/your/project
ExecStart=/usr/bin/python3 /path/to/your/project/aptos_pool_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Kích hoạt service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable aptos-monitor.service
sudo systemctl start aptos-monitor.service
```

## Cấu trúc thông báo

Bot sẽ gửi thông báo với format:
```
🆕 NEW APTOS POOL DETECTED

🏷️ Pool Name: [Tên pool]
🔗 Contract: [Địa chỉ contract]
🆔 Pool ID: [ID pool]
💱 Tokens: [Token A / Token B]
🏪 DEX: [Tên DEX]
⏰ Created: [Thời gian tạo]

🔍 View on GeckoTerminal: [Link]
```

## Logs

Bot tự động ghi log vào file `aptos_monitor.log` và console.

## Troubleshooting

### Bot không gửi được tin nhắn
- Kiểm tra Bot Token có đúng không
- Kiểm tra Chat ID có đúng không
- Đảm bảo bot đã được thêm vào group/channel (nếu sử dụng)

### Không nhận được thông báo pool mới
- Kiểm tra kết nối internet
- Xem log để kiểm tra lỗi API
- GeckoTerminal API có thể bị rate limit

### Lỗi dependencies
```bash
pip install --upgrade -r requirements.txt
```

## Tùy chỉnh

### Thay đổi tần suất kiểm tra
Sửa dòng `await asyncio.sleep(60)` trong hàm `run_monitor()` để thay đổi interval (tính bằng giây).

### Thêm filter
Có thể thêm logic filter trong hàm `notify_new_pools()` để chỉ thông báo pool thỏa mãn điều kiện nhất định.

## Lưu ý

- Bot sử dụng GeckoTerminal API miễn phí, có thể bị giới hạn rate limit
- Khuyến nghị chạy trên VPS để đảm bảo hoạt động 24/7
- Backup file log định kỳ để tránh file quá lớn
