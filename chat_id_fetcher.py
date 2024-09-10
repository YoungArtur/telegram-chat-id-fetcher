from telethon import TelegramClient, errors
from telethon.tl.types import PeerChannel, PeerChat

from typing import List, Callable
from msgspec import json, Struct, ValidationError, DecodeError
from itertools import islice

import asyncio
from rich.console import Console

console = Console()

SUCCESS = "[bold green]✓[/] "
FAIL = "[bold red]✗[/] "
QUESTION = "[bold blue]>[/] "

CONFIG_FILE = "config.json"

class Config(Struct):
    api_id: int
    api_hash: str 
    session_file: str = "chatgetter"

async def auth_flow(
    client: TelegramClient,
    on_number: Callable[[], str],
    on_code: Callable[[], str],
    on_password: Callable[[], str],
    on_incorrect_code: Callable[[], None] = None,
    on_incorrect_password: Callable[[], None] = None,
    on_too_many_attempts: Callable[[], None] = None
):
    number = on_number()
    await client.send_code_request(number)

    is_2fa = False
    attempts = 0
    while attempts < 3:
        code = on_code()
        try:
            await client.sign_in(number, code)
            break
        except errors.SessionPasswordNeededError:
            is_2fa = True
            break
        except (
            errors.PhoneCodeEmptyError,
            errors.PhoneCodeExpiredError,
            errors.PhoneCodeHashEmptyError,
            errors.PhoneCodeInvalidError
        ):
            on_incorrect_code()

        attempts += 1
    else:
        on_too_many_attempts()
        exit(1)

    if is_2fa:
        attempts = 0
        while attempts < 3:
            password = on_password()
            try:
                await client.sign_in(number, password=password)
                break
            except errors.PasswordHashInvalidError:
                on_incorrect_password()
                attempts += 1
        else:
            on_too_many_attempts()
            exit(1)

async def main():
    console.print("[blue bold]telegram chat id fetcher (c) github.com/YoungArtur")

    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.decode(f.read(), type=Config)
    except FileNotFoundError:
        console.print(FAIL + "config file not found.")
        exit(1)
    except (ValidationError, DecodeError) as e:
        console.print(FAIL + f"invalid config file: {str(e).lower()}")
        exit(1)
    
    with console.status('authorizing') as status:
        client = TelegramClient(
            config.session_file, config.api_id, config.api_hash
        )
       
        await client.connect()

        if not await client.is_user_authorized():
            status.stop()

            await auth_flow(
                client,
                on_number=lambda: console.input(QUESTION + "enter your phone number: "),
                on_code=lambda: console.input(QUESTION + "enter the code you received: "),
                on_password=lambda: console.input(QUESTION + "enter your 2FA: ", password=True),
                on_incorrect_code=lambda: console.print(FAIL + "invalid code."),
                on_incorrect_password=lambda: console.print(FAIL + "invalid password."),
                on_too_many_attempts=lambda: console.print(FAIL + "too much unsuccessful attempts.")
            )

    console.print(SUCCESS + "authorized!")

    all_chats = []
    async for dialog in client.iter_dialogs():
        chat_id = dialog.id
        chat_title = dialog.name
        chat_type = type(dialog.entity).__name__
        console.print(f"Found dialog: {chat_title} (ID: {chat_id}, Type: {chat_type})")
        all_chats.append(f"{chat_id} | {chat_title} | {chat_type}")

    with open("chats_list.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(all_chats))

    console.print(SUCCESS + f"Saved {len(all_chats)} chat IDs and titles to chats_list.txt")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print(FAIL + "aborted.")
        exit(1)
