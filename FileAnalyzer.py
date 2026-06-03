import os
import json
import sys
import argparse

# argparse path option
# path = sys.argv[0]

class FileTypeDetector:
    
    def __init__(self):
        self.magicBytes = self.load_file_signatures()
        self.needed = self.compute_needed_bytes()

    # Function to load the file signatures from the JSON file and validate their format
    def load_file_signatures(self):
        try:
            with open('fileSignatures.json', 'r') as file:
                signatures = json.load(file)
            for v in signatures.values():
                if 'Hex' not in v or 'Offset' not in v:
                    raise ValueError("Invalid signature format: each entry must contain 'Hex' and 'Offset' keys.")
                if not isinstance(v['Hex'], list):
                    raise ValueError("Invalid signature format: 'Hex' must be a list.")
                if not isinstance(v['Offset'], list):
                    raise ValueError("Invalid signature format: 'Offset' must be a list.")
            return signatures
        
        except Exception as e:
            print(f"Error loading file signatures: {e}")
            return {}

    # Function to compute the maximum number of bytes needed to read based on the loaded file signatures and their offsets
    def compute_needed_bytes(self):
        needed = 512 #Default value if no signatures are loaded
        for v in self.magicBytes.values():
            for signature in v['Hex']:
                if len(signature) %2 != 0:
                    continue
                sig_len = len(signature) // 2
                for off in v['Offset']:
                    off = self.parse_offset(off)
                    if off is None or off < 0:
                        continue
                    needed = max(needed, off + sig_len)
        return needed

    # Helper function to parse offsets which can be in decimal or hexadecimal format
    def parse_offset(self, offset):
        try:
            return int(offset, 0) if isinstance(offset, str) else int(offset)
        except Exception:
            return None

    # Function to analyze the file and generate a report based on the detected file type and metadata  
    def analyze(self,path):
        try:
            with open(path,'rb') as file:
                content = file.read(self.needed) #Read the first 512 bytes of the file
        except FileNotFoundError:
            print(f"File Not Found")
            return
        except PermissionError:
            print(f"Permission Denied")
            return
        except Exception as e:
            print(f"Error reading file: {e}")
            return
        
        report = {}
        file_types = self.detect_file_type(content)
        report['File Name'],_ = os.path.splitext(os.path.basename(path))
        report['File Size'] = os.stat(path).st_size
        report['File Type'] = file_types if file_types else 'Unknown'
        
        os.makedirs('Reports', exist_ok=True)
        report_path = os.path.join('Reports', report['File Name'] + '_report.json')
        with open(report_path,'w') as report_file:
            json.dump(report, report_file, indent=4)
        report['report_path'] = report_path
        return report

    # Function to detect the file type based ont the loaded file signatures and the read bytes of the file
    def detect_file_type(self,Filebytes):
        res = []
        for k, v in self.magicBytes.items():
            for signature in v['Hex']:
                if len(signature) % 2 != 0:
                    raise ValueError("Invalid signature length: must be an even number of characters.")
                if self.match_file_signature(Filebytes, signature, v['Offset']):
                    res.append(k)
        return res if res else None
    
    # Helper function to match the file signatures to the data bytes of the read file
    def match_file_signature(self, Databytes, signature, offsets):
        checkLen = len(signature) // 2
        for offset in offsets:
            offset = self.parse_offset(offset)
            if offset is None or offset < 0:
                continue
            if offset + checkLen > len(Databytes):
                continue
            chunk = Databytes[offset:offset + checkLen].hex().upper()
            if all(sc == '?' or sc == dc for sc, dc in zip(signature.upper(), chunk)):
                return True
        return False

def getFile():
    detector = FileTypeDetector()
    print('='*50)
    print('FILE DETECTOR AND METADATA ANALYZER')
    while True:
        print('='*50)
        path = input('Enter the absolute path to the file (or \'Q\' to quit ):')
        if path.upper() == 'Q':
            break
        report = detector.analyze(path)
        if report:
            print('Your report:')
            for k,v in report.items():
                print(f'{k} : {v}')
            print('End of report')
            print('Your report has been saved to: ', report['report_path'])
        else:
            print('No report generated for the file.')
    print('Thank you for using my file analyzer, goodbye!')
    # choice = input('Press Y to view the report or N to exit the Program: ')
    # if choice.upper() ==' Y':
    #     pass
    # else:
    #     sys.exit

if __name__ == '__main__':
    getFile()

    parser = argparse.ArgumentParser(description='CLI File Type Detector and Metadata Analyzer')
    parser.add_argument('--file', '-f', action = 'store', help='Path to the file to analyze')