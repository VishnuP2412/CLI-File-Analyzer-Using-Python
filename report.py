import os
import json, csv


def make_report(report, reportFormat, verbose):
    output_dir = report.get('Path', report.get('Report Path', 'Reports'))
    os.makedirs(output_dir, exist_ok=True)
    
    # If the report format is json
    if reportFormat == 'json':
        if verbose:
            print(f"Saving report to: {output_dir} as JSON format...")
        report_path = os.path.join(output_dir, report['File Name'] + '_report.json')
        with open(report_path, 'w') as report_file:
            json.dump(report, report_file, indent=4)
    
    # If the report format is csv
    elif reportFormat == 'csv':
        if verbose:
            print(f"Saving report to: {output_dir} as CSV format...")
        report_path = os.path.join(output_dir, report['File Name'] + '_report.csv')
        with open(report_path, 'w', newline='') as report_file:
            fieldnames = list(report.keys())
            writer = csv.DictWriter(report_file, fieldnames=fieldnames)
            writer.writeheader()
            row = {
                key: json.dumps(value) if isinstance(value, (dict, list)) else value
                for key, value in report.items()
            }
            writer.writerow(row)
    else:
        raise ValueError(f"Unsupported format: {reportFormat}")
    if verbose:
        print(f"Report saved to: {report_path}")
    report['report_path'] = report_path
    return report