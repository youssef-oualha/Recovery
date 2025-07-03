import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import glob

def select_file():
    filename = filedialog.askopenfilename(title="Select Drive Image")
    if filename:
        status_label.config(text=f"Processing {os.path.basename(filename)}...")
        root.update()
        try:
            result = subprocess.run(['recover.exe', filename], capture_output=True, text=True)
            
            # Count recovered files by type
            file_counts = {
                'JPEG': len(glob.glob("[0-9][0-9][0-9].jpg")),
                'PNG': len(glob.glob("[0-9][0-9][0-9].png")),
                'PDF': len(glob.glob("[0-9][0-9][0-9].pdf")),
                'DOCX': len(glob.glob("[0-9][0-9][0-9].docx")),
                'GIF': len(glob.glob("[0-9][0-9][0-9].gif")),
                'MP3': len(glob.glob("[0-9][0-9][0-9].mp3")),
                'BMP': len(glob.glob("[0-9][0-9][0-9].bmp")),
                'RAR': len(glob.glob("[0-9][0-9][0-9].rar"))
            }
            
            total_files = sum(file_counts.values())
            
            # Create recovery summary
            summary = f"Processed {os.path.basename(filename)}\n\n"
            summary += f"Recovery Summary:\n"
            
            # Only show file types that were actually recovered
            for file_type, count in file_counts.items():
                if count > 0:
                    if file_type in ['JPEG', 'PNG', 'GIF', 'BMP']:
                        summary += f"- {file_type} images: {count}\n"
                    elif file_type in ['PDF', 'DOCX']:
                        summary += f"- {file_type} documents: {count}\n"
                    elif file_type == 'MP3':
                        summary += f"- MP3 audio files: {count}\n"
                    elif file_type == 'RAR':
                        summary += f"- RAR archives: {count}\n"
            
            summary += f"\nTotal files recovered: {total_files}"
            
            # Show detailed results dialog
            show_results_dialog(file_counts, total_files, filename)
            
            status_label.config(text="Ready")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            status_label.config(text="Error occurred")

def show_results_dialog(file_counts, total_files, filename):
    """Show a more detailed results dialog with a table of recovered files"""
    results_window = tk.Toplevel(root)
    results_window.title("Recovery Results")
    results_window.geometry("400x450")
    results_window.resizable(False, False)
    
    # Add some padding
    frame = tk.Frame(results_window, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Header
    header = tk.Label(frame, text="File Recovery Results", font=("Arial", 14, "bold"))
    header.pack(pady=(0, 10))
    
    # File processed
    file_label = tk.Label(frame, text=f"Processed: {os.path.basename(filename)}")
    file_label.pack(pady=(0, 15))
    
    # Create a treeview for the results table
    columns = ("type", "count")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
    
    # Define headings
    tree.heading("type", text="File Type")
    tree.heading("count", text="Count")
    
    # Column widths
    tree.column("type", width=200)
    tree.column("count", width=100)
    
    # Add data
    for file_type, count in file_counts.items():
        icon = "🖼️" if file_type in ['JPEG', 'PNG', 'GIF', 'BMP'] else "📄"
        if file_type == 'MP3': icon = "🎵"
        if file_type == 'RAR': icon = "📦"
        
        tree.insert("", tk.END, values=(f"{icon} {file_type}", count))
    
    # Add total row
    tree.insert("", tk.END, values=("TOTAL", total_files), tags=("total",))
    tree.tag_configure("total", background="#e0e0e0", font=("Arial", 9, "bold"))
    
    tree.pack(pady=10)
    
    # Summary label
    if total_files > 0:
        summary_text = "All files have been saved to the application directory."
    else:
        summary_text = "No files were recovered. The image may not contain supported file types."
    
    summary_label = tk.Label(frame, text=summary_text)
    summary_label.pack(pady=10)
    
    # Close button
    close_button = tk.Button(frame, text="Close", command=results_window.destroy, width=10)
    close_button.pack(pady=10)

root = tk.Tk()
root.title("Multi-Format File Recovery Tool")
root.geometry("450x250")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

title_label = tk.Label(frame, text="Multi-Format File Recovery Tool", font=("Arial", 16))
title_label.pack(pady=10)

info_label = tk.Label(frame, text="This tool recovers multiple file types from forensic disk images")
info_label.pack(pady=2)

formats_label = tk.Label(frame, text="Supported formats: JPEG, PNG, PDF, DOCX, GIF, MP3, BMP, RAR")
formats_label.pack(pady=2)

button = tk.Button(frame, text="Select Drive Image", command=select_file, height=2, width=20)
button.pack(pady=10)

status_label = tk.Label(frame, text="Ready", font=("Arial", 10))
status_label.pack(pady=10)

root.mainloop()