import json
import os
import re
from shlex import quote
import struct
import subprocess
import time
import webbrowser
import sqlite3
from playsound import playsound as playsound
import eel
import pyaudio
import pyautogui
import traceback
import time
import re


from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine

# Playing assistant sound function
# API Sensitive information
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

from engine.helper import extract_yt_term, remove_words

con = sqlite3.connect("astra.db")
cursor = con.cursor()


@eel.expose
def playAssistantSound():
    music_dir = "WWW\\vendore\\audio\\start_sound.wav"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                "SELECT path FROM sys_command WHERE name IN (?)", (app_name,)
            )
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute(
                    "SELECT url FROM web_command WHERE name IN (?)", (app_name,)
                )
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening " + query)
                    try:
                        os.system("start " + query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")


def PlayYoutube(query):
    print("Query:", repr(query))
    search_term = extract_yt_term(query)

    if not search_term:
        speak("Sorry, I couldn't find what you want to play.")
        return

    search_term = search_term.strip()
    speak(f"Playing {search_term} on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:

        # pre trained keywords
        porcupine = pvporcupine.create(
            keywords=[
                "jarvis",
                "alexa",
                "bumblebee",
                "hey google",
                "hey siri",
                "terminator",
                "ok google",
            ]
        )
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
        )

        # loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # processing keyword comes from mic
            keyword_index = porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index >= 0:
                print("hotword detected")

                # pressing shortcut key win+j
                import pyautogui as autogui

                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# Find contacts
def findContact(query):

    query = query.lower().strip()

    words_to_remove = {
        ASSISTANT_NAME.lower(),
        "send",
        "message",
        "call",
        "phone",
        "video",
        "voice",
        "whatsapp",
        "whats",
        "app",
        "make",
        "a",
        "an",
        "the",
        "to",
        "please",
        "can",
        "you",
        "start",
        "on",
    }

    # Remove only complete words
    words = query.split()
    query = " ".join(word for word in words if word not in words_to_remove)

    print("Searching contact:", query)

    try:
        cursor.execute(
            """
            SELECT mobile_no, name
            FROM contacts
            WHERE LOWER(name) LIKE ?
            LIMIT 1
            """,
            ("%" + query + "%",),
        )

        result = cursor.fetchone()

        if result:
            mobile_no = str(result[0])

            if not mobile_no.startswith("+91"):
                mobile_no = "+91" + mobile_no

            return mobile_no, result[1]

        speak("Contact not found.")
        return 0, 0

    except Exception as e:
        print(e)
        speak("Something went wrong.")
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    print("whatsApp() called")
    print(mobile_no, message, flag, name)

    if flag == "message":
        target_tab = 14
        jarvis_message = "message send successfully to " + name

    elif flag == "call":
        target_tab = 7
        message = ""
        jarvis_message = "calling to " + name

    else:
        target_tab = 6
        message = ""
        jarvis_message = "staring video call with " + name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    # subprocess.run(full_command, shell=True)

    pyautogui.hotkey("ctrl", "f")

    for i in range(1, target_tab):
        pyautogui.hotkey("tab")

    pyautogui.hotkey("enter")
    speak(jarvis_message)


import time


# Chat Bot
def chatBot(query):
    try:
        completion = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are ASTRA, a smart AI assistant. "
                        "Your developer is Prince"
                        "Reply in only 2 or 3 short sentences. "
                        "Be friendly, natural, and concise."
                    ),
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            temperature=0.7,
            max_tokens=120,
        )

        response = completion.choices[0].message.content.strip()

        print("BUMBLEBEE:", response)
        speak(response)
        return response

    except Exception as e:
        print("ChatBot Error:", e)
        speak("Sorry, I couldn't connect to the AI service.")
        return None


# android automation


def makeCall(name, mobileNo):
    mobileNo = mobileNo.replace(" ", "")
    speak("Calling " + name)
    command = "adb shell am start -a android.intent.action.CALL -d tel:" + mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import (
        replace_spaces_with_percent_s,
        goback,
        keyEvent,
        tapEvents,
        adbInput,
    )

    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(625, 2550)
    # start chat
    tapEvents(1080, 2555)
    # search mobile no
    adbInput(mobileNo)
    # tap on name
    tapEvents(600, 950)
    # tap on input
    tapEvents(280, 2580)
    # message
    adbInput(message)
    # send
    tapEvents(1122, 1717)
    speak("message send successfully to " + name)


# Settings Modal


# Assistant name
@eel.expose
def assistantName():
    name = ASSISTANT_NAME
    return name


@eel.expose
def personalInfo():
    try:
        cursor.execute("SELECT * FROM info")
        results = cursor.fetchall()
        jsonArr = json.dumps(results[0])
        eel.getData(jsonArr)
        return 1
    except:
        print("no data")


@eel.expose
def updatePersonalInfo(name, designation, mobileno, email, city):
    cursor.execute("SELECT COUNT(*) FROM info")
    count = cursor.fetchone()[0]

    if count > 0:
        # Update existing record
        cursor.execute(
            """UPDATE info 
               SET name=?, designation=?, mobileno=?, email=?, city=?""",
            (name, designation, mobileno, email, city),
        )
    else:
        # Insert new record if no data exists
        cursor.execute(
            """INSERT INTO info (name, designation, mobileno, email, city) 
               VALUES (?, ?, ?, ?, ?)""",
            (name, designation, mobileno, email, city),
        )

    con.commit()
    personalInfo()
    return 1


@eel.expose
def displaySysCommand():
    cursor.execute("SELECT * FROM sys_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displaySysCommand(jsonArr)
    return 1


@eel.expose
def deleteSysCommand(id):
    cursor.execute("DELETE FROM sys_command WHERE id = ?", (id,))
    con.commit()


@eel.expose
def addSysCommand(key, value):
    cursor.execute("""INSERT INTO sys_command VALUES (?, ?, ?)""", (None, key, value))
    con.commit()


@eel.expose
def displayWebCommand():
    cursor.execute("SELECT * FROM web_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayWebCommand(jsonArr)
    return 1


@eel.expose
def addWebCommand(key, value):
    cursor.execute("""INSERT INTO web_command VALUES (?, ?, ?)""", (None, key, value))
    con.commit()


@eel.expose
def deleteWebCommand(id):
    cursor.execute("DELETE FROM web_command WHERE Id = ?", (id,))
    con.commit()


@eel.expose
def displayPhoneBookCommand():
    cursor.execute("SELECT * FROM contacts")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayPhoneBookCommand(jsonArr)
    return 1


@eel.expose
def deletePhoneBookCommand(id):
    cursor.execute("DELETE FROM contacts WHERE Id = ?", (id,))
    con.commit()


@eel.expose
def InsertContacts(Name, MobileNo, Email, City):
    cursor.execute(
        """INSERT INTO contacts VALUES (?, ?, ?, ?, ?)""",
        (None, Name, MobileNo, Email, City),
    )
    con.commit()
