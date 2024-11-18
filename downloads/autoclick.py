from pynput import mouse, keyboard
import time
import threading

# Set the delay between each click (30 CPS = 0.033 seconds per click)
click_delay = 0.033

# Initialize mouse and keyboard controllers
mouse_controller = mouse.Controller()

# Flags to control autoclicking for left and right buttons
is_left_clicking = False
is_right_clicking = False

def left_click_mouse():
    """Repeatedly click the left mouse button while is_left_clicking is True."""
    while is_left_clicking:
        mouse_controller.click(mouse.Button.left)
        time.sleep(click_delay)

def right_click_mouse():
    """Repeatedly click the right mouse button while is_right_clicking is True."""
    while is_right_clicking:
        mouse_controller.click(mouse.Button.right)
        time.sleep(click_delay)

def on_press(key):
    global is_left_clicking, is_right_clicking
    # Start left-click autoclicking when the 'B' key is pressed
    if key == keyboard.KeyCode.from_char('x') and not is_left_clicking:
        is_left_clicking = True
        threading.Thread(target=left_click_mouse).start()
    # Start right-click autoclicking when the 'V' key is pressed
    elif key == keyboard.KeyCode.from_char('c') and not is_right_clicking:
        is_right_clicking = True
        threading.Thread(target=right_click_mouse).start()

def on_release(key):
    global is_left_clicking, is_right_clicking
    # Stop left-click autoclicking when the 'B' key is released
    if key == keyboard.KeyCode.from_char('x'):
        is_left_clicking = False
    # Stop right-click autoclicking when the 'V' key is released
    if key == keyboard.KeyCode.from_char('c'):
        is_right_clicking = False

# Set up the keyboard listener
print("Hold 'X' for left-click autoclicking, 'C' for right-click autoclicking. Release to stop.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
