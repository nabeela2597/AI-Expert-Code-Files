import random

import pyttsx3


# Initialize pyttsx3 TTS engine

engine = pyttsx3.init()

engine.setProperty("rate", 150)

engine.setProperty("volume", 0.9)


def speak(text):

    """Speak the text provided to the TTS engine."""

    engine.say(text)

    engine.runAndWait()


def get_samples():

    """Return a list of custom phrases and jokes."""

    return [

        "Hello! I am your computer!",

        "Python is awesome!",

        "This is AI speaking!",

        "Welcome to the future!",

        "Why don't skeletons fight each other? They don't have the guts!"

    ]


def main():

    print("🤖 AI VOICE LAB")

    speak("Hello! Type something for me to say!")

   

    while True:

        text = input("\n🎤 You: ").strip().lower()

       

        # Exit Command

        if text == 'exit':

            speak("Goodbye!")

            break

       

        # Random Sample Command

        elif text == 'sample':

            phrase = random.choice(get_samples())

            print(f"🎲 {phrase}")

            speak(phrase)

       

        # Custom Commands for Speed and Volume

        elif text == 'speed up':

            current_rate = engine.getProperty('rate') + 50

            engine.setProperty('rate', current_rate)

            speak(f"Speed increased to {current_rate}")

       

        elif text == 'slow down':

            current_rate = engine.getProperty('rate') - 50

            engine.setProperty('rate', current_rate)

            speak(f"Speed decreased to {current_rate}")

       

        elif text == 'increase volume':

            current_volume = engine.getProperty('volume') + 0.1

            if current_volume > 1: current_volume = 1

            engine.setProperty('volume', current_volume)

            speak(f"Volume increased to {current_volume}")

       

        elif text == 'decrease volume':

            current_volume = engine.getProperty('volume') - 0.1

            if current_volume < 0: current_volume = 0

            engine.setProperty('volume', current_volume)

            speak(f"Volume decreased to {current_volume}")

       

        # Custom Command for Jokes

        elif text == 'tell a joke':

            jokes = [

                "Why don't skeletons fight each other? They don't have the guts!",

                "What do you get when you cross a snowman and a vampire? Frostbite!",

                "Why don’t scientists trust atoms? Because they make up everything!"

            ]

            joke = random.choice(jokes)

            print(f"😂 {joke}")

            speak(joke)

       

        # Unrecognized Command

        else:

            print("💡 Type 'sample' for ideas or 'exit' to quit.")

            speak("I didn't quite catch that. Try again!")


if __name__ == "__main__":

    main()

