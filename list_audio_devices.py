from pycaw.pycaw import AudioUtilities

def list_audio_devices():
    devices = AudioUtilities.GetAllDevices()
    for device in devices:
        print(f"Device Name: {device.FriendlyName}")

if __name__ == "__main__":
    list_audio_devices()
