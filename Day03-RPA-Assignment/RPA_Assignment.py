import pyautogui
import time

# Wait before starting
time.sleep(2)

# 1. Open Windows Run
pyautogui.hotkey("win", "r")
time.sleep(1)

# 2. Open Notepad
pyautogui.write("notepad", interval=0.1)
pyautogui.press("enter")
time.sleep(2)

# 3. Write first line
pyautogui.write("Hello, this is my first line.", interval=0.05)
pyautogui.press("enter")

# 4. Write second line
pyautogui.write(
    "This is my second line using PyAutoGUI.",
    interval=0.05
)

# 5. Take screenshot BEFORE saving
pyautogui.screenshot("notepad_before_save.png")

print("Screenshot captured: notepad_before_save.png")

# 6. Save the file
pyautogui.hotkey("ctrl", "s")
time.sleep(2)

# 7. Enter file name
pyautogui.write("pyautogui_demo.txt", interval=0.05)

# 8. Save
pyautogui.press("enter")

time.sleep(2)

print("File saved successfully!")