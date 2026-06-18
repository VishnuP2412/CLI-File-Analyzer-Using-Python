import json
def load_file_signatures():
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
        
def parse_offset( offset):
        try:
            return int(offset, 0) if isinstance(offset, str) else int(offset)
        except Exception:
            return None

def compute_needed_bytes(magicBytes):
        needed = 512 #Default value if no signatures are loaded
        for v in magicBytes.values():
            for signature in v['Hex']:
                if len(signature) %2 != 0:
                    continue
                sig_len = len(signature) // 2
                for off in v['Offset']:
                    off = parse_offset(off)
                    if off is None or off < 0:
                        continue
                    needed = max(needed, off + sig_len)
        return needed