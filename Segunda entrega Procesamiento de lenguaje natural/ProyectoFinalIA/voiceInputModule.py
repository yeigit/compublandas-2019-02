import os
import speech_recognition as sr
from unidecode import unidecode

mic = sr.Microphone()
r = sr.Recognizer()
r.energy_threshold = 2500


class VoiceInMod():
    def get_voice(self):
        with mic as source:
            # r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        print 'Reconociendo'
        try:
            voice_input = r.recognize_google(audio, language='es-CO')
            normalized_input = unidecode(voice_input)
        except sr.UnknownValueError:
            return ''

        return normalized_input
