import os
import eel

from engine.features import *
from engine.command import *
from engine.auth import recoganize


def start():

    eel.init("WWW")

    playAssistantSound()

    @eel.expose
    def init():
        # subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready For face Authentication")
        flag = recoganize.AuthenticateFace()

        if flag == 1:
            eel.hideFaceAuth()
            speak("Authentication successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Prince. How Can I Help You")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Fail")

    # os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    # eel.start("index.html", mode=None, host="localhost", block=True)
    eel.start(
    "index.html",
    mode="edge",
    host="localhost",
    block=True,
    size=(1920, 1080),
    cmdline_args=["--start-maximized"]
)
    
