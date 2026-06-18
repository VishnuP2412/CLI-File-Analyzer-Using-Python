## Smart File Type Detector + Metadata Analyzer - Project Plan

**TL;DR:** Enhance `FileAnalyzer.py` into a production-grade CLI tool with argparse support, advanced metadata extraction, multi-format export (JSON/CSV), batch processing, and extensible file type detection for 15+ file types.

---

## 🎯 TO-DO (Priority Implementation)

### Phase 1: CLI Framework (REQUIRED)

- [x] **Integrate argparse** - Replace comments with full CLI argument parser
  - `--file <path>` : Single file analysis
  - `--batch <directory>` : Batch directory scanning
  - `--output <path>` : Custom output location (default: `Reports/`)
  - `--format {json,csv}` : Export format selection
  - `--recursive` : Enable recursive directory scanning
  - `--verbose` : Detailed output logging
- [x] **Create main() entrypoint** - Refactor getFile() flow into CLI-driven execution
  - Parse command-line arguments
  - Route to single-file or batch analysis
  - Handle missing arguments gracefully

### Phase 2: Extended Metadata & Export (CORE)

- [x] **Enhance metadata extraction** - Add comprehensive file information:
  - Absolute file path
  - Creation time (os.stat().st_ctime)
  - Modification time (os.stat().st_mtime)
  - File mode/permissions (os.stat().st_mode)
  - File encoding detection (for text files)
- [x] **CSV export support** - Implement structured CSV writer
  - Header row with all metadata fields
  - Per-file rows for batch results
  - Proper escaping and formatting

### Phase 3: Batch Processing (CORE)

- [ ] **Directory scanning** - Implement batch analysis:
  - Iterate through directory (recursive or top-level per flag)
  - Process each file with error resilience
  - Aggregate results into single or per-file reports
- [ ] **Batch report aggregation** - Generate combined reports:
  - Summary statistics (total files, detected types, errors)
  - Per-file details in structured format
  - Processing time tracking

### Phase 4: Testing & Validation

- [ ] Test single-file JSON export: `python FileAnalyzer.py --file sample.pdf --format json --output test.json`
- [ ] Test single-file CSV export: `python FileAnalyzer.py --file sample.png --format csv --output test.csv`
- [ ] Test batch processing: `python FileAnalyzer.py --batch ./test-folder --format json --output batch-report.json`
- [ ] Test recursive scanning: `python FileAnalyzer.py --batch ./test-folder --recursive --format json`
- [ ] Verify at least 15 file types detected correctly across test set
- [ ] Validate error handling for permission denied, unreadable files, and missing directories

---

## 💡 RECOMMENDED (Enhance Quality & Usability)

- [ ] **Progress indicator** - Add tqdm or simple counter for batch processing feedback
- [ ] **Logging module** - Track processing history, timestamps, and errors to `.log` files
- [ ] **File type categorization** - Group results by type (Documents, Images, Archives, etc.)
- [ ] **Help documentation** - Add comprehensive `--help` output with usage examples
- [ ] **Verbose mode output** - Print detailed detection steps when `--verbose` enabled
- [ ] **Input validation** - Robust CLI argument checking with user-friendly error messages
- [ ] **Performance metrics** - Report processing time and files-per-second rate in batch mode

---

## ⭐ OPTIONAL / RESUME-WORTHY FEATURES

These add professional polish and demonstrate advanced skills:

1. **Hash Generation** - Compute MD5/SHA256 for each file (data integrity verification)
2. **HTML Report Export** - Generate formatted HTML reports with styled tables and charts
3. **Configuration File Support** - Allow `.detector.conf` YAML/JSON for default CLI settings
4. **Parallel Processing** - Use `multiprocessing` or `concurrent.futures` for large batch jobs
5. **Statistics Dashboard** - Summary of file type distribution, size ranges, and common types
6. **Extensible Plugin System** - Allow custom file type detectors via plugin architecture
7. **Database Export** - Write results to SQLite for querying and historical tracking
8. **Real-time Streaming** - Read from stdin for pipeline integration (e.g., `find . -type f | python FileAnalyzer.py --stream`)
9. **Dry-run Mode** - Preview analysis without writing reports (useful for validation)
10. **Archive Inspection** - Peek inside ZIP/TAR/RAR to detect contained file types
11. **MIME Type Validation** - Cross-reference detected type with system MIME database
12. **Fingerprinting Mode** - Generate file signatures for unknown types (auto-learning)

