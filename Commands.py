import win32gui # type: ignore
import win32api # type: ignore
import screen_brightness_control as sbc
import webbrowser
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import subprocess

def microfon_enabled():
    WM_APPCOMMAND = 0x319
    APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)

def brightness_up():
    primary_brightness = sbc.get_brightness(display=0)[0]
    if (primary_brightness > 89):
        sbc.set_brightness(100, display=0)
    else:    
        sbc.set_brightness(primary_brightness + 10, display=0)

def brightness_down():
    primary_brightness = sbc.get_brightness(display=0)[0]
    if (primary_brightness < 11):
        sbc.set_brightness(0, display=0)
    else:    
        sbc.set_brightness(primary_brightness - 10, display=0)

def volume_min():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-65.0, None)

def volume_max():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(0, None)

def volume_up():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    currentVolumeDb = volume.GetMasterVolumeLevel()
    if (currentVolumeDb > -10):
        volume_max()
    else:
        volume.SetMasterVolumeLevel(currentVolumeDb+10, None)

def volume_down():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    currentVolumeDb = volume.GetMasterVolumeLevel()
    if (currentVolumeDb < -30.0):
        volume_min()
    else:
        volume.SetMasterVolumeLevel(currentVolumeDb-5, None)

def open_web_page(page):
    webbrowser.open(page)

def run_word():
    subprocess.run('start winword', shell=True)

def run_open_office():
    subprocess.run('start powerpnt', shell=True)

