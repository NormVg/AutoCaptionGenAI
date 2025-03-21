import speech_recognition as sr

def recognize_speech_from_wav(file_path,lang=''):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.record(source)
        
        try:
            recognized_text = recognizer.recognize_whisper(audio_data)
            return recognized_text

        except sr.UnknownValueError:
            return None

        except sr.RequestError as e:
            return None


asa = recognize_speech_from_wav("res.wav")
from pprint import pprint
pprint(asa)
