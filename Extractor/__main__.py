import asyncio
import importlib
import signal
from pyrogram import idle
from Extractor.modules import ALL_MODULES

# =========================
# 🔹 Dummy Flask Server For Render
# =========================
from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running on Render Baby😘"

def run_flask():
    port = int(os.environ.get("PORT", 10000))  # Render requires a port
    app.run(host="0.0.0.0", port=port)
# =========================


loop = asyncio.get_event_loop()

# Graceful shutdown
should_exit = asyncio.Event()

def shutdown():
    print("Shutting down gracefully...")
    loop.create_task(should_exit.set())  # triggers exit from idle

signal.signal(signal.SIGTERM, lambda s, f: loop.create_task(should_exit.set()))
signal.signal(signal.SIGINT, lambda s, f: loop.create_task(should_exit.set()))

async def sumit_boot():
    # Load all modules
    for all_module in ALL_MODULES:
        importlib.import_module("Extractor.modules." + all_module)

    print("» ʙᴏᴛ ᴅᴇᴘʟᴏʏ sᴜᴄᴄᴇssғᴜʟʟʏ🎉😘")

    # Start the Pyrogram bot
    await idle()

    print("» ɢᴏᴏᴅ ʙʏᴇ ! sᴛᴏᴘᴘɪɴɢ ʙᴏᴛ.")

if __name__ == "__main__":
    # Start Flask dummy server (Render fix)
    threading.Thread(target=run_flask).start()

    try:
        loop.run_until_complete(sumit_boot())
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        loop.close()
        print("Loop closed.")
