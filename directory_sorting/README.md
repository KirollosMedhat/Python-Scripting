# Directory Sorting

Sorts every file in a given directory into subfolders based on file extension. For example, `.txt` files are moved into a `txt_files/` subfolder, `.pdf` files into a `pdf_files/` subfolder, and so on. Files with no extension are left untouched.

## Requirements

- Python installed (no external packages needed — this script only uses the standard library)

## Usage

1. **Download the script** (`directory_sorting.py`) to your machine.

2. **Navigate to the folder containing the script** using `cd`:

   ```powershell
   cd "D:\Python Scripting\directory_sorting"
   ```

3. **Identify the directory you want sorted.** For example:

   ```
   C:\Users\user\Downloads\
   ```

4. **Run the script**, passing that directory as an argument:

   ```powershell
   python directory_sorting.py "<path to the directory you want sorted>"
   ```

   Example:

   ```powershell
   python directory_sorting.py "C:\Users\user\Downloads\"
   ```

## What it does

- Scans every file directly inside the given directory (not subfolders)
- Groups files by extension (e.g. `.pdf`, `.txt`, `.py`)
- Creates a subfolder named `<extension>_files` for each extension found, if it doesn't already exist
- Moves each file into its corresponding subfolder
- Files with no extension are skipped and left in place
- Prints the total time taken to complete

## Notes

- Running the script again on an already-sorted directory is safe — it will simply find nothing left to sort at the top level.
- If the script itself is placed inside the directory being sorted, it will also sort itself into a `py_files/` folder. Run it from a separate location if you want to avoid this.