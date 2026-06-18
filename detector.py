from utils import load_file_signatures, compute_needed_bytes, parse_offset
import json
import os
from datetime import datetime
import stat

class FileDetector:
    def __init__(self, path='Reports', format='json', verbose=False):
        self.magicBytes = load_file_signatures()
        self.needed = compute_needed_bytes(self.magicBytes)
        self.path = path
        self.format = format
        self.verbose = verbose
    
    def analyze(self,ip_path):
        
        # If verbose mode is enabled
        if self.verbose:
            print(f"Analyzing file: {ip_path}")
        
        # Trying to open the file in "Read Binary" mode
        try:
            with open(ip_path,'rb') as file:
                if self.verbose:
                    print(f"Successfully opened the file: {ip_path}")
                    print(f"Reading the {self.needed} bytes of the file for analysis...")
                content = file.read(self.needed) #Read the first 512 bytes of the file
            if self.verbose:
                print(f"Successfully read {len(content)} bytes from the file.")
        
        # If the file not is found
        except FileNotFoundError:
            print(f"Error: File Not Found: {ip_path}")
            return
        
        # If permission is denied
        except PermissionError:
            print(f"Error: Permission Denied: {ip_path}")
            return
        
        # Other exceptions
        except Exception as e:
            print(f"Error reading file: {e}")
            return
        
        if self.verbose:
            print(f"Detecting file type based on the read bytes...")
        
        # Calling function to analyze the file type of the file
        file_types = self.detect_file_type(content)
        
        # If no magic-bytes match, trying simple text heuristics (JSON, CSV, plain text)
        if not file_types:
            text_type = self.detect_text_like(content)
            if text_type:
                file_types = text_type

        if self.verbose:
            print(f"Creating a report for the file...")

        # Detect file encoding and build the report dictionary
        encoding = self.detect_encoding(content)
        report = self.generate_report_dict(file_types=file_types, encoding=encoding, ip_path=ip_path)

        if self.verbose:
            print(f"Report generated for file: {report['File Name']}")
        
        # Returning the dictionary
        return report

    # Function to create a report dictionary
    def generate_report_dict(self, file_types, encoding, ip_path):
        report = {}
        stats = os.stat(ip_path)
        # Updating the report dictionary
        report['File Name'], _ = os.path.splitext(os.path.basename(ip_path))
        report['File Size'] = stats.st_size
        report['File Type'] = file_types if file_types else 'Unknown'
        report['Encoding'] = encoding
        report['Creation Time'] = datetime.fromtimestamp(getattr(stats, 'st_birthtime', stats.st_ctime)).strftime('%Y-%m-%d %H:%M:%S')
        report['Modification Time'] = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        report['Access Time'] = datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')

        permissions = stat.filemode(stats.st_mode)
        if self.format == 'json':
            report['Permissions'] = {
                'Owner': permissions[1:4],
                'Group': permissions[4:7],
                'Others': permissions[7:10]
            }
        else:
            report['Owner Permissions'] = permissions[1:4]
            report['Group Permissions'] = permissions[4:7]
            report['Others Permissions'] = permissions[7:10]
        report['File Index'] = stats.st_ino
        report['Absolute File Path'] = os.path.abspath(ip_path)
        report['Path'] = self.path or 'Reports'
        report['Report Path'] = self.path or 'Reports'

        return report

    # Function to detect the file type of a file
    def detect_file_type(self,file_bytes):
        
        # List that will contain the possible file types
        res = []
        if self.verbose:
            print(f"Analyzing file with {len(file_bytes)} bytes read for signature matching...")
        
        # Getting the {key:value} pair of file types and their magic bytes
        for k, v in self.magicBytes.items():
            for signature in v['Hex']:
                
                # If the file signature has odd number of bytes, error
                if len(signature) % 2 != 0:
                    raise ValueError("Error: Invalid signature length: must be an even number of characters.")
                
                # Calling the helper function to see for matches and appending to res if found
                if self.match_file_signature(file_bytes, signature, v['Offset']):
                    res.append(k)
        if res:
            if self.verbose:
                print(f"File type(s) detected: {', '.join(res)}")
            return ', '.join(res)
        else:
            if self.verbose:
                print("No file type detected based on the signatures.")
            return None
        
    # Heuristic to detect text-like files (JSON, CSV, plain text)
    def detect_text_like(self, data):
        try:
            s = data.decode('utf-8', errors='ignore')
        except Exception:
            return None
        if not s:
            return None
        stripped = s.lstrip()

        # JSON heuristic
        if stripped.startswith('{') or stripped.startswith('['):
            try:
                json.loads(stripped)
                return 'JSON'
            except Exception:
                pass

        # CSV heuristic: presence of commas in first few lines
        lines = s.splitlines()
        sample = lines[:10]
        comma_lines = sum(1 for line in sample if ',' in line)
        if comma_lines >= 1 and len(sample) > 0:
            return 'CSV'

        # Plain text heuristic: high printable character ratio and few NUL bytes
        if b'\x00' in data:
            return None
        printable = 0
        total = 0
        for ch in s:
            total += 1
            if ch.isprintable() or ch.isspace():
                printable += 1
        if total == 0:
            return None
        if (printable / total) >= 0.95:
            return 'Text'
        return None

    def detect_encoding(self, data):
        # Detect common text encodings using byte order marks and decode attempts.
        if data.startswith(b'\xef\xbb\xbf'):
            return 'UTF-8 with BOM'
        if data.startswith(b'\xff\xfe'):
            return 'UTF-16 LE with BOM'
        if data.startswith(b'\xfe\xff'):
            return 'UTF-16 BE with BOM'

        encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'cp1252', 'latin-1']
        for encoding in encodings:
            try:
                data.decode(encoding)
                return encoding.upper()
            except Exception:
                continue

        # If the data is mostly printable ASCII, classify as ASCII text.
        if all(byte == 0 or 32 <= byte < 127 for byte in data):
            return 'ASCII'

        return 'Binary'
    
    # Helper function to match the file signatures to the data bytes of the read file
    def match_file_signature(self, Databytes, signature, offsets):
        checkLen = len(signature) // 2
        for offset in offsets:
            offset = parse_offset(offset)
            if offset is None or offset < 0:
                continue
            if offset + checkLen > len(Databytes):
                continue
            chunk = Databytes[offset:offset + checkLen].hex().upper()
            if all(sc == '?' or sc == dc for sc, dc in zip(signature.upper(), chunk)):
                return True
        return False