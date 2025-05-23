import threading
import time
import urllib.request
import os

class DownloadThread(threading.Thread):
    def __init__(self, url, filename):
        super().__init__()
        self.url = url
        self.filename = filename
        
    def run(self):
        print(f"Starting download of {self.url}")
        start_time = time.time()
        try:
            urllib.request.urlretrieve(self.url, self.filename)
            duration = time.time() - start_time
            print(f"Downloaded {self.filename} in {duration:.2f} seconds")
        except Exception as e:
            print(f"Error downloading {self.url}: {e}")

def download_files_concurrently(url_list):
    threads = []
    
    # Create directory for downloads if it doesn't exist
    os.makedirs("downloads", exist_ok=True)
    
    # Create and start a thread for each URL
    for i, url in enumerate(url_list):
        filename = f"downloads/file_{i+1}.txt"
        thread = DownloadThread(url, filename)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print("All downloads completed!")

if __name__ == "__main__":
    # Sample URLs to download (these are public text files)
    urls = [
        "https://www.gutenberg.org/files/1342/1342-0.txt",  # Pride and Prejudice
        "https://www.gutenberg.org/files/2701/2701-0.txt",  # Moby Dick
        "https://www.gutenberg.org/files/84/84-0.txt",      # Frankenstein
        "https://www.gutenberg.org/files/1661/1661-0.txt",  # The Adventures of Sherlock Holmes
        "https://www.gutenberg.org/files/11/11-0.txt"       # Alice's Adventures in Wonderland
    ]
    
    download_files_concurrently(urls)