'''Lesson 2: Sentiment Analysis using the Coloroma and TextBlob Libraries'''
# Import colorama
from colorama import Fore, Style
from textblob import TextBlob

# Initialize colorama for colored output
colorama.init()

# Welcome message for the start of the program
print(f"{Fore.CYAN} 🕵️‍♂️ Welcome to Sentiment Spy! 🕵️‍♀️{Style.RESET_ALL}")

# Prompt user for their name, defaulting to "Mystery Agent" if no name is provided
user_name = input(f"{Fore.MAGENTA}Please enter your name: {Style.RESET_ALL}").strip()
if not user_name:
    user_name = "Mystery Agent" # Fallback if user doesn't provide a name

# Create an empty list to store conversation history
conversation_history = []

# Greet the user and explain the program's purpose
print(f"\n{Fore.CYAN}Hello, Agent {user_name}! 👋")
print(f"{Fore.CYAN}I will analyze your sentences with TextBlob and show you the sentiment. 🧠")
print(f"{Fore.CYAN}You can type 'history' to see your history ({Fore.CYAN}history{Fore.CYAN})")
print(f"{Fore.YELLOW}or 'exit' ({Fore.YELLOW}exit{Fore.YELLOW}) to quit.{Style.RESET_ALL}\n")

# Main loop for user interaction
while True:
    user_input = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()

    # Check if user input is empty
    if not user_input:
        print(f"{Fore.RED}Please enter some text or a valid command.{Style.RESET_ALL}")
        continue

    # Check for commands
    if user_input.lower() == "exit":
        print(f"{Fore.BLUE} 👋 Exiting Sentiment Spy. Farewell, Agent {user_name}! 🤖{Style.RESET_ALL}")
        break
    
    elif user_input.lower() == "clear":
        conversation_history.clear()
        print(f"{Fore.CYAN} ✅ All conversation history cleared!{Style.RESET_ALL}")
        continue
    
    elif user_input.lower() == "history":
        if not conversation_history:
            print(f"{Fore.YELLOW}No conversation history yet.{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}📜 Conversation History:{Style.RESET_ALL}")
            for idx, (text, polarity, sentiment_type) in enumerate(conversation_history, start=1):
                # Choose color and emoji based on sentiment
                if sentiment_type == "Positive":
                    color = Fore.GREEN
                    emoji = "😀"
                elif sentiment_type == "Negative":
                    color = Fore.RED
                    emoji = "😞"
                else: # Neutral
                    color = Fore.YELLOW
                    emoji = "😐"
                
                print(f" {idx}. {color}{emoji} {text}{Style.RESET_ALL} (polarity: {polarity:.2f}, {sentiment_type}) {Style.RESET_ALL}")
        continue
    
    # Analyze sentiment
    try:
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity
        
        # Determine sentiment type and corresponding emoji
        if polarity > 0:
            sentiment_type = "Positive"
            color = Fore.GREEN
            emoji = "😀"
        elif polarity < 0:
            sentiment_type = "Negative"
            color = Fore.RED
            emoji = "😞"
        else:
            sentiment_type = "Neutral"
            color = Fore.YELLOW
            emoji = "😐"

        # Store in history
        conversation_history.append((user_input, polarity, sentiment_type))

        # Print result with color, emoji, and polarity
        print(f"{color}{emoji} {sentiment_type} Sentiment Detected! 🔬")
        print(f"Polari ty: {polarity:.2f}{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
