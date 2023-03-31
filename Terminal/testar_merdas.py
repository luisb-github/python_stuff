import tkinter as tk

root = tk.Tk()
root.withdraw()  # keep the window from showing

print(root.clipboard_get())
