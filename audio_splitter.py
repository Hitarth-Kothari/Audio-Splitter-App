import sys
import time
import pygetwindow as gw
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import soundcard as sc
import ctypes


class AudioController:
    def __init__(self):
        # Update these device names to match your actual devices
        self.screen1_device = "Speakers (Realtek(R) Audio)"  # Replace with your actual device name for the main screen
        self.screen2_device = "HDMI (NVIDIA High Definition Audio)"  # Replace with your actual device name for the second screen
        self.is_running = False
        # Dictionary to track the last known screen for each Chrome window
        self.window_screens = {}

    def get_chrome_windows(self):
        """Find and return all Chrome windows."""
        windows = gw.getWindowsWithTitle('Google Chrome')
        if windows:
            return windows
        else:
            return []

    def set_audio_device(self, device_name):
        """Set the default audio playback device using soundcard library."""
        print(f"Attempting to set audio output to: {device_name}")

        speakers = sc.all_speakers()
        target_speaker = None

        for speaker in speakers:
            if device_name.lower() in speaker.name.lower():
                target_speaker = speaker
                break

        if target_speaker is None:
            print(f"Device '{device_name}' not found.")
            return False

        try:
            sc.default_speaker = target_speaker
            print(f"Audio output set to: {device_name}")
            return True
        except Exception as e:
            print(f"Error setting default device: {e}")
            return False

    def get_screen_for_window(self, window):
        """Determine which screen the window is on based on its position."""
        if window.left + window.right <= 0:  
            return "screen2"
        else:
            return "screen1"

    def monitor_chrome_windows(self):
        """Monitor Chrome window positions and update audio output based on screen."""
        ctypes.windll.ole32.CoInitialize(None)
        
        print("Starting Chrome window monitoring...")
        try:
            while self.is_running:
                chrome_windows = self.get_chrome_windows()
                for window in chrome_windows:
                    current_screen = self.get_screen_for_window(window)
                    window_id = window._hWnd

                    if window_id in self.window_screens:
                        last_screen = self.window_screens[window_id]
                        if current_screen != last_screen:
                            if current_screen == "screen2" and self.screen2_device:
                                if self.set_audio_device(self.screen2_device):
                                    print(f"Switched audio to {self.screen2_device} for window: {window.title}")
                            elif current_screen == "screen1" and self.screen1_device:
                                if self.set_audio_device(self.screen1_device):
                                    print(f"Switched audio to {self.screen1_device} for window: {window.title}")
                            self.window_screens[window_id] = current_screen
                            print(f"Window '{window.title}' moved from {last_screen} to {current_screen}")
                    else:
                        self.window_screens[window_id] = current_screen

                time.sleep(1)
        finally:
            # Ensure COM is uninitialized properly
            ctypes.windll.ole32.CoUninitialize()

    def start(self):
        """Start monitoring windows in a background thread."""
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self.monitor_chrome_windows)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print("Started audio controller.")

    def stop(self):
        """Stop the monitoring and audio control."""
        self.is_running = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join()
        print("Stopped audio controller.")


class SystemTrayApp:
    def __init__(self):
        self.audio_controller = AudioController()
        self.icon = None
        self.is_enabled = False

    def create_icon(self):
        """Create the system tray icon."""
        image = Image.new('RGB', (64, 64), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 0), (64, 64)], fill="blue")
        self.icon = pystray.Icon("Audio Splitter", image, menu=self.create_menu())

    def create_menu(self):
        """Create the system tray menu."""
        if not self.is_enabled:
            return (
                item('Enable', self.toggle_enable),
                item('Quit', self.quit)
            )
        else:
            return (
                item('Disable', self.toggle_enable),
                item('Quit', self.quit)
            )   

    def toggle_enable(self, icon, item):
        """Toggle the enabling/disabling of the app."""
        if self.is_enabled:
            self.audio_controller.stop()
            icon.icon = Image.new('RGB', (64, 64), color=(255, 255, 255))  # Change icon to indicate stopped
            self.is_enabled = False
            print("Audio splitter disabled.")
        else:
            self.audio_controller.start()
            icon.icon = Image.new('RGB', (64, 64), color=(0, 255, 0))  # Change icon to indicate running
            self.is_enabled = True
            print("Audio splitter enabled.")

    def quit(self, icon, item):
        """Quit the application."""
        self.audio_controller.stop()
        icon.stop()
        print("Quitting audio splitter app...")

    def run(self):
        """Run the system tray application."""
        self.create_icon()
        self.icon.run()


if __name__ == "__main__":
    app = SystemTrayApp()
    app.run()
