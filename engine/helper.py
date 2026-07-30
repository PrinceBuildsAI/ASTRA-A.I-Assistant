import os
import re
import time

# def extract_yt_term(command):
#     command = command.lower().strip()

#     # Remove common keywords
#     command = command.replace("play song", "")
#     command = command.replace("play", "")
#     command = command.replace("search youtube", "")
#     command = command.replace("youtube", "")
#     command = command.replace("on youtube", "")

#     search_term = command.strip()


#     return search_term if search_term else None
def extract_yt_term(command):
    command = command.lower().strip()

    # Only process if it's a YouTube-related command
    youtube_triggers = ["play", "play song", "youtube", "on youtube", "search youtube"]

    if not any(trigger in command for trigger in youtube_triggers):
        return None

    # Remove common keywords
    command = command.replace("play song", "")
    command = command.replace("search youtube", "")
    command = command.replace("on youtube", "")
    command = command.replace("play", "")
    command = command.replace("youtube", "")

    search_term = " ".join(command.split())

    return search_term if search_term else None


def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = " ".join(filtered_words)

    return result_string


# key events like receive call, stop call, go back
def keyEvent(key_code):
    command = f"adb shell input keyevent {key_code}"
    os.system(command)
    time.sleep(1)


# Tap event used to tap anywhere on screen
def tapEvents(x, y):
    command = f"adb shell input tap {x} {y}"
    os.system(command)
    time.sleep(1)


# Input Event is used to insert text in mobile
def adbInput(message):
    command = f'adb shell input text "{message}"'
    os.system(command)
    time.sleep(1)


# to go complete back
def goback(key_code):
    for i in range(6):
        keyEvent(key_code)


# To replace space in string with %s for complete message send
def replace_spaces_with_percent_s(input_string):
    return input_string.replace(" ", "%s")


# def markdown_to_text(md):
#     html = markdown2.markdown(md)
#     soup = BeautifulSoup(html, "html.parser")
#     return soup.get_text().strip()
