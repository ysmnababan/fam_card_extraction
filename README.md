# Family Card Data Extraction

This application uses **OCR (Optical Character Recognition)** to extract data from **Family Card PDF or image files**.
It is built with Python and packaged with tools like **PyInstaller** so it can be used by non-technical users as a standalone executable.

---

## ⭐ Features

* Extracts text data from Family Card **PDF or image files**
* Uses **OCR technology** (Google Vision API) for accurate extraction
* Converts the extracted data into **Japanese Family Card format**
* Can be packaged as a **Windows executable (.exe)** for easy use
* Saves the extracted data as an **Excel (.xlsx)** file

---

## 📌 Prerequisites

Before running or building the application, ensure you have:

### ✔ Python 3.x

### ✔ Poppler (already included in the application package)

### ✔ Google Cloud Vision API Credentials

The application requires a Google Vision API key for OCR.
Place your credentials here:

* **Windows:**
  `C:\app_credentials\secret.json`
* **Linux:**
  `~/.config/kk_scanner/secret.json`

---

## 🛠 Installation

Follow these steps if you want to run the source code:

1. **Clone the repository:**

   ```bash
   git clone git@github.com:ysmnababan/fam_card_extraction.git
   cd fam_card_extraction
   ```

2. **(Optional) Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux / macOS
   venv\Scripts\activate           # Windows
   ```

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

To run the application:

```bash
python main.py
```

Once the app is running:

1. **Open the PDF or image file** you want to extract data from
2. **Select 4 points** on the image to define the OCR extraction area
3. The application will process the text
4. **Save the result as an Excel file**

---

## 📦 Building the Executable (Windows)

You can build a `.exe` using **PyInstaller** or **auto-py-to-exe**.

### Option 1: Using auto-py-to-exe (easiest for beginners)

1. Install the tool:

   ```bash
   pip install auto-py-to-exe
   ```

2. Run it:

   ```bash
   auto-py-to-exe
   ```

3. In the GUI:

   * Select `main.py` as your script
   * Add **poppler** and **templ** folders in *Additional Files*
   * Choose:

     * **One Directory (onedir)**
     * **Console** mode
   * Click **Convert .py to .exe**

> 💡 Build the executable **on Windows** to avoid missing DLL errors.

---

### Option 2: Using PyInstaller (command line)

Example command:

```bash
pyinstaller --noconfirm --onedir --console ^
  --add-data "C:\Users\user\Documents\learning\fam_card_extraction\poppler;poppler/" ^
  --add-data "C:\Users\user\Documents\learning\fam_card_extraction\templ;templ/" ^
  C:\Users\user\Documents\learning\fam_card_extraction\main.py
```

(Use the same structure for other Windows paths.)

---
## 📷 Demo
![Demo GIF](./demo/demo.gif)

---
## 🤝 Contributing

Contributions are welcome!
Please open an issue or submit a pull request for improvements or bug fixes.