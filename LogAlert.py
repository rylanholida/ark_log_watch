import win32gui
import re
import pyautogui
import time
import discord
import sys

print("Author: Cinder\n")
print("Description:\nLooks at the first 4 lines in tribe log and searches for any\nnew 'destroyed' words and prints to the #tribe-log channel\n")

client = discord.Client()

# Activate Ark window
class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

w = WindowMgr()
w.find_window_wildcard(".*ARK.*")
w.set_foreground()

time.sleep(1)

pyautogui.screenshot('screenshot.png', region=(1340, 184, 455, 32))  # Get initial image

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print("\nClose this window to exit the script.\n")
    channel = client.get_channel(863757173812232202)  # tribe-log

    while True:
        if not (pyautogui.locateOnScreen('screenshot.png', region=(1340, 184, 455, 70), confidence=0.7)):
            destroyed = pyautogui.locateOnScreen('destroyed.png', region=(1340, 184, 455, 70), confidence=0.7)
            if destroyed != None:
                print("Something was destroyed!")
                pyautogui.screenshot('screenshot.png', region=(1340, destroyed[1]-20, 455, 32))
                #await channel.send("Something was destroyed!\n@here")
                await channel.send(file=discord.File("screenshot.png"))

client.run("TOKEN")
