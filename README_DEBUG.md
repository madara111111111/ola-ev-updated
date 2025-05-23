# Why am I seeing two `codespaces-flask-main` folders?

This usually happens because:
- One folder is named with a dash (`codespaces-flask-main`) and the other with an underscore (`codespaces_flask_main`).
- You may have copied, renamed, or extracted the project in a way that created both versions.
- Python treats `-` and `_` differently in imports: only `_` is valid in module names.

## What should you do?

- **Keep only one folder** for your main app package.
- If your imports use `codespaces_flask_main`, delete or move the `codespaces-flask-main` folder.
- If your imports use `codespaces-flask-main`, rename it to `codespaces_flask_main` (replace `-` with `_`).

## How to fix

1. Decide on a single folder name: `codespaces_flask_main` (recommended).
2. Move all your code (routes, models, templates, etc.) into that folder.
3. Update your imports everywhere to use `codespaces_flask_main`.
4. Delete the other folder to avoid confusion.

**Summary:**  
- Only one app package folder should exist.
- Use underscores (`_`) in Python package/folder names, not dashes (`-`).

## Why are template files being corrupted?

- If you open/save HTML files in a non-text editor (like Word or a hex editor), they may be saved as binary or in a non-UTF-8 encoding.
- Downloading or copying files from email, WhatsApp, or some cloud services can corrupt encoding.
- Accidentally saving a file as a Word doc, PDF, or with the wrong extension can cause corruption.
- Using "Save As" in some editors with the wrong encoding (e.g., UTF-16, ANSI) instead of UTF-8.
- Copy-pasting from web pages or PDFs can introduce hidden/binary characters.

**How to avoid corruption:**
- Always use a code/text editor (VS Code, Sublime, Notepad++).
- Save files as UTF-8 plain text.
- Avoid editing code files in Word, Excel, or similar apps.
- If you see gibberish or errors, delete and recreate the file as plain text.
