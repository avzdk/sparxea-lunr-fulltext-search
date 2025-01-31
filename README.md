# sparxea-lunr-fulltext-search
A lightweight full-text search solution for Enterprise Architect HTML exports using Lunr.js. This project indexes all EA-generated pages, enabling fast and efficient client-side search with filtering capabilities.

## **Description:**  
A lightweight full-text search solution for Enterprise Architect HTML exports using **Lunr.js**. This project indexes all EA-generated pages, enabling fast and efficient client-side search with filtering capabilities.  

## **Features**  
- 🏗 **Automatic Indexing:** Parses and indexes all HTML files under `/SparxEA_HTML_Export/EARoot`
- 🔎 **Full-text Search:** Uses **Lunr.js** for fast client-side search  
- 🎯 **Fuzzy Matching & Filtering:** Supports typo-tolerant search and category-based filtering  
- 🚀 **Global Search Bar:** Automatically inserts the search bar into every exported page  
- 🔄 **Re-run Safe:** Updates the index without duplicating search bars  

Built with **Python (BeautifulSoup, JSON)** for indexing and **JavaScript (Lunr.js)** for search functionality. 🚀

---

## **1️⃣ Installation & Setup**

### **Step 1: Clone the Repository**
```sh
git clone https://github.com/rolfmadsen/sparxea-lunr-fulltext-search.git
cd ea-search-index
```

### **Step 2: Place the Enterprise Architect HTML Export**
Ensure that your **EA HTML export folder** (e.g., `SparxEA_HTML_Export`) is placed in the same directory as `main.py`:

```
📂 ea-search-index
 ┣ 📂 SparxEA_HTML_Export
 ┃  ┣ 📂 EARoot
 ┃  ┃  ┣ 📜 index.htm
 ┃  ┃  ┣ 📜 other EA-generated files...
 ┃  ┗ 📂 images
 ┃  ┗ 📂 css
 ┣ 📜 main.py  <-- The indexing script
 ┗ 📜 README.md
```

### **Step 3: Install Dependencies**
This script requires **Python 3.x** and the following dependencies:
```sh
pip install beautifulsoup4
```

---

## **2️⃣ Running the Script**
To generate the search index and insert the search bar, run:
```sh
python main.py
```
This will:
- Traverse **all subfolders** under `SparxEA_HTML_Export/EARoot`
- Extract **titles and text content** from **valid** HTML files
- Create `search-index.js` in `SparxEA_HTML_Export/`
- Insert a **global search bar** into each page

**Re-run the script anytime** new HTML exports are added.

---

## **3️⃣ Viewing the Search in Action**
1. Open `SparxEA_HTML_Export/index.htm` in a browser  
2. Type your search term in the **Search Enterprise Architect Model** field  
3. Click **Search** or press **Enter**  
4. Results will appear with links to matching EA pages  

---

## **4️⃣ How It Works**
- **`main.py`** extracts and indexes **all relevant content**  
- The **search bar** is inserted **automatically** in each HTML page  
- **`search-index.js`** is updated each time the script runs  
- **`search.js`** enables fast search with **Lunr.js**  

---

## **5️⃣ Troubleshooting**
### **1. Search not working?**
- Ensure `search-index.js` is generated in `SparxEA_HTML_Export/`
- Open the browser console (`F12` > Console) for any errors

### **2. Multiple search bars appearing?**
- The script **removes duplicate search bars** before inserting a new one
- If duplicate search bars appear, check for manually inserted ones in `index.htm`

### **3. CORS errors when running locally?**
- If using `file://` URLs, some browsers **block local JS fetching**  
- Open the HTML export **through a local server** (e.g., Python):
  ```sh
  cd SparxEA_HTML_Export
  python -m http.server 8000
  ```
  Then open `http://localhost:8000/index.htm`

---

## **6️⃣ Future Improvements**
- ✅ Add **pagination for large results**
- ✅ Support **more metadata filtering**
- ✅ Optimize index size for **faster loading**
- ✅ Improve **UI styling** for better readability

---

## **7️⃣ License**
This project is licensed under the **[[LICENSE]]**.

---

With this setup, you can **search and navigate** through your **Enterprise Architect** models instantly. 🚀
