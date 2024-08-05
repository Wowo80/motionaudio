# motionaudio
MotionAudio is a Python script that creates a video from an audio file and an image. The script allows you to specify the audio and image files, output directory, output format, and output filename through command-line arguments. It also provides options to open a settings file, reset settings to default, and use a graphical file explorer for selecting files and directories.

## Features

   - Combine an audio file and an image into a video.
   - Specify the output directory, filename, and format.
   - Use system default paths for audio, image, and video directories.
   - Open a graphical file explorer for selecting files and directories.
   - Save and load settings to/from a configuration file.
   - Reset settings to default.

## Requirements

   - Python 3.x
   - PyQt5
   - Pillow
   - ffmpeg


## Installation

1. Clone the repository:

```
git clone https://github.com/wowo80/motionaudio.git
cd motionaudio
```

2. Install the required Python packages:
```
    pip install PyQt5 Pillow
```
3. Install ffmpeg:

  - Windows: Download and install from [ffmpeg.org](ffmpeg.org)
  - macOS: Use Homebrew: brew install ffmpeg
  - Linux: Use your package manager, e.g., sudo apt install ffmpeg


    
## Usage
Command-Line Arguments

   + -a, --audio: Path to the audio file.
   + -p, --image: Path to the image file.
   + -o, --output: Path to the output directory.
   + -n, --name: Name of the output file.
   + -f, --format: Format of the output file (default is mp4).
   + -s, --settings: Open the settings file.
   + -rs, --resetsettings: Reset settings to default.

## Examples

  Basic usage with specified audio, image, and output directory:
```
python motionaudio.py -a /path/to/audio.mp3 -p /path/to/image.jpg -o /path/to/output/dir
```
Specify output filename and format:
```
python motionaudio.py -a /path/to/audio.mp3 -p /path/to/image.jpg -o /path/to/output/dir -n myvideo -f avi
```
Open settings file:
```
python motionaudio.py -s
```
Reset settings to default:
```
python motionaudio.py -rs
```


## Running Without Arguments

If you run the script without specifying arguments, it will open graphical file explorers for you to select the audio file, image file, and output directory:

## Settings

this lets you too change what happens if its not specified in the arguments
here are the settings you can change

- format: lets you change the default output format
- output directory: lets you change the default directory for the out put
- output file name: lets you change the output filesname
- audio browse path: lets you change the default browse path for audio files
- image browse path: lets you change the default browse path for image files
- output browse path: lets you change the default browse path for selecting the directory of the output file

  
