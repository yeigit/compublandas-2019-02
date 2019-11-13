import os
import speech_recognition as sr
from gtts import gTTS
import time
mic = sr.Microphone()

class VoiceOutMod():
    def speak(self, string, lang = 'es-CO'):
        if string:
            tts = gTTS(text=string, lang=lang)
            tts.save("audio.mp3")
            os.system("vlc audio.mp3 --intf dummy --play-and-exit")
            time.sleep(3)
        return 1
