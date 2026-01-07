# Tkinter GUI (code from before)

import tkinter as tk
from tkinter import scrolledtext
import asyncio
import websockets
import threading
import json

class AlfredGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Alfredx: Waynecore Assistant")
        self.root.geometry("600x400")
        self.chat = scrolledtext.ScrolledText(self.root)
        self.chat.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=5, padx=10, fill=tk.X)
        self.entry.bind("<Return>", self.send_message)
        self.ws = None
        self.connect()

    def connect(self):
        def run_websocket():
            asyncio.run(self.websocket_client())
        threading.Thread(target=run_websocket, daemon=True).start()

    async def websocket_client(self):
        uri = "ws://localhost:8000/ws"
        async with websockets.connect(uri) as ws:
            self.ws = ws
            while True:
                try:
                    msg = await ws.recv()
                    self.chat.insert(tk.END, f"Alfredx: {msg}\n")
                    self.chat.see(tk.END)
                except:
                    break

    def send_message(self, event=None):
        msg = self.entry.get()
        if msg and self.ws:
            asyncio.run_coroutine_threadsafe(self.ws.send(msg), asyncio.get_event_loop())
            self.chat.insert(tk.END, f"You ({msg}): \n")
            self.chat.see(tk.END)
            self.entry.delete(0, tk.END)

if __name__ == "__main__":
    app = AlfredGUI()
    app.root.mainloop()
