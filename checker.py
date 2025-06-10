import difflib 
import asyncio
import subprocess
import tkinter as tk
from tkinter import *
from deep_translator import GoogleTranslator
import scraper
import json

BG_COLOR = "white"
BTN_COLOR = "#6A0DAD"  
TEXT_COLOR = "black" 
TEXT_BG = "#F5F5F5"  

def translate_to_tr(text):
    try:
        return GoogleTranslator(source='en', target='tr').translate(text)
    except:
        return text
    
async def get_all_package_names():
    try:
        with open("fast_pypi_summary.json","r",encoding="utf-8") as f:
            return list(json.load(f))
    except:
        return []

async def user_interface():
    global text, root, result_label
    
    root = Tk()
    root.title("Python Library Auto Installer")
    root.geometry("800x600")
    root.configure(bg=BG_COLOR)
    
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    label = tk.Label(root, text="Please enter a library name:", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
    label.grid(row=0, column=0)

    text = tk.Text(root, height=2, width=50, font=("Arial", 12), bg=TEXT_BG, fg="black", highlightbackground=BTN_COLOR)
    text.grid(row=1, column=0,padx=5)
    
    result_label = tk.Label(root, text="", font=("Arial", 12), bg=BG_COLOR, fg="black")
    result_label.grid(row=3, column=0, pady=10)

    package_names = await get_all_package_names()
    
    btn = tk.Button(root, text="Click For Search", font=("Arial", 12, "bold"), bg=BTN_COLOR, fg=TEXT_COLOR, borderwidth=2, relief="ridge",
                    command=lambda: show_similar_packages(text.get("1.0", "end-1c"), package_names))
    btn.grid(row=2, column=0, pady=10, sticky="nsew")

    root.mainloop()

def show_similar_packages(text, package_names):
    matches = difflib.get_close_matches(text, package_names)
    
    result_window = Toplevel()
    result_window.title("Similar Packages")
    result_window.geometry("800x600")
    result_window.configure(bg=BG_COLOR)

    if not matches:
        result_label = Label(result_window, text="No Similar Packages Found", font=("Arial", 14, "bold"), bg=BG_COLOR, fg="red")
        result_label.grid(row=2, column=0, pady=20)
        return
    
    result_label = Label(result_window, text="Similar Packages Found", font=("Arial", 14, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
    result_label.pack(pady=20)
    
    for i in matches:
        result_label = Label(result_window, text=i, font=("Arial", 12), bg=BG_COLOR, fg="black")
        result_label.pack(pady=5)
        
def install_packages(package_name):
    try:
        subprocess.check_call(["pip", "install", package_name])
        result_label = Label(root, text="Package Installed Successfully", font=("Arial", 12, "bold"), bg=BG_COLOR, fg="green")
        result_label.grid(row=4, column=0, pady=20)
    except:
        result_label = Label(root, text="Package Installation Failed", font=("Arial", 12, "bold"), bg=BG_COLOR, fg="red")
        result_label.grid(row=4, column=0, pady=20)
        
async def main():
    await scraper.main()
    await user_interface()

if __name__ == "__main__":
    asyncio.run(main())
