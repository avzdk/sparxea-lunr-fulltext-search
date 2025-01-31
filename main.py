import os
import json
from bs4 import BeautifulSoup

# Set BASE_DIR dynamically to the script's directory (No hardcoded paths)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "SparxEA_HTML_Export")  # Root folder for the report
HTML_DIR = os.path.join(BASE_DIR, "EARoot")  # HTML files inside EARoot

# Ensure the directory exists
if not os.path.exists(HTML_DIR):
    print(f"⚠️ Warning: Folder '{HTML_DIR}' not found. Exiting...")
    exit()

# Define the search bar HTML to be inserted
SEARCH_BAR_HTML = """
<div id="search-container">
    <h2><a id="index-link" href="#">Search Enterprise Architect Model</a></h2>
    <input id="search" type="text" placeholder="Search classes, attributes, descriptions...">
    <button id="searchBtn">Search</button>
    <ul id="results"></ul>
</div>
<link rel="stylesheet" href="../css/search.css">
<script>
document.addEventListener("DOMContentLoaded", function() {
    var indexLink = document.getElementById("index-link");
    var currentPath = window.location.pathname;

    // Split on 'SparxEA_HTML_Export' to determine how many levels down we are
    var pathAfterBase = currentPath.split("SparxEA_HTML_Export")[1] || "";
    var pathSegments = pathAfterBase.split("/").filter(Boolean);
    // Subtract 1 for the actual filename (e.g., EA1.htm)
    var depth = Math.max(0, pathSegments.length - 1);
    var prefix = "../".repeat(depth);

    indexLink.href = prefix + "index.htm";

    // Dynamically load Lunr.js from CDN
    var lunrScript = document.createElement("script");
    lunrScript.src = "https://unpkg.com/lunr/lunr.js"; 
    document.head.appendChild(lunrScript);

    // Dynamically load our local search.js from the export root
    var searchScript = document.createElement("script");
    searchScript.src = prefix + "search.js";
    document.head.appendChild(searchScript);
});
</script>
"""

index = []
id_counter = 1
ignored_files = {"blank.htm", "toc.htm", "index.htm"}  # Ignore placeholders

# Recursively scan subdirectories
for root, _, files in os.walk(HTML_DIR):
    for filename in files:
        if filename.endswith(".htm") or filename.endswith(".html"):
            if filename in ignored_files:
                print(f"⚠️ Skipping placeholder file: {filename}")
                continue  # Skip unwanted files

            filepath = os.path.join(root, filename)
            print(f"🔍 Processing: {filepath}")  # Debugging output

            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            # Extract title
            title = soup.title.string.strip() if soup.title else filename

            # Skip if title contains a placeholder
            if "#TITLE#" in title:
                print(f"⚠️ Skipping file with placeholder title: {filename}")
                continue

            # Extract meaningful content
            content_blocks = soup.find_all(["div", "td", "th", "p", "li"])
            content = ' '.join([el.get_text(" ", strip=True) for el in content_blocks]).strip()

            # Remove known placeholders
            if "#CONTENT#" in content or "#BREAD_CRUMB#" in content:
                print(f"⚠️ Skipping file with placeholder content: {filename}")
                continue

            # Remove excess whitespace
            content = " ".join(content.split())

            # Determine element type based on filename
            element_type = "Unknown"
            if "class" in filename.lower():
                element_type = "Class"
            elif "attribute" in filename.lower():
                element_type = "Attribute"
            elif "diagram" in filename.lower():
                element_type = "Diagram"

            # Convert path to relative (from SparxEA_HTML_Export root)
            relative_url = os.path.relpath(filepath, BASE_DIR).replace("\\", "/")

            # Add to search index
            index.append({
                "id": str(id_counter),
                "title": title,
                "content": content,
                "url": relative_url,
                "type": element_type
            })
            id_counter += 1

            # Insert search bar at the top of the <body>
            body = soup.body
            if body:
                # Remove existing search bar if it already exists
                existing_search_bar = body.find(id="search-container")
                if existing_search_bar:
                    existing_search_bar.decompose()

                # Insert the search bar at the beginning of the body
                body.insert(0, BeautifulSoup(SEARCH_BAR_HTML, "html.parser"))

                # Write the modified HTML back to the file
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(str(soup))

# Save search index as a global variable in the root
js_index_path = os.path.join(BASE_DIR, "search-index.js")
with open(js_index_path, "w", encoding="utf-8") as f:
    f.write("var searchData = " + json.dumps(index, indent=2, ensure_ascii=False) + ";\n")

print(f"✅ Full-text search index generated successfully at {js_index_path}")
print(f"✅ Search bar injected into all pages in {HTML_DIR}")

# Write the search.js file to enable search functionality
js_search_path = os.path.join(BASE_DIR, "search.js")
SEARCH_JS_CONTENT = """ 
document.addEventListener("DOMContentLoaded", function () {
    // Only build the index once lunr.js has loaded
    if (typeof lunr === "undefined") {
        console.error("❌ Lunr library not found. Make sure you're online or check lunrScript.src.");
        return;
    }

    // Check if global searchData is loaded from search-index.js
    if (typeof searchData === "undefined") {
        console.error("❌ searchData is not defined. Check search-index.js.");
        return;
    }

    console.log("✅ Loaded search data:", searchData);

    // Build Lunr index
    const idx = lunr(function () {
        this.ref("id");
        this.field("title", { boost: 10 });
        this.field("content");

        searchData.forEach(doc => this.add(doc));
    });

    const searchInput = document.getElementById("search");
    const searchBtn = document.getElementById("searchBtn");
    const resultsContainer = document.getElementById("results");

    function performSearch() {
        const query = searchInput.value.trim();
        if (query.length < 2) {
            resultsContainer.innerHTML = "<li>Type at least 2 characters...</li>";
            return;
        }

        // Lunr fuzzy search
        const results = idx.search(`${query}~1`);
        displayResults(results, query);
    }

    function displayResults(results, query) {
        resultsContainer.innerHTML = "";
        results.forEach(r => {
            const item = searchData.find(d => d.id === r.ref);
            if (item) {
                const highlightedTitle = highlight(item.title, query);
                resultsContainer.innerHTML += `
                    <li><a href="${item.url}">${highlightedTitle} (${item.type})</a></li>
                `;
            }
        });
        if (!resultsContainer.innerHTML) {
            resultsContainer.innerHTML = "<li>No results found.</li>";
        }
    }

    function highlight(text, query) {
        const regex = new RegExp("(" + query + ")", "gi");
        return text.replace(regex, "<mark>$1</mark>");
    }

    // Enter key triggers search
    searchInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            performSearch();
        }
    });

    // Click button triggers search
    searchBtn.addEventListener("click", performSearch);
});
"""

with open(js_search_path, "w", encoding="utf-8") as f:
    f.write(SEARCH_JS_CONTENT)

print(f"✅ search.js file added at {js_search_path}")
