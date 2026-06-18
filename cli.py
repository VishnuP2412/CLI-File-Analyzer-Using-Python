import argparse
import os
from detector import FileDetector
from report import make_report

class CommandLineInterface:
    def __init__(self):
        pass
    
    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='CLI File Type Detector and Metadata Analyzer')
        parser.add_argument('--file','-f', action='store', help='Path to the file to analyze')
        parser.add_argument('--batch','-b', action='store', help='Path to a the folder to analyze')
        parser.add_argument('--format','-fmt', action = 'store',help='Output format for the report (json,csv)', default='json')
        parser.add_argument('--recursive','-r', action='store_true',help='Recursively analyze files in subdirectories (works only with --batch)')
        parser.add_argument('--output','-o',action='store', help='Path to the folder where reports will be saved', default='Reports')
        parser.add_argument('--verbose','-v',action='store_true', help='Enable a verbose output')
        return parser, parser.parse_args()


def main():
    
    parser, args = CommandLineInterface().parse_arguments()

    print(r"""  ___  __    __    ____  __  __    ____     __   __ _   __   __    _  _  ____  ____  ____ """)
    print(r""" / __)(  )  (  )  (  __)(  )(  )  (  __)   / _\ (  ( \ / _\ (  )  ( \/ )(__  )(  __)(  _ \ """)
    print(r"""( (__ / (_/\ )(    ) _)  )( / (_/\ ) _)   /    \/    //    \/ (_/\ )  /  / _/  ) _)  )   / """)
    print(r""" \___)\____/(__)  (__)  (__)\____/(____)  \_/\_/\_)__)\_/\_/\____/(__/  (____)(____)(__\_) """)
    
    format_args = args.format.lower() if args.format else 'json'

    # Checks if the output format is correct or not
    if format_args not in ('json','csv'):
        print("Invalid output format specified. Defaulting to JSON")
        format_args = 'json'
    
    # Assigns the output directory if specified else defaults to Reports folder
    output_dir = args.output or 'Reports'

    # Checks if verbose mode has been enabled or not
    if args.verbose:
        print('Verbose mode enabled')
        print(f'Output directory set to: {output_dir}')
        print(f'Report format set to: {format_args}')

    # Checks if both --file and --batch flags are used. If used, return with status code 1
    if args.file and args.batch:
        print("Error: Please use --file or --batch, not both.")
        return 1
    
    # If --file flag was used
    if args.file:
        
        # Creating an FileDetector object
        Analyzer = FileDetector(
            path=output_dir,
            format=format_args,
            verbose=args.verbose )

        # Analyzing the file and getting the dictionary containing details of the file
        report = Analyzer.analyze(ip_path=args.file)
        
        # If no report dictionary was created
        if not report:
            print("Error: No report was created.")
            return 1
        
        # Creating a report in the specified format or default format(json)
        final_report = make_report(report=report,reportFormat=format_args,verbose=args.verbose)
        
        # Printing the report contents
        for k,v in final_report.items():
            print(f'{k}:{v}')
        print('End of reports')
        return 0
    
    # If --batch flag was used
    elif args.batch:

        # Creating an FileDetector object
        Analyzer = FileDetector(
            path=output_dir,
            format=format_args,
            verbose=args.verbose )
        
        # If the given path does not exist
        if not os.path.exists(args.batch):
            print("Error: No directory found yet. Pass a directory.")
            return 1
        
        # If the given path is not a directory
        if not os.path.isdir(args.batch):
            print("Error: Path is not a directory. Pass a directory.")
            return 1
        
        # Variables to calculate the files processed and files failed
        scan_root = args.batch
        files_processed = 0
        files_failed = 0
        
        # if --recursive flag was used
        if args.recursive:
            
            # Walk every subdirectory under the batch root
            for root, dirs, files in os.walk(scan_root):
                
                # Reading each file name of the files in the current directory
                for filename in files:
                    
                    # Creating a file path to fetch the file
                    filePath = os.path.join(root, filename)
                    
                    # Analyzing the file and getting the dictionary containing details of the file
                    report = Analyzer.analyze(ip_path=filePath)
                    
                    # If no report dictionory was created
                    if not report:
                        print(f"Warning: report could not be created for {filePath}")
                        files_failed += 1
                        continue
                    
                    # Creating a report in the specified format or default format(json)
                    final_report = make_report(
                        report = report,
                        reportFormat=format_args,
                        verbose=args.verbose
                    )
                    files_processed += 1
                    if args.verbose:
                        print(f"Saved report for {filePath}")
                   
                    # Printing the report contents
                    for k,v in final_report.items():
                        print(f'{k}:{v}')
                
        else:

            # getting a list of entries in the batch directory
            list_of_files = os.listdir(scan_root)
            
            # getting the filename of each file
            for file in list_of_files:
                
                # Creating a file path to fetch the file
                filePath = os.path.join(scan_root,file)
                
                # If the file is a directory
                if not os.path.isfile(filePath):
                    continue
                
                # Analyzing the file and getting the dictionary containing details of the file
                report = Analyzer.analyze(ip_path=filePath)
                
                # If no report dictionory was created
                if not report:
                    print(f"Error: Report could not be created for {filePath}.")
                    files_failed += 1
                    continue

                # Creating a report in the specified format or default format(json)
                final_report = make_report(
                    report=report,reportFormat=format_args,verbose=args.verbose)
                
                files_processed += 1
                
                if args.verbose:
                    print(f"Saved report for {filePath}")
                
                # Printing the report contents
                for k,v in final_report.items():
                    print(f'{k}:{v}')
        print(f"Processed {files_processed} files, {files_failed} failed")
        print('End of reports')
        return 0
    
    else:
        parser.print_help()
        return 0
    
if __name__ == "__main__":
    status_code = main()
    print(f"Program ended with the status code {status_code}")