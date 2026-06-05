# CLI File Type Detector

A simple Python command-line tool that detects file types using file signature (magic bytes) matching and saves file metadata reports.

## Features

### Currently Implemented ✅

- Detects file type by comparing file bytes against known magic signatures
- Supports 30+ file formats including `png`, `jpg`, `pdf`, `zip`, `mp3`, `mp4`, `exe`, `iso`, `rar`, and more
- Generates JSON or CSV reports with file name, size, type, and report path
- Extensible `fileSignatures.json` database with 30+ file types
- Full `argparse` CLI support with `--file`, `--batch`, `--output`, `--format`, `--recursive`, and `--verbose`
- Interactive fallback mode when no CLI arguments are provided
- Comprehensive error handling (missing files, permission errors, read failures)
- Modular signature validation and offset parsing

### Planned Features 🚀

- Batch directory scanning with aggregated reporting
- Extended metadata (creation time, modification time, file permissions, encoding detection)
- Logging and progress indicators
- Alternative features: file hashing, HTML reports, parallel processing

## Files

- `FileAnalyzer.py` - Main analyzer script with the CLI and file type detection logic
- `FileSignaturedumper.py` - Helper script to generate or update the `fileSignatures.json` database
- `fileSignatures.json` - Signature database defining supported file types, hex patterns, and offsets
- `Reports/` - Output folder for generated analysis reports
- `test1.json` - Example data file (project-specific)
- `ep.csv` - Example dataset file (project-specific)
- `plan-smartFileTypeDetector.prompt.md` - Project planning prompt

## Requirements

- Python 3.7 or newer

## Setup

1. Clone or download the repository.
2. Make sure Python is installed on your system.
3. From the project directory, run the signature dumper to generate or refresh the signature database:

```bash
python FileSignaturedumper.py
```

4. Then run the analyzer:

```bash
python FileAnalyzer.py
```

## Usage

### CLI usage

Run the analyzer directly with command-line arguments:

```bash
python FileAnalyzer.py --file "C:\path\to\example.pdf" --output Reports --format json
```

Or for CSV export:

```bash
python FileAnalyzer.py --file "C:\path\to\example.csv" --output Reports --format csv
```

For batch processing:

```bash
python FileAnalyzer.py --batch "C:\path\to\folder" --output Reports --format json --recursive
```

### Interactive fallback

If you run the script without CLI arguments, it still prompts for a file path:

```bash
python FileAnalyzer.py
```

Then enter the absolute file path and press Enter, or enter `Q` to quit.

Reports are saved in the `Reports/` folder by default, for example:

```text
Reports\example_report.json
```

## Extending the Signature Database

To add or modify supported file types, update `fileSignatures.json` with:

- `Hex`: List of magic byte patterns in hexadecimal
- `Offset`: List of offsets where the pattern may appear

You can add your own custom file signatures by creating new entries in `fileSignatures.json` using the same structure as the existing definitions.

After editing the signature database, run:

```bash
python FileSignaturedumper.py
```

This regenerates or refreshes the signature file from the source signature definitions.

## Project Status & Roadmap

Based on `plan-smartFileTypeDetector.prompt.md`:

### ✅ Phase 0: Foundation (COMPLETED)

- Core `FileTypeDetector` class with signature loading and validation
- Binary signature detection with magic bytes and offset matching
- JSON report generation to `Reports/` directory
- Error handling for file I/O and permission issues
- Interactive input loop via `getFile()` function
- Basic metadata: file name, file size, detected type

### 🔄 Phase 1: CLI Framework (COMPLETED)

- [x] Replace interactive mode with full `argparse` argument parser
- [x] Implement `--file`, `--batch`, `--output`, `--format`, `--recursive`, `--verbose` flags
- [x] Create `main()` entrypoint to route CLI args vs. interactive fallback
- [x] Graceful argument validation and help documentation

### 📋 Phase 2: Extended Metadata & Export (PLANNED)

- [ ] Enhanced metadata extraction (timestamps, permissions, encoding detection)
- [ ] CSV export support with header rows and proper formatting
- [ ] File absolute path, creation/modification times in reports

### 📦 Phase 3: Batch Processing (PLANNED)

- [ ] Directory scanning (recursive or top-level per `--recursive` flag)
- [ ] Batch report aggregation with summary statistics
- [ ] Per-file or consolidated report output
- [ ] Error resilience and processing tracking

### 🧪 Phase 4: Testing & Validation (PLANNED)

- [ ] Comprehensive test suite for single-file and batch operations
- [ ] Validation of 30+ file types across test set
- [ ] Error handling verification (permission denied, missing files, etc.)

### ⭐ Advanced Features (OPTIONAL)

- Hash generation (MD5/SHA256)
- HTML report export with styled tables
- Configuration file support (`.detector.conf`)
- Parallel processing for large batches
- Database export (SQLite)
- Archive inspection (peek inside ZIP/TAR/RAR)
- Plugin system for custom detectors

## Notes

- The script currently reads the first bytes of the file (up to 512 bytes) based on the largest required signature length
- Files are matched against 30+ known magic byte signatures with offset support
- If a file type cannot be identified, the analyzer returns `Unknown`
- CLI argument support is implemented; interactive fallback remains available when no args are passed
- All reports are saved to the `Reports/` directory by default (auto-created)
- Supports both decimal and hexadecimal offset specifications in signature definitions

## License

This project is provided as-is. Feel free to adapt and extend it for your own file detection needs.
