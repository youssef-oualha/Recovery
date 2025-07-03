import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def select_file():
    filename = filedialog.askopenfilename(title="Select Drive Image")
    if filename:
        status_label.config(text=f"Processing {os.path.basename(filename)}...")
        root.update()
        try:
            result = subprocess.run(['recover.exe', filename], capture_output=True, text=True)
            recovered_files = [f for f in os.listdir('.') if f.endswith('.jpg') and f.split('.')[0].isdigit()]
            messagebox.showinfo("JPEG Recovery Complete", f"Processed {os.path.basename(filename)}\n\nRecovered {len(recovered_files)} JPEG files.\n\nNote: Only JPEG files were detected and recovered.")
            status_label.config(text="Ready")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            status_label.config(text="Error occurred")

root = tk.Tk()
root.title("File Recovery Tool")
root.geometry("400x200")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

title_label = tk.Label(frame, text="JPEG Recovery Tool", font=("Arial", 16))
title_label.pack(pady=10)

info_label = tk.Label(frame, text="This tool recovers JPEG files from disk images")
info_label.pack(pady=5)

button = tk.Button(frame, text="Select Drive Image", command=select_file, height=2, width=20)
button.pack(pady=10)

status_label = tk.Label(frame, text="Ready", font=("Arial", 10))
status_label.pack(pady=10)

root.mainloop()