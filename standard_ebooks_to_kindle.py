import os
import requests

# --- STEP 1: GENERATE THE EXACT SERVER URL ---
def generate_download_url(author, title):
    # Standard Ebooks formats all URLs to lowercase, with dashes, removing punctuation
    def clean_string(text):
        text = text.lower()
        text = text.replace("'", "").replace("’", "").replace(",", "")
        text = text.replace(" ", "-")
        return text

    clean_author = clean_string(author)
    clean_title = clean_string(title)
    
    # Matches the exact standard distribution layout
    url = f"https://standardebooks.org/ebooks/{clean_author}/{clean_title}/downloads/{clean_author}_{clean_title}.epub"
    return url


# --- STEP 2: DOWNLOAD THE FILE DIRECTLY ---
def download_file(url, folder_name, filename):
    # 1. Create the subfolder automatically if it doesn't exist yet
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"📁 Created a new subfolder: /{folder_name}")

    # 2. Combine the folder and filename (e.g., "downloads/thomas-hardy_a-pair-of-blue-eyes.epub")
    full_destination_path = os.path.join(folder_name, filename)

    print(f"🔍 Target URL: {url}")
    print(f"⏳ Downloading into folder: '{full_destination_path}'...")
    try:
        response = requests.get(url, stream=True)
        
        # If they don't have this book/author combination, stop here
        if response.status_code == 404:
            print("❌ Error 404: Could not find that book on Standard Ebooks. Check your spelling!")
            return False
            
        # Save the file completely unmodified into the subfolder
        with open(full_destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print("💾 Success! File downloaded completely unmodified.")
        return True
    except Exception as e:
        print(f"❌ Failed to download file: {e}")
        return False


# --- STEP 3: THE MAIN BRAIN ---
def main():
    # -------------------------------------------------------------
    # JUST CHANGE THESE TWO LINES FOR ANY BOOK YOU WANT TO GRAB:
    BOOK_AUTHOR = "Thomas Hardy"
    BOOK_TITLE = "A Pair of Blue Eyes"
    
    # NAME YOUR SUBFOLDER HERE (Change "downloads" to whatever you want)
    SUBFOLDER_NAME = "downloads"
    # -------------------------------------------------------------
    
    # Generate the direct link
    download_url = generate_download_url(BOOK_AUTHOR, BOOK_TITLE)
    
    # Extract the exact, official filename from the end of the web link
    filename = download_url.split("/")[-1]
    
    # Execute the download pipeline targeting the subfolder
    if download_file(download_url, SUBFOLDER_NAME, filename):
        print(f"📂 Saved cleanly inside your '{SUBFOLDER_NAME}' folder!")
        print("🚀 Opening your subfolder now so you can drop it into amazon.com/sendtokindle")
        
        # Automatically pops open the exact subfolder so you can grab the file instantly
        try:
            target_folder_path = os.path.join(os.getcwd(), SUBFOLDER_NAME)
            os.startfile(target_folder_path)
        except Exception:
            pass

if __name__ == "__main__":
    main()