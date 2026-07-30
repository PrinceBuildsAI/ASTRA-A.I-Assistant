import pyttsx3
import speech_recognition as sr
import eel
import time
from faster_whisper import WhisperModel
import tempfile
import os
import re
import speech_recognition as sr
from faster_whisper import WhisperModel


# Text to Speech
def speak(text):
    text = str(text)
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 174)
    engine.setProperty("volume", 1.0)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


import re


def cleanCommand(query):
    query = query.lower().strip()

    # Remove punctuation
    query = re.sub(r"[^a-z0-9\s]", "", query)

    # Remove extra words which do not change the actual command
    extra_words = [
        "app",
        "application",
        "program",
        "software",
        "browser",
        "search engine",
        "song",
        "music",
    ]

    corrections = {
        "lead code": "leetcode",
        "leet code": "leetcode",
        "leat code": "leetcode",
    }

    for heard, correct in corrections.items():
        query = query.replace(heard, correct)

    # Remove double spaces
    return " ".join(query.split())


# Speech to Text

model = None
recognizer = sr.Recognizer()


def takeCommand():
    global model

    # Whisper loads only on the first voice command
    if model is None:
        print("Loading voice model...")
        model = WhisperModel("base", device="cpu", compute_type="int8")

    r = recognizer

    try:
        with sr.Microphone() as source:
            print("Listening....")
            eel.DisplayMessage("Listening....")

            r.pause_threshold = 0.4
            r.non_speaking_duration = 0.2
            r.dynamic_energy_threshold = False
            r.energy_threshold = 300
            r.adjust_for_ambient_noise(source, duration=1)

            audio = r.listen(source, timeout=5, phrase_time_limit=8)

        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")

        # Save microphone audio temporarily for Whisper
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as file:
            file.write(audio.get_wav_data())
            audio_file = file.name

        try:
            segments, info = model.transcribe(
                audio_file,
                language="en",
                task="transcribe",
                beam_size=1,
                vad_filter=True,
                initial_prompt=(
                    "Commands include open leetcode, open YouTube, "
                    "open Google, open WhatsApp."
                ),
            )

            query = " ".join(segment.text for segment in segments).strip()

        finally:
            if os.path.exists(audio_file):
                os.remove(audio_file)

        # Make the command easier for your intent system to match
        query = query.lower().strip()
        query = re.sub(r"[^a-z0-9\s]", "", query)

        corrections = {
            "lead code": "leetcode",
            "leet code": "leetcode",
            "leat code": "leetcode",
        }

        for heard, correct in corrections.items():
            query = query.replace(heard, correct)

        print(f"Final command: {query}")
        eel.DisplayMessage(query)

        return query

    except Exception as e:
        print("Speech recognition error:", e)
        return ""


# text = takeCommand()


@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takeCommand()
    else:
        query = message

    query = cleanCommand(query)
    print("Clean command:", query)
    print(query)
    eel.senderText(query)

    if not query:
        eel.ShowHood()
        return

    query = query.lower()
    print("Recognized Query:", query)

    try:
        # query = takeCommand()
        # print(query)

        # if not query:
        #     eel.ShowHood()
        #     return

        # query = query.lower()

        if "open" in query:
            from engine.features import openCommand

            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube

            PlayYoutube(query)

        elif (
            ("send" in query and "message" in query)
            or "phone call" in query
            or "video call" in query
        ):
            from engine.features import findContact, whatsApp, makeCall, sendMessage

            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takeCommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query:
                        speak("what message to send")
                        message = takeCommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send" in query and "message" in query:
                        message = "message"
                        speak("what message to send")
                        query = takeCommand()

                    elif "phone call" in query:
                        message = "call"
                    else:
                        message = "video call"

                    whatsApp(contact_no, query, message, name)

        else:
            from engine.features import chatBot

            chatBot(query)

    except Exception as e:
        print("Error in allCommands:", e)

    eel.ShowHood()
