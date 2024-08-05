#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PIL import Image
import math
import sys
import argparse
import os
import subprocess
import configparser

default_settings = {
    'format': "'mp4'",
    'output_dir': "'{BROWSE}'",
    'default_name': "'{AUDIO}'",
    'audio_browse_path': "'{SYSTEM_MUSIC}'",
    'image_browse_path': "'{SYSTEM_PICTURES}'",
    'output_browse_path': "'{SYSTEM_VIDEOS}'"
}

class FileDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Dialog")
        self.setGeometry(100, 100, 300, 200)
        self.file_path = None
        self.directory_path = None

    def select_file(self, file_type, file_extensions, default_path):
        options = QFileDialog.Options()
        self.file_path, _ = QFileDialog.getOpenFileName(self, f"Select {file_type}", default_path, file_extensions, options=options)
        return self.file_path

    def select_directory(self, default_path):
        options = QFileDialog.Options()
        self.directory_path = QFileDialog.getExistingDirectory(self, "Select Output Directory", default_path, options=options)
        return self.directory_path

def adjust_image_dimensions(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        new_width = width if width % 2 == 0 else width - 1
        new_height = height if height % 2 == 0 else height - 1
        
        if (new_width, new_height) != (width, height):
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img.save(image_path)
    return image_path

def load_settings(settings_file='motionaudiosettings.txt'):
    config = configparser.ConfigParser()
    if os.path.exists(settings_file):
        config.read(settings_file)
        settings = {
            'format': config.get('DEFAULT', 'format', fallback=default_settings['format']).strip("'"),
            'output_dir': config.get('DEFAULT', 'output_dir', fallback=default_settings['output_dir']).strip("'"),
            'default_name': config.get('DEFAULT', 'default_name', fallback=default_settings['default_name']).strip("'"),
            'audio_browse_path': config.get('DEFAULT', 'audio_browse_path', fallback=default_settings['audio_browse_path']).strip("'"),
            'image_browse_path': config.get('DEFAULT', 'image_browse_path', fallback=default_settings['image_browse_path']).strip("'"),
            'output_browse_path': config.get('DEFAULT', 'output_browse_path', fallback=default_settings['output_browse_path']).strip("'")
        }
    else:
        settings = default_settings
    return settings

def save_settings(settings, settings_file='motionaudiosettings.txt'):
    config = configparser.ConfigParser()
    config['DEFAULT'] = settings
    with open(settings_file, 'w') as configfile:
        configfile.write("# format: Supported types: mp4, avi, mkv, etc.\n")
        configfile.write("# output_dir: Use {BROWSE} to open file explorer for selecting the path\n")
        configfile.write("# default_name: Use {AUDIO} for the audio file name or {IMAGE} for the image file name\n")
        configfile.write("# audio_browse_path: Use {SYSTEM_MUSIC} for system music directory\n")
        configfile.write("# image_browse_path: Use {SYSTEM_PICTURES} for system pictures directory\n")
        configfile.write("# output_browse_path: Use {SYSTEM_VIDEOS} for system videos directory\n")
        config.write(configfile)

def reset_settings(settings_file='motionaudiosettings.txt'):
    save_settings(default_settings, settings_file)
    print("Settings have been reset to default.")

def get_system_path(path_type):
    if path_type == 'SYSTEM_MUSIC':
        if sys.platform == 'win32': #windows
            return os.path.join(os.environ['USERPROFILE'], 'Music')
        elif sys.platform == 'darwin': #mac
            return os.path.expanduser('~/Music')
        else: #linux
            return os.path.expanduser('~/Music')
    elif path_type == 'SYSTEM_PICTURES':
        if sys.platform == 'win32': #windows
            return os.path.join(os.environ['USERPROFILE'], 'Pictures')
        elif sys.platform == 'darwin': #mac
            return os.path.expanduser('~/Pictures')
        else: #linux
            return os.path.expanduser('~/Pictures')
    elif path_type == 'SYSTEM_VIDEOS':
        if sys.platform == 'win32': #windows
            return os.path.join(os.environ['USERPROFILE'], 'Videos')
        elif sys.platform == 'darwin': #mac
            return os.path.expanduser('~/Videos')
        else: #linux
            return os.path.expanduser('~/Videos')
    return ''

def main():
    app = QApplication(sys.argv)
    file_dialog = FileDialog()
    
    settings = load_settings()

    parser = argparse.ArgumentParser(description="Create a video from an audio file and an image.")
    parser.add_argument('-a', '--audio', type=str, help="Path to the audio file")
    parser.add_argument('-p', '--image', type=str, help="Path to the image file")
    parser.add_argument('-o', '--output', type=str, help="Path to the output directory")
    parser.add_argument('-n', '--name', type=str, help="Name of the output file")
    parser.add_argument('-f', '--format', type=str, help="Format of the output file", default=settings['format'])
    parser.add_argument('-s', '--settings', action='store_true', help="Open settings file")
    parser.add_argument('-rs', '--resetsettings', action='store_true', help="Reset settings to default")

    args = parser.parse_args()

    if args.settings:
        if not os.path.exists('motionaudiosettings.txt'):
            save_settings(default_settings)
        if sys.platform == 'win32':
            os.startfile('motionaudiosettings.txt')
        elif sys.platform == 'darwin':
            subprocess.call(['open', 'motionaudiosettings.txt'])
        else:
            subprocess.call(['xdg-open', 'motionaudiosettings.txt'])
        return

    if args.resetsettings:
        reset_settings()
        return

    audio_file = args.audio or file_dialog.select_file('Audio File', 'Audio Files (*.mp3 *.wav *.aac *.flac *.ogg *.wma *.m4a *.aiff *.alac *.opus)', get_system_path('SYSTEM_MUSIC'))
    image_file = args.image or file_dialog.select_file('Image File', 'Image Files (*.png *.jpg *.jpeg *.bmp *.tiff *.heif *.jfif)', get_system_path('SYSTEM_PICTURES'))
    output_dir = args.output or (file_dialog.select_directory(get_system_path('SYSTEM_VIDEOS')) if settings['output_dir'] == '{BROWSE}' else settings['output_dir'])

    if args.name:
        output_name = args.name
    else:
        output_name = settings['default_name']
        if '{AUDIO}' in output_name:
            output_name = output_name.replace('{AUDIO}', os.path.splitext(os.path.basename(audio_file))[0])
        if '{IMAGE}' in output_name:
            output_name = output_name.replace('{IMAGE}', os.path.splitext(os.path.basename(image_file))[0])

    output_format = args.format or settings['format']
    output_path = os.path.join(output_dir, f"{output_name}.{output_format}")

    image_file = adjust_image_dimensions(image_file)

    # Create video using ffmpeg
    command = [
        'ffmpeg',
        '-loop', '1',
        '-i', image_file,
        '-i', audio_file,
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        output_path
    ]

    subprocess.run(command, check=True)
    print(f"Video created at {output_path}")

if __name__ == "__main__":
    main()
