import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, simpledialog  # ← ADDED simpledialog
import asyncio
import websockets
from threading import Thread
import sys
import json


class AlfredxGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Alfredx Phase 2: Winter Soldier")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Chat
        self.create_chat_tab()
        
        # Tab 2: Winter Soldier Activation
        self.create_winter_soldier_tab()
        
        # WebSocket
        self.ws = None
        self.ws_url = "ws://127.0.0.1:8000/ws"
        self.loop = None
        self.voice_active = False
        
        self.start_asyncio_thread()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def create_chat_tab(self):
        """Phase 1 Chat tab"""
        chat_frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(chat_frame, text="💬 Chat")
        
        self.status_label = tk.Label(
            chat_frame,
            text="⏳ Connecting...",
            bg="#1a1a1a",
            fg="yellow",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=5)
        
        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            bg="#0a0a0a",
            fg="#00ff00",
            font=("Consolas", 11),
            wrap=tk.WORD,
            state="disabled"
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        input_frame = tk.Frame(chat_frame, bg="#1a1a1a")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.chat_input = tk.Entry(
            input_frame,
            bg="#2a2a2a",
            fg="white",
            font=("Arial", 12),
            insertbackground="white"
        )
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.chat_input.bind("<Return>", self.on_chat_send)
        
        tk.Button(
            input_frame,
            text="Send",
            bg="#0066cc",
            fg="white",
            command=self.on_chat_send
        ).pack(side=tk.RIGHT)
        
    def create_winter_soldier_tab(self):
        """Winter Soldier activation tab"""
        ws_frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(ws_frame, text="⚡ Winter Soldier")
        
        tk.Label(
            ws_frame,
            text="WINTER SOLDIER PROTOCOL",
            bg="#1a1a1a",
            fg="#ff0000",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Progress
        self.ws_progress_label = tk.Label(
            ws_frame,
            text="Progress: 0/10",
            bg="#1a1a1a",
            fg="white",
            font=("Arial", 12)
        )
        self.ws_progress_label.pack(pady=5)
        
        self.ws_progress_bar = ttk.Progressbar(
            ws_frame,
            length=600,
            mode='determinate',
            maximum=10
        )
        self.ws_progress_bar.pack(pady=10)
        
        # Current word
        self.ws_current_word = tk.Label(
            ws_frame,
            text="Say: LONGING",
            bg="#1a1a1a",
            fg="#00ff00",
            font=("Arial", 14, "bold")
        )
        self.ws_current_word.pack(pady=10)
        
        # Log
        self.ws_log = scrolledtext.ScrolledText(
            ws_frame,
            bg="#0a0a0a",
            fg="cyan",
            font=("Consolas", 10),
            height=15,
            state="disabled"
        )
        self.ws_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(ws_frame, bg="#1a1a1a")
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="🎤 Start Voice Activation",
            bg="#cc0000",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.start_voice_activation,
            width=25
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="✍️ Type Word",
            bg="#0066cc",
            fg="white",
            font=("Arial", 12),
            command=self.type_word_dialog,
            width=15
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="⏹️ Stop Voice",
            bg="#666666",
            fg="white",
            font=("Arial", 12),
            command=self.stop_voice_activation,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
    def log_chat(self, text, color="#00ff00"):
        """Log to chat area"""
        def append():
            self.chat_area.config(state="normal")
            self.chat_area.insert(tk.END, text + "\n")
            self.chat_area.tag_config("msg", foreground=color)
            self.chat_area.see(tk.END)
            self.chat_area.config(state="disabled")
        self.root.after(0, append)
        
    def log_ws(self, text, color="cyan"):
        """Log to Winter Soldier tab"""
        def append():
            self.ws_log.config(state="normal")
            self.ws_log.insert(tk.END, text + "\n")
            self.ws_log.tag_config("msg", foreground=color)
            self.ws_log.see(tk.END)
            self.ws_log.config(state="disabled")
        self.root.after(0, append)
        
    def update_ws_progress(self, progress, total, next_word):
        """Update Winter Soldier progress"""
        def update():
            self.ws_progress_bar['value'] = progress
            self.ws_progress_label.config(text=f"Progress: {progress}/{total}")
            self.ws_current_word.config(text=f"Say: {next_word.upper()}")
        self.root.after(0, update)
        
    def update_status(self, text, color):
        def update():
            self.status_label.config(text=text, fg=color)
        self.root.after(0, update)
        
    def start_asyncio_thread(self):
        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.connect_websocket())
            self.loop.run_forever()
        Thread(target=run_loop, daemon=True).start()
        
    async def connect_websocket(self):
        try:
            self.ws = await websockets.connect(self.ws_url, ping_interval=20)
            self.update_status("✅ Phase 2 Connected", "lime")
            self.log_chat("=== Phase 2: Winter Soldier Online ===", "#00aaff")
            asyncio.create_task(self.receive_messages())
        except Exception as e:
            self.update_status(f"❌ {e}", "red")
            
    async def receive_messages(self):
        try:
            async for message in self.ws:
                data = json.loads(message)
                msg_type = data.get("type")
                
                if msg_type == "chat_reply":
                    self.log_chat(f"🤖 {data['message']}", "#00aaff")
                    
                elif msg_type == "winter_soldier_result":
                    result = data["result"]
                    status = result["status"]
                    
                    if status == "continue":
                        self.log_ws(f"✅ Correct! Next: {result['next_word']}", "lime")
                        self.update_ws_progress(result['progress'], result['total'], result['next_word'])
                        
                    elif status == "activated":
                        self.log_ws("🎯 WINTER SOLDIER ACTIVATED! ✅", "red")
                        messagebox.showinfo("ACTIVATED", "SOLDIER READY FOR COMPLIANCE")
                        
                    elif status == "retry":
                        hints = result.get('hints', [])
                        self.log_ws(f"❌ Wrong. Try: {result['expected']} (or {', '.join(hints[:2])})", "orange")
                        
                    elif status == "failed":
                        self.log_ws(f"❌ {result['message']}", "red")
                        
                elif msg_type == "voice_result":
                    result = data["result"]
                    if result["success"]:
                        text = result["text"]
                        self.log_ws(f"🎤 Heard: {text}", "yellow")
                        # Check word
                        await self.ws.send(json.dumps({
                            "command": "winter_soldier_check",
                            "text": text
                        }))
                    else:
                        self.log_ws(f"🎤 Error: {result['error']}", "red")
                        
        except websockets.exceptions.ConnectionClosed:
            self.update_status("⚠️ Disconnected", "orange")
        except Exception as e:
            self.log_chat(f"Error: {e}", "red")
            
    def on_chat_send(self, event=None):
        msg = self.chat_input.get().strip()
        if msg and self.ws:
            self.log_chat(f"👤 You: {msg}", "white")
            self.chat_input.delete(0, tk.END)
            asyncio.run_coroutine_threadsafe(
                self.ws.send(json.dumps({"command": "chat", "text": msg})),
                self.loop
            )
            
    def type_word_dialog(self):
        """Manual word input - keeps prompting"""
        if not self.ws:
            messagebox.showerror("Error", "Not connected!")
            return
        
        word = simpledialog.askstring(
            "Winter Soldier Protocol", 
            "Enter trigger word (or 'stop' to quit):"
        )
        
        if word and word.lower() != 'stop':
            self.log_ws(f"✍️ Typed: {word}", "cyan")
            asyncio.run_coroutine_threadsafe(
                self.ws.send(json.dumps({
                    "command": "winter_soldier_check",
                    "text": word
                })),
                self.loop
            )
            # Auto-prompt for next word after 1 second
            self.root.after(1000, self.type_word_dialog)

    def start_voice_activation(self):
        """Continuous voice activation loop"""
        if not self.ws:
            messagebox.showerror("Error", "Not connected!")
            return
        
        self.voice_active = True
        self.log_ws("🎤 Voice mode active. Speak trigger words...", "lime")
        self.voice_listen_loop()
    
    def voice_listen_loop(self):
        """Keep listening until 10/10 or stopped"""
        if not self.voice_active:
            return
        
        self.log_ws("🎤 Listening...", "yellow")
        asyncio.run_coroutine_threadsafe(
            self.ws.send(json.dumps({"command": "voice_listen"})),
            self.loop
        )
        # Wait 3 seconds, then listen again
        self.root.after(3000, self.voice_listen_loop)
    
    def stop_voice_activation(self):
        """Stop voice loop"""
        self.voice_active = False
        self.log_ws("⏹️ Voice mode stopped", "orange")

    def on_close(self):
        if self.ws:
            asyncio.run_coroutine_threadsafe(self.ws.close(), self.loop)
        if self.loop:
            self.loop.stop()
        self.root.destroy()
        sys.exit(0)
        
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AlfredxGUI()
    app.run()
