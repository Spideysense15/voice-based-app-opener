import subprocess
import os
import keyboard
from datetime import datetime
import sys
import speech_recognition as sr
import pyttsx3
import time

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Function to speak a given text
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Dictionary to map application names to their commands
app_commands = {
    "notepad": "notepad",
    "calculator": "calc",
    "browser": "open brave",
    "file_explorer": "explorer",
    "valorant": "Valorant"
}

def greet_user():
    """Greet the user based on the time of day and tell the time."""
    current_time = datetime.now()
    hour = current_time.hour
    
    if 5 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 17:
        greeting = "Good afternoon!"
    elif 17 <= hour < 21:
        greeting = "Good evening!"
    else:
        greeting = "Good night!"
    
    time_str = current_time.strftime("%I:%M %p")  # Format time in HH:MM AM/PM
    greeting_message = f"{greeting} The current time is {time_str}."
    print(greeting_message)
    speak(greeting_message)

def open_application(app_type):
    # Convert the input to lowercase for consistent matching
    app_type = app_type.lower()
    
    # Look up the command based on the app_type
    if app_type in app_commands:
        try:
            subprocess.run(app_commands[app_type], shell=True)
            success_message = f"{app_type.capitalize()} opened successfully!"
            print(success_message)
            speak(success_message)
        except Exception as e:
            error_message = f"Failed to open {app_type}: {str(e)}"
            print(error_message)
            speak(error_message)
    else:
        not_recognized_message = f"Application type '{app_type}' not recognized."
        print(not_recognized_message)
        speak(not_recognized_message)

def restart_program():
    """Restart the current program."""
    print("Restarting the program...")
    speak("Restarting the program...")
    python = sys.executable  # Path to the Python interpreter
    os.execl(python, python, *sys.argv)  # Restart the script

def listen_for_application():
    """Listen for voice input to open applications."""
    with sr.Microphone() as source:
        print("Listening for application to open...")
        speak("Listening for application to open...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")

            # Check if the trigger word "Jarvis" is in the command
            if "jarvis" in command.lower():
                app_type = command.lower().replace("jarvis", "").strip()  # Extract application name
                if app_type:  # Check if there is an app name provided
                    open_application(app_type)
                else:
                    print("No application name provided after 'Jarvis'.")
                    speak("No application name provided after 'Jarvis'.")
                return False  # End the loop
            else:
                print("Trigger word not detected.")
                speak("Trigger word not detected.")
                return True  # Continue listening

        except sr.UnknownValueError:
            error_message = "Sorry, I did not understand that."
            print(error_message)
            speak(error_message)
            return True  # Continue listening
        except sr.RequestError:
            error_message = "Could not request results from the speech recognition service."
            print(error_message)
            speak(error_message)
            return True  # Continue listening

def main():
    # Greet the user with time
    greet_user()

    # Example usage
    while True:
        if not listen_for_application():  # Listen for voice input
            print("Ending the conversation.")
            speak("Ending the conversation.")
            break  # Exit the loop and end the program

# Set up a keyboard shortcut for restarting the program (Ctrl + R)
keyboard.add_hotkey('ctrl+r', restart_program)

if __name__ == "__main__":
    main()
