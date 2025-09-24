import requests
import time
import asyncio
import logging
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# GeckoTerminal API endpoint (Aptos latest pools)
API_URL = "https://app.geckoterminal.com/api/p1/aptos/latest_pools?include=dex,dex.network,pool_metric,tokens&page=1&include_network_metrics=true&pool_creation_hours_ago[lte]=72&networks=aptos"

# Store pool IDs we've already seen to avoid duplicate notifications
seen_pools = set()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aptos_monitor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AptosPoolMonitor:
    def __init__(self, bot_token, chat_id):
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/123.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

    async def fetch_latest_pools(self):
        """Fetch latest pools from GeckoTerminal API"""
        try:
            response = requests.get(API_URL, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching pools: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return []

    def format_pool_message(self, pool):
        """Format pool information for Telegram message"""
        attributes = pool.get("attributes", {})
        relationships = pool.get("relationships", {})
        
        # Extract basic info
        pool_id = pool.get("id", "Unknown")
        contract_address = attributes.get("address", "Unknown")
        pool_name = attributes.get("name", "Unknown")
        created_at = attributes.get("pool_created_at", "Unknown")
        
        # Extract token information
        tokens_data = relationships.get("tokens", {}).get("data", [])
        token_names = []
        for token in tokens_data:
            token_id = token.get("id")
            # You might need to extract token names from included data
            token_names.append(token_id.split('_')[-1] if token_id else "Unknown")
        
        # Extract DEX information
        dex_data = relationships.get("dex", {}).get("data", {})
        dex_name = dex_data.get("id", "Unknown DEX")
        
        # Format creation time
        try:
            if created_at != "Unknown":
                created_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                formatted_time = created_time.strftime("%Y-%m-%d %H:%M:%S UTC")
            else:
                formatted_time = "Unknown"
        except:
            formatted_time = created_at

        message = f"""
🆕 **NEW APTOS POOL DETECTED**

🏷️ **Pool Name:** {pool_name}
🔗 **Contract:** `{contract_address}`
🆔 **Pool ID:** `{pool_id}`
💱 **Tokens:** {' / '.join(token_names) if token_names else 'Unknown'}
🏪 **DEX:** {dex_name}
⏰ **Created:** {formatted_time}

🔍 **View on GeckoTerminal:**
https://www.geckoterminal.com/aptos/pools/{contract_address}
        """
        return message.strip()

    async def send_telegram_message(self, message):
        """Send message to Telegram"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
            logger.info("Message sent successfully to Telegram")
            return True
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    async def notify_new_pools(self, pools):
        """Check for new pools and send notifications"""
        new_pools_count = 0
        
        for pool in pools:
            pool_id = pool.get("id")
            
            if pool_id and pool_id not in seen_pools:
                new_pools_count += 1
                seen_pools.add(pool_id)
                
                # Format and send message
                message = self.format_pool_message(pool)
                success = await self.send_telegram_message(message)
                
                if success:
                    logger.info(f"New pool notification sent: {pool_id}")
                else:
                    logger.error(f"Failed to send notification for pool: {pool_id}")
                
                # Add small delay between messages to avoid rate limiting
                await asyncio.sleep(1)
        
        if new_pools_count == 0:
            logger.info("No new pools found")
        else:
            logger.info(f"Found and notified {new_pools_count} new pools")
        
        return new_pools_count

    async def run_monitor(self):
        """Main monitoring loop"""
        logger.info("Starting Aptos pool monitoring...")

        # Test Telegram connection
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text="🤖 Aptos Pool Monitor started successfully!"
            )
        except Exception as e:
            logger.error(f"Failed to send startup message: {e}")
            return

        while True:
            try:
                pools = await self.fetch_latest_pools()
                logger.info(f"Fetched {len(pools)} pools from API")

                if pools:
                    await self.notify_new_pools(pools)
                else:
                    logger.warning("No pools data received from API")

                # Wait 60 seconds before next check
                await asyncio.sleep(60)

            except KeyboardInterrupt:
                logger.info("Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                await asyncio.sleep(30)  # Wait 30 seconds before retrying

async def main():
    # Check if required environment variables are set
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    if not TELEGRAM_CHAT_ID:
        logger.error("TELEGRAM_CHAT_ID not found in environment variables")
        return
    
    # Create and run monitor
    monitor = AptosPoolMonitor(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    await monitor.run_monitor()

if __name__ == "__main__":
    asyncio.run(main())
