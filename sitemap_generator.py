import os
import requests
from bs4 import BeautifulSoup
from xml.dom.minidom import Document
from datetime import datetime
from urllib.parse import urlparse, urljoin
from fake_useragent import UserAgent  

# Initialize a UserAgent object to generate random User-Agent headers
user_agent = UserAgent()

def get_links(url):
    try:
        # Generate a random User-Agent header
        headers = {'User-Agent': user_agent.random}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            return links
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def create_custom_xml_sitemap(domain, folder="sitemaps"):
    full_url = f"https://{domain}"
    links = get_links(full_url)
    current_datetime = datetime.utcnow().isoformat() + '+00:00'

    # Create the sitemaps folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = os.path.join(folder, f"{domain}.xml")

    doc = Document()
    urlset = doc.createElement("urlset")
    urlset.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    urlset.setAttribute("xsi:schemaLocation", "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")
    doc.appendChild(urlset)

    domain_url_element = doc.createElement("url")
    domain_loc_element = doc.createElement("loc")
    domain_loc_element.appendChild(doc.createTextNode(full_url))
    domain_url_element.appendChild(domain_loc_element)
    domain_lastmod_element = doc.createElement("lastmod")
    domain_lastmod_element.appendChild(doc.createTextNode(current_datetime))
    domain_url_element.appendChild(domain_lastmod_element)
    domain_priority_element = doc.createElement("priority")
    domain_priority_element.appendChild(doc.createTextNode("0.5"))
    domain_url_element.appendChild(domain_priority_element)
    urlset.appendChild(domain_url_element)

    for link in links:
        url_element = doc.createElement("url")
        loc_element = doc.createElement("loc")
        full_link = urljoin(full_url, link)
        loc_element.appendChild(doc.createTextNode(full_link))
        url_element.appendChild(loc_element)
        lastmod_element = doc.createElement("lastmod")
        lastmod_element.appendChild(doc.createTextNode(current_datetime))
        url_element.appendChild(lastmod_element)
        priority_element = doc.createElement("priority")
        priority_element.appendChild(doc.createTextNode("0.8"))
        url_element.appendChild(priority_element)
        urlset.appendChild(url_element)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(doc.toprettyxml(indent="  "))

    print(f"Sitemap for {domain} has been saved to {filename}")

if __name__ == '__main__':
    domain = input("Enter the domain name to create a formatted XML sitemap (e.g., example.com): ")
    create_custom_xml_sitemap(domain)
