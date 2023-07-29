# -----------------------------------------------------------
# speech recognition class for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# -----------------------------------------------------------

import speech_recognition as sr

from config import TEST_AUDIO_FILE


class SpeechRecognizer:
    def __init__(self):
        self.r = sr.Recognizer()

    def recognize(self, filename):
        text = None
        try:
            with sr.AudioFile(filename) as source:
                audio = self.r.record(source)  # read the entire audio file
        except Exception as e:
            audio = None
            print("Speech Recognizer Sphinx error; {0}".format(e))
        try:
            text = self.r.recognize_sphinx(audio)
        except sr.UnknownValueError:
            print("Speech Recognizer Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Speech Recognizer Sphinx error; {0}".format(e))
        except AssertionError as e:
            print("Speech Recognizer Sphinx error; {0}".format(e))
        return text

    def test(self):
        text = self.recognize(TEST_AUDIO_FILE)
        return text == 'one two three'


recognizer = SpeechRecognizer()
