# SparxEA LunrJS Full-text Search

A lightweight full-text search solution for **Enterprise Architect** HTML exports using **Lunr.js**. This project indexes all `.htm` pages in the **SparxEA_HTML_Export/EARoot** folder (and its subfolders) and automatically inserts a search bar into each page, including the index.htm page, enabling fast and efficient client-side search.

## **Description**
- Parses and indexes **all** `.htm` files (except ignored ones like `index.htm`, `blank.htm`, and `toc.htm`) under **SparxEA_HTML_Export**.
- Uses **BeautifulSoup** (Python) to extract text and titles, then **Lunr.js** (JavaScript) for fast client-side search.
- Automatically inserts a small search bar and two JavaScript references (`searchIndex.js` and `searchLogic.js`) into each `.htm` file.

## **Features**
- **Automatic Indexing**: Uses Python to walk all subfolders of `SparxEA_HTML_Export`  
- **Full-text Search**: Powered by Lunr.js in the browser
  - **Partial Matches**: Append wildcards to search terms
  - **Pre-built Index**: Optionally generate a serialized Lunr index to avoid the browser “blink”
- **On-the-fly Injection**: Adds the search bar to each `.htm` so you can search from anywhere  
- **Re-run Safe**: Skips adding a second bar if one is already present

## **Folder & File Overview**

After running `main.py`, you’ll see a structure like this:

```
SparxEA_HTML_Export
 ┣ EARoot
 ┃  ┣ EA1
 ┃  ┃  ┣ EA1.htm
 ┃  ┃  ┣ ...
 ┃  ┣ EA2
 ┃  ┃  ┣ EA42.htm
 ┃  ┃  ┣ ...
 ┃  ┣ ...
 ┣ css
 ┣ images
 ┣ js
 ┃  ┣ searchIndex.js   <-- Autogenerated Lunr index
 ┃  ┣ searchLogic.js   <-- JS logic for handling searches
 ┗ index.htm           <-- Main page where search bar is also injected

main.py  <-- The Python indexing + injection script
README.md
```

## **1️⃣ Installation & Setup**

### **1. Clone or Download**  
Place the **main.py** file in the same folder as your exported HTML site folder:

```
my_project/
 ┣ SparxEA_HTML_Export/
 ┃   ┣ EARoot/
 ┃   ┗ ...
 ┣ main.py
 ┗ README.md
```

### **2. Install Dependencies**

Ensure you have **Python 3.x** and run:
```bash
pip install beautifulsoup4
```

## **2️⃣ Usage**

From the folder containing `main.py` and `SparxEA_HTML_Export`, run:

```bash
python main.py
```

This will:
- Collect `.htm` files under **SparxEA_HTML_Export/EARoot** (excluding some by name)
- Parse each file to extract the `<title>` and body text
- Create a `js/searchIndex.js` and a `js/searchLogic.js` in **SparxEA_HTML_Export/js**
- Insert `<script>` references and a `<div id="lunrSearchBar">` near `<body>` in every `.htm`

## **3️⃣ Viewing the Result**

Run a Python server:
```bash
python -m http.server
```
Open `[SparxEA_HTML_Export/index.htm](http://localhost:8000/SparxEA_HTML_Export/)` in a browser:

1. Look for the **search bar** that was inserted at the top.  
2. Type your query to see matching results dynamically displayed.
3. Using your mouse click a result or navigate to the result using TAB select it using ENTER keys
4. Clicking a result link navigates to that `.htm` page (using correct relative paths).

### Clearing the Search
When you clear the search field (delete all text), no results are displayed—preventing a huge listing of all pages.

## **4️⃣ How It Works**

1. **Gather Documents**  
   - `main.py` reads every `.htm` under `SparxEA_HTML_Export`.
   - Uses **BeautifulSoup** to extract text and `<title>`.

2. **Generate Index**  
   - It writes a `searchIndex.js` containing a Lunr index of all pages’ text.  
   - Also writes `searchLogic.js` to handle search calls.

3. **Inject Bar**  
   - Modifies each `.htm` to include:
     1. References to Lunr.js CDN, `searchIndex.js`, and `searchLogic.js`.
     2. A `<div id="lunrSearchBar">` with an `<input>` for on-page searching.

## **6️⃣ Future Enhancements**

- **Fuzzy** or partial matching out of the box (requires user to type `term~1`)  
- **Metadata** or category-based filtering  
- **Styling** improvements for the search results

---

With this setup, you get a **client-side** full-text search for your **Sparx EA** HTML exports using LunrJS. Enjoy!
