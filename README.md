 # Audio Splitter App

This project allows you to split Chrome's audio between two screens based on which screen the Chrome window is currently displayed.

## Table of Contents
- [Audio Splitter App](#audio-splitter-app)
- [Table of Contents](#table-of-contents)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Enabling the Audio Splitter](#enabling-the-audio-splitter)
  - [Disabling the Audio Splitter](#disabling-the-audio-splitter)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Project Structure

The project directory contains the following files and folders:

AudioSplitterApp/ <br />
│ <br />
├── venv/ <br />
│ ├── Scripts/ <br />
│ │ ├── activate <br />
│ <br />
├── audio_splitter.py <br />
├── list_audio_devices.py <br />
├── requirements.txt <br />
├── README.md <br />

- `venv/`: Virtual environment directory.
- `audio_splitter.py`: Main script for splitting audio based on the Chrome window's screen.
- `list_audio_devices.py`: Helper script to list available audio devices.
- `requirements.txt`: Lists the required packages for the project.
- `README.md`: This README file.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your_username/AudioSplitterApp.git
   cd AudioSplitterApp
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix-based systems
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Enabling the Audio Splitter

1. Run the `audio_splitter.py` script:
   ```sh
   python audio_splitter.py
   ```
2. A system tray icon will appear. Click on the icon and select `Enable` to start monitoring Chrome windows and switching audio devices based on their screen location.

### Disabling the Audio Splitter

1. To disable the audio splitter, click on the system tray icon and select `Disable`. This will stop the monitoring process.

## Acknowledgements

1. This project uses `pygetwindow` for Chrome window management.
2. `pystray` is used to create the system tray icon for controlling the application.
3. `soundcard` library is used for managing audio devices.
4. `Pillow` is used for creating and modifying the tray icon image.