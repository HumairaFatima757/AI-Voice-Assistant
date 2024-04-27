import tempfile
import os
from gtts import gTTS
import pygame
from pydub import AudioSegment
import speech_recognition as sr
import pyautogui
import webbrowser

os.environ["PATH"] += os.pathsep + r"C:\Downloads\ffmpeg-7.0-full_build\bin"

pygame.init()
pygame.mixer.init()

def listen_for_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError as e:
        print("Unable to access the Google Speech Recognition API:", e)
        return None

def respond(response_text):
    print(response_text)
    tts = gTTS(text=response_text, lang='en')

    # Use a temporary file for the audio
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio_path = temp_audio.name
        tts.save(temp_audio_path)

        sound = AudioSegment.from_mp3(temp_audio_path)
        sound.export(r"C:\Users\sumaira\Desktop\respond.wav", format="wav")


    pygame.mixer.music.load("respond.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    print("Audio playback finished.")
    # Delete the temporary audio file
    os.unlink(temp_audio_path)

tasks = []
listeningToTask = False

def main():
    global tasks
    global listeningToTask
    while True:
        command = listen_for_command()

        triggerKeyword = "huma"

        if command and command.startswith(triggerKeyword + " "):
            command = command[len(triggerKeyword) + 1:].strip()# Remove the trigger keyword from the command
            if listeningToTask:
                tasks.append(command)
                listeningToTask = False
                respond("Adding " + command + " to your task list. You have " + str(len(tasks)) + " currently in your list.")
            elif "add a task" in command:
                listeningToTask = True
                respond("Sure, what is the task?")
            elif "list tasks" in command:
                respond("Sure. Your tasks are:")
                for task in tasks:
                    respond(task)
            elif "take a screenshot" in command:
                pyautogui.screenshot("screenshot.png")
                respond("I took a screenshot for you.")
            elif "open chrome" in command:
                respond("Opening Chrome.")
                webbrowser.open("https://www.google.com/chrome/")
            elif "exit" in command:
                respond("Goodbye!")
                break
            else:
                respond("Sorry, I'm not sure how to handle that command.")

if __name__ == "__main__":
    print("Starting virtual assistant...")
    #respond("This has been building a virtual assistant with Python")
    main()
