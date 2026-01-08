import speech_recognition as sr
from langdetect import detect
import pyttsx3
import threading

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        
        # Set voice (English default)
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', voices[0].id)
        
    def listen(self, timeout=5):
        """Listen to microphone and return text"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                
            # Try Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            
            # Detect language
            try:
                lang = detect(text)
            except:
                lang = 'en'
                
            return {"text": text, "language": lang, "success": True}
            
        except sr.WaitTimeoutError:
            return {"success": False, "error": "Timeout"}
        except sr.UnknownValueError:
            return {"success": False, "error": "Could not understand"}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    def speak(self, text, language='en'):
        """Text-to-speech output"""
        def _speak():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
        thread = threading.Thread(target=_speak, daemon=True)
        thread.start()
