import json
import os

magicBytes = {
        '7z': {'Hex': ['377ABCAF271C'], 'Offset': [0]}, #7z archive
        'avi': {'Hex': ['52494646????????564920'], 'Offset': [0]}, #AVI video file
        'bmp': {'Hex': ['424D'], 'Offset': [0]}, #BMP image file
        'deb': {'Hex': ['213C617263683E0A'], 'Offset': [0]}, #Debian package file
        'dir (Big Endian)': {'Hex': ['52494658????????4D563933'], 'Offset': [0]}, #Directory (folder) Big Endian
        'dir (Little Endian)': {'Hex': ['58464952????????3339564D'], 'Offset': [0]}, #Directory (folder) Little Endian
        'doc': {'Hex': ['D0CF11E0A1B11AE1'], 'Offset': [0] }, #Microsoft Word document
        'exe': {'Hex': ['4D5A'], 'Offset': [0]}, #Windows executable file
        'gif': {'Hex': ['474946383961'], 'Offset' : [0]}, #GIF image file (GIF89a)
        'gz': {'Hex': ['1F8B'], 'Offset': [0]}, #Gzip compressed file
        'heic': {'Hex':['6674797068656963'], 'Offset': [4]}, #HEIC Image file (High Efficiency Image Format)
        'iso': {'Hex': ['4344303031'], 'Offset': [0x8001, 0x8801, 0x9001]}, #ISO disk image
        'jpeg': {'Hex': ['FFD8'], 'Offset': [0]}, #JPEG image file
        'mpeg': {'Hex': ['000001BA', '000001B3'], 'Offset': [0]}, #MPEG video file
        'mp3': {'Hex': ['494433','FFFB','FFF3', 'FFF2'], 'Offset': [0]}, #MP3 audio file
        'mp4': {'Hex': ['6674797069736F6D','667479704D534E56'], 'Offset': [4]}, #MP4 video file
        'pdf': {'Hex': ['255044462D'], 'Offset': [0]}, #PDF document
        'png': {'Hex': ['89504E470D0A1A0A'], 'Offset': [0]}, #PNG image file
        'rar': {'Hex': ['526172211A0700','526172211A070100'], 'Offset': [0]}, #RAR archive
        'sqlitedb': {'Hex': ['53514C69746520666F726D6174203300'], 'Offset': [0]}, #SQLite database file
        'tar': {'Hex': ['7573746172003030','7573746172202000'], 'Offset': [257]}, #TAR archive
        'tar z': {'Hex': ['1F9D','1FA0'], 'Offset': [0]}, #Z compressed file
        'txt (UTF-16LE)':{'Hex': ['FFFE'], 'Offset': [0]}, #txt files UTF-16LE encoded
        'txt (UTF-16BE)':{'Hex': ['FEFF'], 'Offset': [0]}, #txt files UTF-16BE encoded
        'txt (UTF-32LE)':{'Hex': ['FFFE0000'], 'Offset': [0]}, #txt files UTF-32LE encoded
        'txt (UTF-32BE)':{'Hex': ['FEFF0000'], 'Offset': [0]}, #txt files UTF-32BE encoded
        'wav':{'Hex':['52494646????????57415645'], 'Offset':[0]}, #WAV audio file
        'webm': {'Hex': ['1A45DFA3'], 'Offset': [0]}, #WEBM video file
        'webp': {'Hex': ['52494646????????57454250'], 'Offset': [0]}, #WEBP video file
        'zip': {'Hex': ['504B0304','504B0506','504B0708'], 'Offset': [0]} #ZIP archive
    }

path = os.path.join('fileSignatures.json')
with open(path, 'w') as file:
    json.dump(magicBytes, file, indent=4)