---

## ✅ COMPLETED

These features are already implemented across the CLI modules (`cli.py`, `detector.py`, `report.py`, `utils.py`):

1. **Core FileTypeDetector Class** - Holds signature definitions, detection logic, and extraction helpers
2. **Binary Signature Detection** - Reads first 512 bytes and matches against magic-byte signatures
3. **Magic Byte Loading** - Loads and validates file signatures from `fileSignatures.json`
4. **Extended Metadata Extraction** - Collects file name, file size, detected file type, encoding, timestamps, permissions, and absolute path
5. **JSON Report Generation** - Writes structured reports to `Reports/` directory with auto-creation
6. **CSV Report Generation** - Writes row-based CSV reports with header row and serialized nested values
7. **Error Handling** - Gracefully handles missing files, permission errors, and read failures
8. **CLI Framework** - Supports `--file`, `--batch`, `--output`, `--format`, `--recursive`, and `--verbose`

---

## 🔧 TECHNICAL DECISIONS

### Current Architecture

- **File**: `FileAnalyzer.py` (CLI-enabled with interactive fallback)
- **Signatures**: `fileSignatures.json` (15+ magic-byte definitions)
- **Output**: `Reports/` directory (auto-created by default)
- **Read Strategy**: First 512 bytes (magic bytes + offset matching)
- **Detection Fallback**: "Unknown" when no signature matches

### Key Design Choices

✅ **Binary magic-byte detection** over extension-based (more reliable)  
✅ **Default output to `Reports/`** with explicit override support  
✅ **Separate JSON/CSV exporters** for modularity  
✅ **Error resilience** in batch mode (continue on error, log failures)  
✅ **Interactive mode as fallback** when no CLI args provided

---

## 📋 FURTHER CONSIDERATIONS

1. **Recursive Scanning Default** - Should `--batch` scan recursively by default or require `--recursive`?
   - _Recommendation_: Require `--recursive` explicitly (safer for large directories)

2. **Batch Report Format** - Single consolidated report or individual per-file reports?
   - _Recommendation_: Consolidated JSON/CSV with optional `--per-file` flag for individual exports

3. **Interactive Fallback** - Preserve getFile() as fallback when no arguments provided?
   - _Recommendation_: Yes, for backward compatibility and user-friendliness

4. **File Size Limits** - Process all files or set a max size to avoid memory issues?
   - _Recommendation_: Add optional `--max-size` flag (default: unlimited for metadata, 10MB for content)

5. **Timestamp Format** - ISO 8601 or Unix epoch?
   - _Recommendation_: ISO 8601 for readability in reports

---

## 📊 RESUME HIGHLIGHTS

This project demonstrates:

- **CLI Development**: argparse, argument validation, help documentation
- **File I/O & Binary Processing**: Magic byte detection, hex parsing, offset handling
- **Data Structures**: JSON/CSV generation, report aggregation, error tracking
- **System Programming**: os.stat(), file permissions, batch directory operations
- **Error Handling**: Graceful degradation, user-friendly error messages, logging
- **Code Quality**: Modular design, extensibility, clear separation of concerns
- **Testing & Validation**: Multi-format output validation, edge case handling

---

## 📝 RELEVANT FILES

- `FileAnalyzer.py` — Main implementation (to be enhanced with argparse)
- `FileSignatureDumper.py` — Utility for generating `fileSignatures.json` from known file samples
- `fileSignatures.json` — Magic byte definitions (15+ file types)
- `reports/` — Output directory for generated reports
