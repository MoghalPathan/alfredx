import tkinter as tk
from tkinter import scrolledtext, messagebox
import asyncio
import websockets
from threading import Thread
import sys

class AlfredxGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Alfredx: Waynecore Assistant - Phase 1")
        self.root.geometry("700x500")
        self.root.configure(bg="#1a1a1a")
        
        # Status bar
        self.status_label = tk.Label(
            self.root, 
            text="⏳ Connecting to backend...", 
            bg="#1a1a1a", 
            fg="yellow",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=5)
        
        # Chat display
        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            bg="#0a0a0a",
            fg="#00ff00",
            font=("Consolas", 11),
            wrap=tk.WORD,
            state="disabled"
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg="#1a1a1a")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_box = tk.Entry(
            input_frame,
            bg="#2a2a2a",
            fg="white",
            font=("Arial", 12),
            insertbackground="white"
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_box.bind("<Return>", self.on_send)
        
        self.send_btn = tk.Button(
            input_frame,
            text="Send",
            bg="#0066cc",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.on_send,
            cursor="hand2"
        )
        self.send_btn.pack(side=tk.RIGHT)
        
        # WebSocket variables
        self.ws = None
        self.ws_url = "ws://127.0.0.1:8000/ws"
        self.loop = None

        # Focus input box
        self.input_box.focus_set()
        
        # Start async loop in separate thread
        self.start_asyncio_thread()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def log_message(self, text, color="#00ff00"):
        """Thread-safe message logging"""
        def append():
            self.chat_area.config(state="normal")
            self.chat_area.insert(tk.END, text + "\n", "msg")
            self.chat_area.tag_config("msg", foreground=color)
            self.chat_area.see(tk.END)
            self.chat_area.config(state="disabled")
        self.root.after(0, append)
        
    def update_status(self, text, color):
        """Update status label"""
        def update():
            self.status_label.config(text=text, fg=color)
        self.root.after(0, update)
        
    def start_asyncio_thread(self):
        """Start asyncio event loop in separate thread"""
        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.connect_websocket())
            self.loop.run_forever()
        
        thread = Thread(target=run_loop, daemon=True)
        thread.start()
        
    async def connect_websocket(self):
        """Connect to backend WebSocket"""
        try:
            self.ws = await websockets.connect(self.ws_url, ping_interval=20)
            self.update_status("✅ Connected to Alfredx Backend", "lime")
            self.log_message("=== Alfredx Phase 1 Online ===", "#00aaff")
            
            # Start receiving messages
            asyncio.create_task(self.receive_messages())
            
        except Exception as e:
            self.update_status(f"❌ Connection failed: {e}", "red")
            self.log_message(f"ERROR: {e}", "red")
            
    async def receive_messages(self):
        """Listen for messages from backend"""
        try:
            async for message in self.ws:
                self.log_message(f"🤖 {message}", "#00aaff")
        except websockets.exceptions.ConnectionClosed:
            self.update_status("⚠️ Connection closed", "orange")
        except Exception as e:
            self.log_message(f"Receive error: {e}", "red")
            
    def on_send(self, event=None):
        """Handle send button/Enter key"""
        message = self.input_box.get().strip()
        
        if not message:
            return
            
        if not self.ws:
            messagebox.showerror("Error", "Not connected to backend!")
            return
            
        # Display user message
        self.log_message(f"👤 You: {message}", "white")
        self.input_box.delete(0, tk.END)
        
        # Send via WebSocket (schedule on async loop)
        asyncio.run_coroutine_threadsafe(
            self.ws.send(message),
            self.loop
        )
        
    def on_close(self):
        """Clean shutdown"""
        if self.ws:
            asyncio.run_coroutine_threadsafe(self.ws.close(), self.loop)
        if self.loop:
            self.loop.stop()
        self.root.destroy()
        sys.exit(0)
        
    def run(self):
        """Start GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AlfredxGUI()
    app.run()
