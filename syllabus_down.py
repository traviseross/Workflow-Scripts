from pathlib import Path
import re
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

exts = ["htm", "html", "pdf", "cfm", "docx", "doc", "rtf", "xml"]
r = requests.get("https://thebhc.org/syllabi")
soup = bs(r.content, "html.parser")
table_soup = soup.find("table", {"class": "table table-hover table-striped"})
rows = table_soup.find_all("tr")
for r in rows:
    cells = r.find_all("td")
    cells = [c.text for c in cells]
    try:
        title = cells[0].strip()
        try:
            title = title.split("(")[0].strip()
        except IndexError:
            title = title.strip()
    except IndexError:
        year = ""
        title = "error on title"
    try:
        auth = cells[1]
        auth_name = auth.split(", ")[0].strip()
        institution = auth.split(", ")[-1].strip()
    except IndexError:
        auth_name = "error on author"
        institution = "error on author"
    link = r.find("a", href=True)
    if link is None:
        continue
    url = link["href"]
    ext = url.split(".")[-1]
    auth_name = re.sub(r"[\t\n\/\:]", " ", auth_name)
    auth_name = re.sub(r"[\s+]", " ", auth_name)
    institution = re.sub(r"[\t\n\/\:]", " ", institution)
    institution = re.sub(r"[\s+]", " ", institution)
    title = re.sub(r"[\t\n\/\:]", " ", title)
    title = re.sub(r"[\s+]", " ", title)
    if ext in exts:
        filename = f"/Users/travisross/Downloads/Syllabi/{auth_name} - {title} - {institution}.{ext}"
    else:
        filename = (
            f"/Users/travisross/Downloads/Syllabi/{auth_name} - {title} - {institution}"
        )
    filename = Path(filename)
    response = requests.get(url)
    filename.write_bytes(response.content)
