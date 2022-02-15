from bs4 import BeautifulSoup

file_location = input("File location? ")
with open(file_location, encoding="utf-8") as o:
    document = o.read()
soup = BeautifulSoup(document, "html.parser")
output = soup.prettify()

file_name = file_location.split(".")[-1]
file_ext = file_location.split(".")[1]
with open(file_location,'w', encoding="utf-8") as f:
    f.write(output)
    f.close()

