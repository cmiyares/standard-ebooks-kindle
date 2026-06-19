import os
import requests
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading

# --- STEP 1: GENERATE THE EXACT SERVER URL ---
def generate_download_url(author, title):
    def clean_string(text):
        text = text.lower()
        text = text.replace("'", "").replace("’", "").replace(",", "")
        text = text.replace(" ", "-").strip()
        return text

    clean_author = clean_string(author)
    clean_title = clean_string(title)
    
    return f"https://standardebooks.org/ebooks/{clean_author}/{clean_title}/downloads/{clean_author}_{clean_title}.epub"


# --- STEP 2: THE DOWNLOAD PIPELINE (ADAPTED FOR GUI) ---
def download_book_pipeline(author, title, log_widget, download_button):
    # Disable button during download so user doesn't double-click
    download_button.config(state=tk.DISABLED)
    
    if not author.strip() or not title.strip():
        log_widget.insert(tk.END, "❌ Error: Both Author and Title fields must be filled out!\n\n")
        download_button.config(state=tk.NORMAL)
        return

    SUBFOLDER_NAME = "downloads"
    download_url = generate_download_url(author, title)
    filename = download_url.split("/")[-1]
    full_destination_path = os.path.join(SUBFOLDER_NAME, filename)

    log_widget.insert(tk.END, f"🔍 Target URL: {download_url}\n")
    log_widget.insert(tk.END, f"⏳ Connecting to Standard Ebooks...\n")
    log_widget.see(tk.END)

    try:
        if not os.path.exists(SUBFOLDER_NAME):
            os.makedirs(SUBFOLDER_NAME)

        response = requests.get(download_url, stream=True)
        
        if response.status_code == 404:
            log_widget.insert(tk.END, "❌ Error 404: Book not found. Please verify spelling and punctuation!\n\n")
            download_button.config(state=tk.NORMAL)
            return
            
        with open(full_destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        log_widget.insert(tk.END, f"💾 Success! Saved to /{SUBFOLDER_NAME}/{filename}\n")
        log_widget.insert(tk.END, "🚀 Opening folder for Send-to-Kindle drag & drop...\n\n")
        log_widget.see(tk.END)
        
        # Open the Windows directory automatically
        try:
            os.startfile(os.path.join(os.getcwd(), SUBFOLDER_NAME))
        except Exception:
            pass

    except Exception as e:
        log_widget.insert(tk.END, f"❌ Network Error: {e}\n\n")
    
    # Re-enable the button for the next book
    download_button.config(state=tk.NORMAL)
    log_widget.see(tk.END)


# --- STEP 3: THREADING ENGINE ---
def start_download_thread(author_entry, title_entry, log_widget, download_button):
    author = author_entry.get()
    title = title_entry.get()
    
    threading.Thread(
        target=download_book_pipeline, 
        args=(author, title, log_widget, download_button), 
        daemon=True
    ).start()


# --- STEP 4: INTERFACE LAYOUT AND DESIGN ---
def build_gui():
    root = tk.Tk()
    root.title("Standard Ebooks Downloader")
    root.geometry("500x450")
    root.resizable(False, False)
    
    # Apply a clean styling layout
    style = ttk.Style()
    style.theme_use('vista' if 'vista' in style.theme_names() else 'default')

    # Main structural wrapper frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Application Header
    title_label = ttk.Label(main_frame, text="📖 Standard Ebooks Downloader", font=("Segoe UI", 16, "bold"))
    title_label.pack(pady=(0, 15))

    # Input Elements Frame
    input_frame = ttk.LabelFrame(main_frame, text=" Book Details ", padding="15")
    input_frame.pack(fill=tk.X, pady=(0, 15))

    # Author Input
    ttk.Label(input_frame, text="Author Name:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
    author_entry = ttk.Entry(input_frame, font=("Segoe UI", 10), width=40)
    author_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
    author_entry.insert(0, "Thomas Hardy")

    # Title Input
    ttk.Label(input_frame, text="Book Title:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
    title_entry = ttk.Entry(input_frame, font=("Segoe UI", 10), width=40)
    title_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
    title_entry.insert(0, "A Pair of Blue Eyes")

    # Large Action Button
    download_button = ttk.Button(
        main_frame, 
        text="Download eBook", 
        command=lambda: start_download_thread(author_entry, title_entry, log_box, download_button)
    )
    download_button.pack(fill=tk.X, pady=(0, 15))

    # Live Status Activity Log Window (FIXED: Changed "dashed" to "bold")
    log_label = ttk.Label(main_frame, text="Activity Log:", font=("Segoe UI", 10, "bold"))
    log_label.pack(anchor=tk.W)
    
    log_box = scrolledtext.ScrolledText(main_frame, height=10, font=("Consolas", 9), bg="#f8f9fa", fg="#333333")
    log_box.pack(fill=tk.BOTH, expand=True)
    log_box.insert(tk.END, "Ready to pull classic literature down to your machine.\n\n")

    # Start the continuous loop to render the dashboard layout
    root.mainloop()

if __name__ == "__main__":
    build_gui()