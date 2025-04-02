import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# College website ka URL (HTTPS)
base_url = "https://jecrcuniversity.edu.in/"  # Apne college ka URL daal yahan

# Folder jahan files save honge
output_dir = "college_files"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Supported file extensions
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
doc_extensions = ('.pdf', '.doc', '.docx', '.txt')

def download_file(url, folder):
    try:
        # HTTPS ke liye headers add kar sakte hain agar zarurat pade
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, stream=True, verify=True)  # verify=True for HTTPS
        if response.status_code == 200:
            filename = os.path.join(folder, url.split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {url} (Status: {response.status_code})")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Main scraping logic
try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(base_url, headers=headers, verify=True)  # verify=True for HTTPS
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Images scrape kar
        images = soup.find_all('img')
        for img in images:
            img_url = img.get('src')
            if img_url:
                img_url = urljoin(base_url, img_url)
                if img_url.lower().endswith(image_extensions):
                    download_file(img_url, output_dir)

        # Documents scrape kar
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                href = urljoin(base_url, href)
                if href.lower().endswith(doc_extensions):
                    download_file(href, output_dir)

    else:
        print(f"Error fetching website: Status code {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Connection error: {e}")

print("Scraping complete!")