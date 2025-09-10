# NON FINAL GUI , STRICTLY FOR SPRINT 0

import tkinter as tk

def show_choice():
    choice_label.config(text=f"Selected: {var.get()}")

root = tk.Tk()
root.title("SOS Sprint 0 GUI Demo")
root.geometry("400x300")

# Text
title = tk.Label(root, text="SOS Project GUI Example", font=("Arial", 16))
title.pack(pady=10)

# Canvas with multiple lines
canvas = tk.Canvas(root, width=300, height=150, bg="white")
canvas.pack(pady=10)

# Horizontal line
canvas.create_line(20, 30, 280, 30, fill="blue", width=2)

# Vertical line
canvas.create_line(150, 10, 150, 140, fill="red", width=2)

# Diagonal lines
canvas.create_line(20, 130, 280, 20, fill="green", width=2)
canvas.create_line(20, 20, 280, 130, fill="purple", width=2)

# Checkbox
check_var = tk.IntVar()
check = tk.Checkbutton(root, text="Enable Extra Feature", variable=check_var)
check.pack(pady=5)

# Radio buttons
var = tk.StringVar(value="None")
radio1 = tk.Radiobutton(root, text="Option A", variable=var, value="A", command=show_choice)
radio2 = tk.Radiobutton(root, text="Option B", variable=var, value="B", command=show_choice)
radio1.pack()
radio2.pack()

# Label to show selected option
choice_label = tk.Label(root, text="Selected: None")
choice_label.pack(pady=10)

root.mainloop()
