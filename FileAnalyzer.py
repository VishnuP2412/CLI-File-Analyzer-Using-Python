import os
import json, csv
import argparse
from cli import main

if __name__ == '__main__':
    status_code = main()
    print(f"Program ended with the status code {status_code}")