from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

KEYWORDS = ["modernisation", "renovation", "cash buyer", "refurbishment",
            "investment opportunity", "doer upper", "project", "needs work",
            "auction", "blank canvas"]

@app.route("/", methods=["GET", "POST"])
def index():
    listings = []
    if request.method == "POST":
        url = request.form.get("url")
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for c in soup.select(".propertyCard"):
            t = c.select_one(".propertyCard-title")
            p = c.select_one(".propertyCard-priceValue")
            lnk = c.select_one("a.propertyCard-link")
            desc = c.select_one(".propertyCard-description")
            if t and p and lnk:
                title = t.text.strip()
                price = p.text.strip()
                link = "https://www.rightmove.co.uk" + lnk["href"]
                description = desc.text.strip() if desc else ""
                tags = [kw for kw in KEYWORDS if kw in description.lower()]
                listings.append({
                    "title": title, "price": price,
                    "description": description, "link": link,
                    "tags": ", ".join(tags) if tags else "Standard"
                })
    return render_template("index.html", listings=listings)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
