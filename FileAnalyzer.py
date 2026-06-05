import os
import json, csv
import argparse

# argparse path option
# path = sys.argv[0]

class FileTypeDetector:
    
    def __init__(self, path='Reports', format='json', verbose=False):
        self.magicBytes = self.load_file_signatures()
        self.needed = self.compute_needed_bytes()
        self.path = path
        self.format = format
        self.verbose = verbose

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
        
        if self.verbose:
            print(f"Analyzing file: {path}")
        try:
            with open(path,'rb') as file:
                if self.verbose:
                    print(f"Successfully opened the file: {path}")
                    print(f"Reading the {self.needed} bytes of the file for analysis...")
                content = file.read(self.needed) #Read the first 512 bytes of the file
            if self.verbose:
                print(f"Successfully read {len(content)} bytes from the file.")
        except FileNotFoundError:
            print(f"File Not Found: {path}")
            return
        except PermissionError:
            print(f"Permission Denied: {path}")
            return
        except Exception as e:
            print(f"Error reading file: {e}")
            return
        
        report = {}
        if self.verbose:
            print(f"Detecting file type based on the read bytes...")
        file_types = self.detect_file_type(content)
        # If no magic-bytes match, try simple text heuristics (JSON, CSV, plain text)
        if not file_types:
            text_type = self.detect_text_like(content)
            if text_type:
                file_types = text_type
        if self.verbose:
            print(f"Creating a report for the file...")
        report['File Name'],_ = os.path.splitext(os.path.basename(path))
        report['File Size'] = os.stat(path).st_size
        report['File Type'] = file_types if file_types else 'Unknown'

        if self.verbose:
            print(f'Report generated for file: {path}')
        output_dir = self.path or 'Reports'
        os.makedirs(output_dir, exist_ok=True)
        if self.format == 'json':
            if self.verbose:
                print(f"Saving report to: {output_dir} as JSON format...")
            report_path = os.path.join(output_dir, report['File Name'] + '_report.json')
            with open(report_path, 'w') as report_file:
                json.dump(report, report_file, indent=4)
        elif self.format == 'csv':
            if self.verbose:
                print(f"Saving report to: {output_dir} as CSV format...")
            report_path = os.path.join(output_dir, report['File Name'] + '_report.csv')
            with open(report_path, 'w', newline='') as report_file:
                writer = csv.writer(report_file)
                writer.writerow(['Key', 'Value'])
                for k, v in report.items():
                    writer.writerow([k, v])
        else:
            raise ValueError(f"Unsupported format: {self.format}")
        if self.verbose:
            print(f"Report saved to: {report_path}")
        report['report_path'] = report_path
        return report

    # Function to detect the file type based ont the loaded file signatures and the read bytes of the file
    def detect_file_type(self,Filebytes):
        res = []
        if self.verbose:
            print(f"Analyzing file with {len(Filebytes)} bytes read for signature matching...")
        for k, v in self.magicBytes.items():
            for signature in v['Hex']:
                if len(signature) % 2 != 0:
                    raise ValueError("Invalid signature length: must be an even number of characters.")
                if self.match_file_signature(Filebytes, signature, v['Offset']):
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

def main():
    print('='*50)
    print('FILE DETECTOR AND METADATA ANALYZER')
    print('='*50)
    parser = argparse.ArgumentParser(description='CLI File Type Detector and Metadata Analyzer')
    parser.add_argument('--file', '-f', action='store', help='Path to the file to analyze')
    parser.add_argument('--batch', '-b', action='store', help='Path to the folder to analyze')
    parser.add_argument('--format', '-fmt', action='store', help='Output format for the report (json, csv)', default='json')
    parser.add_argument('--recursive', '-r', action='store_true', help='Recursively analyze files in subdirectories (only with --batch)')
    parser.add_argument('--output', '-o', action='store', help='Path to the folder where reports will be saved', default='Reports')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    output_dir = args.output or 'Reports'
    format_arg = args.format.lower() if args.format else 'json'
    if format_arg not in ('json', 'csv'):
        print('Invalid format specified. Defaulting to JSON.')
        format_arg = 'json'

    detector = FileTypeDetector(path=output_dir, format=format_arg, verbose=args.verbose)

    if args.verbose:
        print('Verbose mode enabled.')
        print(f'Output directory set to: {output_dir}')
        print(f'Report format set to: {detector.format}')

    if args.file and args.batch:
        print('Please use either --file or --batch, not both.')
        return
    if args.file:
        report = detector.analyze(args.file)
        if report:
            print('Report generated for file:', args.file)
            print('Your report:')
            for k, v in report.items():
                print(f'{k} : {v}')
            print('End of report')
    elif args.batch:
        if not os.path.isdir(args.batch):
            print(f'Batch folder not found: {args.batch}')
            return
        for root, _, files in os.walk(args.batch):
            for file in files:
                file_path = os.path.join(root, file)
                report = detector.analyze(file_path)
                if report:
                    print('=' * 50)
                    print('Report generated for file:', file_path)
                    print('Your report:')
                    for k, v in report.items():
                        print(f'{k} : {v}')
                    print('End of report')
            if not args.recursive:
                break
    else:
        parser.print_help()
        return
        

if __name__ == '__main__':
    main()