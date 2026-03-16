'''Lesson 3: Building Rule based chatbots'''
# Import random for joke selection
import random
# Import Fore from colorama for colored text
from colorama import Fore, Style

# Initialize colorama (autoreset ensures each print resets after use)
Style.RESET_ALL

# Destination & joke data
# List of possible destinations
destinations = ["Bali", "Maldives", "Phuket", "Fiji", "Hawaii", "Bora Bora", "Mauritius", "Himalayas", "Kyoto", "Rome", "Paris", "New York"]

# List of jokes
jokes = [
    "Why don't programmers like nature? Too many bugs!🐛",
    "Why did the computer go to the doctor? Because it had a virus!💻",
    "Why did a website's code feel cold? Because it had its 'I-C' control!🥶"
]

# Function to normalize user input (remove extra spaces, make lowercase)
def normalize_input(text):
    return text.lower().strip()

# Provide travel recommendations
def recommend():
    print(f"{Fore.CYAN}🤖TravelBot: Beaches, mountains, or cities?")
    preference = normalize_input(input(f"{Fore.YELLOW}You: "))
    
    # Check for specific preferences
    if "beaches" in preference or "beach" in preference:
        if "destinations" in preference:
            print(f"{Fore.GREEN}🤖TravelBot: How about (suggestion)?") # This line is incomplete in the image
        else:
            print(f"{Fore.GREEN}🤖TravelBot: I'd suggest (yes/no).") # This line is incomplete in the image
    
    elif "mountains" in preference or "mountain" in preference:
        print(f"{Fore.GREEN}🤖TravelBot: Awesome! Enjoy (suggestion)!🏔️") # This line is incomplete in the image
    
    elif "cities" in preference or "city" in preference:
        print(f"{Fore.RED}🤖TravelBot: Let's try another.🏙️") # This line is incomplete in the image
        recommend()
    
    else:
        print(f"{Fore.RED}🤖TravelBot: I'll suggest again.")
        recommend()
        
    print(f"{Fore.RED}🤖TravelBot: Sorry, I don't have that type of destination.") # This line is incomplete in the image

# Offer packing tips
def packing_tips():
    print(f"{Fore.CYAN}🤖TravelBot: Sure!")
    location = normalize_input(input(f"{Fore.YELLOW}You: "))
    duration = normalize_input(input(f"{Fore.YELLOW}How many days? "))
    days = int(duration)
    
    print(f"{Fore.CYAN}🤖TravelBot: Packing tips for {days} days in {location}:")
    print(f"{Fore.CYAN}👕 Pack at least one outfit per day.")
    print(f"{Fore.CYAN}🔌 Bring chargers/adapters.")
    print(f"{Fore.CYAN}💧 Stay hydrated! Journal.")

# Tell a random joke
def tell_joke():
    print(f"{Fore.YELLOW}🤖TravelBot: {random.choice(jokes)}")

# Display the main help menu
def show_help():
    print(f"{Fore.MAGENTA}🤖I can:🤖")
    print(f"{Fore.GREEN}✈️ Offer travel spots (say 'recommendation')")
    print(f"{Fore.GREEN}💼 Offer packing tips (say 'packing')")
    print(f"{Fore.GREEN}😂 Tell a joke (say 'joke')")
    print(f"{Fore.GREEN}➡️ Type 'exit' or 'bye' to end.")

# Chat function to handle user interaction
def chat():
    print(f"{Fore.CYAN}Hello! I'm TravelBot.👋")
    name = normalize_input(input(f"{Fore.YELLOW}Your name? "))
    print(f"{Fore.CYAN}Nice to meet you, {name}! :)")
    
    # Display help menu at the start
    show_help()
    
    # Main chat loop
    while True:
        user_input = normalize_input(input(f"{Fore.YELLOW}{name}: "))
        
        if "recommend" in user_input or "suggest" in user_input:
            recommend()
        elif "pack" in user_input or "packing" in user_input:
            packing_tips()
        elif "joke" in user_input or "funny" in user_input:
            tell_joke()
        elif "help" in user_input:
            show_help()
        elif "exit" in user_input or "bye" in user_input:
            print(f"{Fore.CYAN}🤖TravelBot: Safe travels! Goodbye!")
            break
        else:
            print(f"{Fore.RED}🤖TravelBot: Could you rephrase?🤔")

# Run the chatbot
if __name__ == "__main__":
    chat()
