# Use 'requests' to download the page from the URL appearing in column 1 of the row
r = requests.get(row[0])
# Read the contents of the HTML page and store them inside of the variable 'soup'
soup = BeautifulSoup(r.text, "lxml")