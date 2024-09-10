# Telegram Chat ID Fetcher

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![Telethon](https://img.shields.io/badge/Telethon-1.24.0-green)

A Python script to fetch and save the IDs of all Telegram chats (groups, channels, private messages) associated with an account.

## Features

- Fetches the chat ID, title, and type (group, channel, private message).
- Saves the result in a text file (`chats_list.txt`).
- Works with both user accounts and bot sessions.
- Supports 2FA authentication.

## Prerequisites

- Python 3.x
- [Telethon](https://github.com/LonamiWebs/Telethon) library
- A Telegram API ID and API Hash (get them from [my.telegram.org](https://my.telegram.org))

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/YoungArtur/telegram-chat-id-fetcher.git
   ```
  
2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Edit a **config.json** file in the root directory with your API credentials:

   ```json
{
  "api_id": YOUR_API_ID,
  "api_hash": "YOUR_API_HASH",
  "session_file": "your_session_name"
}
   ```

## Usage
Run the script to start fetching chat IDs:
   ```bash
   python chat_id_fetcher.py
   ```

You will be prompted to enter your phone number, the verification code, and 2FA password (if enabled).

The fetched chat IDs and titles will be saved to **chats_list.txt**.

## Example Output
```less
Found dialog: MyGroup (ID: 123456789, Type: PeerChannel)
Found dialog: MyChannel (ID: 987654321, Type: PeerChat)
```

## Troubleshooting
Ensure you have the correct API ID and Hash from my.telegram.org.
Ensure you have a valid config.json file.
If you encounter a SessionPasswordNeededError, make sure you enter the correct 2FA password.
