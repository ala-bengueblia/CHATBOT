import nltk
import random
import re
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

# Download necessary NLTK data
nltk.download('punkt')

def chatbot_response(user_input):
    user_input = user_input.lower()
    
    # Define possible responses
    responses = {
        'greetings': ["\n Hello! How can I assist you today?", "Hi there! How can I help you?", "Hey! What can I do for you today?"],
        'how_are_you': ["\n I'm just a bot, but I'm here to help you!", "I'm doing great, thanks for asking! How can I assist you?", "I'm functioning as expected! How can I help you?"],
        'name_questions': ["\n I'm a simple chatbot created by a Python script.", "You can call me Chatbot!", "I'm your friendly neighborhood chatbot!"],
        'goodbyes': [" \n Goodbye! Have a great day!", "See you later!", "Take care!"],
        'unknown': [" \n I'm sorry, I didn't understand that. Can you please rephrase?", "Can you clarify that?", "I'm not sure what you mean. Could you elaborate?"],
        'weather': [" \n I can't check the weather yet, but you can try asking me something else!", "Weather functionality isn't available yet. Please ask something else."],
        'time': ["\n Current time is " + datetime.now().strftime('%H:%M:%S'), "It's " + datetime.now().strftime('%H:%M:%S') + " right now."]
    }

    # Define patterns
    patterns = {
        'greetings': re.compile(r'\b(hello|hi|hey|hola)\b'),
        'how_are_you': re.compile(r'\b(how are you|how\'s it going|how do you do)\b'),
        'name_questions': re.compile(r'\b(what is your name|who are you)\b'),
        'goodbyes': re.compile(r'\b(bye|goodbye|see you|ciao)\b'),
        'weather': re.compile(r'\b(weather)\b'),
        'time': re.compile(r'\b(time)\b')
    }
    
    # Match patterns
    for key, pattern in patterns.items():
        if pattern.search(user_input):
            return random.choice(responses[key])
    
    # Default response
    return random.choice(responses['unknown'])

def type_message(message, tag, delay=50):
    if message:
        chat_window.insert(tk.END, message[:1], (tag,))
        chat_window.after(delay, type_message, message[1:], tag, delay)
    else:
        chat_window.config(state=tk.DISABLED)
        scroll_to_end()

def typing_indicator():
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "Chatbot is typing...", 'typing')
    chat_window.update_idletasks()  # Ensure the typing indicator is visible
    chat_window.after(2000, lambda: chat_window.config(state=tk.NORMAL) or chat_window.delete('typing_start', tk.END))  # Show for 2 seconds
    chat_window.config(state=tk.DISABLED)
    scroll_to_end()

def send_message(event=None):
    user_input = entry.get()
    if user_input.strip():
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You: " + user_input + "\n", ('user',))
        chat_window.config(state=tk.DISABLED)
        entry.delete(0, tk.END)
        
        typing_indicator()
        chat_window.after(2000, lambda: type_message("Chatbot: " + chatbot_response(user_input), 'chatbot'))

def clear_chat():
    chat_window.config(state=tk.NORMAL)
    chat_window.delete(1.0, tk.END)
    chat_window.config(state=tk.DISABLED)

def copy_to_clipboard():
    chat_window.config(state=tk.NORMAL)
    chat_content = chat_window.get(1.0, tk.END)
    root.clipboard_clear()
    root.clipboard_append(chat_content)
    chat_window.config(state=tk.DISABLED)

def toggle_night_mode():
    global night_mode
    if night_mode:
        root.configure(bg="#f0f0f0")
        chat_window.config(bg="#ffffff", fg="#000000")
        entry.config(bg="#ffffff", fg="#000000")
        send_button.config(bg="#4CAF50", fg="#ffffff")
        clear_button.config(bg="#f44336", fg="#ffffff")
        copy_button.config(bg="#2196F3", fg="#ffffff")
        night_mode_button.config(bg="#FFC107", fg="#000000", text="Night Mode")
        
        # Add a fade effect for night mode
        chat_window.after(500, lambda: root.configure(bg="#ffffff"))
    else:
        root.configure(bg="#333333")
        chat_window.config(bg="#000000", fg="#ffffff")
        entry.config(bg="#555555", fg="#ffffff")
        send_button.config(bg="#4CAF50", fg="#ffffff")
        clear_button.config(bg="#f44336", fg="#ffffff")
        copy_button.config(bg="#2196F3", fg="#ffffff")
        night_mode_button.config(bg="#FFC107", fg="#000000", text="Day Mode")
        
        # Add a fade effect for day mode
        chat_window.after(500, lambda: root.configure(bg="#333333"))
    
    night_mode = not night_mode

def scroll_to_end():
    chat_window.see(tk.END)

# Set up the GUI
root = tk.Tk()
root.title("Chatbot")
root.geometry("1000x800")  # Agrandir la fenêtre principale

night_mode = False

# Configurer la police avec une taille plus grande
text_font = ('Arial', 16)  # Taille de la police agrandie

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', bg="#ffffff", fg="#000000", font=text_font)
chat_window.tag_configure('user', foreground="#007BFF", font=text_font)  # Blue for user
chat_window.tag_configure('chatbot', foreground="#28A745", font=text_font)  # Green for chatbot
chat_window.tag_configure('typing', foreground="#FF5733", font=text_font)  # Orange for typing indicator
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry_frame = tk.Frame(root, bg="#f0f0f0")
entry_frame.pack(padx=20, pady=10, fill=tk.X, expand=True)

entry = tk.Entry(entry_frame, width=100, bg="#ffffff", fg="#000000", font=text_font)  # Agrandir la zone de saisie et la police
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry.bind("<Return>", send_message)

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=5)

send_button = tk.Button(button_frame, text="Send", command=send_message, bg="#4CAF50", fg="#ffffff", font=text_font)
send_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="Clear", command=clear_chat, bg="#f44336", fg="#ffffff", font=text_font)
clear_button.pack(side=tk.LEFT, padx=10)

copy_button = tk.Button(button_frame, text="Copy", command=copy_to_clipboard, bg="#2196F3", fg="#ffffff", font=text_font)
copy_button.pack(side=tk.LEFT, padx=10)

night_mode_button = tk.Button(button_frame, text="Night Mode", command=toggle_night_mode, bg="#FFC107", fg="#000000", font=text_font)
night_mode_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
