import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

st.set_page_config(page_title="Auto Downloader", layout="centered")

st.title("📥 Auto File Downloader")


URL = "https://github.com/kavya200205/LMS"   

st.write(f"Using predefined URL: {URL}")


destination = st.text_input("Enter destination folder path")

if st.button("Download Files"):

    if not destination:
        st.error("Please enter a destination folder.")
    else:
        try:
           
            os.makedirs(destination, exist_ok=True)

            
            response = requests.get(URL)
            soup = BeautifulSoup(response.text, "html.parser")

           
            links = soup.find_all("a")

            file_links = []

            
            for link in links:
                href = link.get("href")

                if href and href.lower().endswith((".txt", ".img",".tgz",".py",".ipynb",".pdf")):
                    full_url = urljoin(URL, href)
                    file_links.append(full_url)

            if not file_links:
                st.warning("No .txt or .img files found.")
            else:
                st.success(f"Found {len(file_links)} files. Downloading...")

                for file_url in file_links:
                    file_name = os.path.join(destination, file_url.split("/")[-1])

                    # Download file
                    with requests.get(file_url, stream=True) as r:
                        with open(file_name, "wb") as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)

                    st.write(f"✅ Downloaded: {file_name}")

                st.success("🎉 All files downloaded successfully!")

        except Exception as e:
            st.error(f"Error: {e}")