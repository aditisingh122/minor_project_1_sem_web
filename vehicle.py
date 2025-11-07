import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ------------------ MySQL Connection ------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",             
        password="25mca20298",   
        database="vehicle_db"
    )

# ------------------ CRUD Functions ------------------
def add_vehicle():
    reg = reg_entry.get()
    owner = owner_entry.get()
    vtype = type_entry.get()
    color = color_entry.get()

    if reg == "" or owner == "" or vtype == "" or color == "":
        messagebox.showerror("Error", "All fields are required")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO vehicles (reg_no, owner, vehicle_type, color) VALUES (%s, %s, %s, %s)",
                (reg, owner, vtype, color))
    conn.commit()
    conn.close()
    fetch_data()
    clear_fields()
    messagebox.showinfo("Success", "Vehicle added successfully!")

def fetch_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles")
    rows = cur.fetchall()
    table.delete(*table.get_children())
    for row in rows:
        table.insert("", tk.END, values=row)
    conn.close()

def get_cursor(event):
    cursor_row = table.focus()
    content = table.item(cursor_row)
    row = content['values']
    if row:
        clear_fields()
        reg_entry.insert(0, row[1])
        owner_entry.insert(0, row[2])
        type_entry.insert(0, row[3])
        color_entry.insert(0, row[4])

def update_vehicle():
    selected = table.focus()
    if not selected:
        messagebox.showerror("Error", "Select a record to update")
        return
    values = table.item(selected, "values")
    vid = values[0]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE vehicles SET reg_no=%s, owner=%s, vehicle_type=%s, color=%s WHERE id=%s",
                (reg_entry.get(), owner_entry.get(), type_entry.get(), color_entry.get(), vid))
    conn.commit()
    conn.close()
    fetch_data()
    clear_fields()
    messagebox.showinfo("Updated", "Vehicle record updated successfully!")

def delete_vehicle():
    selected = table.focus()
    if not selected:
        messagebox.showerror("Error", "Select a record to delete")
        return
    values = table.item(selected, "values")
    vid = values[0]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM vehicles WHERE id=%s", (vid,))
    conn.commit()
    conn.close()
    fetch_data()
    messagebox.showinfo("Deleted", "Vehicle record deleted successfully!")

def search_vehicle():
    keyword = search_entry.get()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles WHERE reg_no LIKE %s OR owner LIKE %s OR vehicle_type LIKE %s",
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    rows = cur.fetchall()
    table.delete(*table.get_children())
    for row in rows:
        table.insert("", tk.END, values=row)
    conn.close()

def clear_fields():
    reg_entry.delete(0, tk.END)
    owner_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)
    color_entry.delete(0, tk.END)

# ------------------ GUI ------------------
root = tk.Tk()
root.title(" Vehicle Record System")
root.state("zoomed")
root.configure(bg="#0e1a2b")

title = tk.Label(root, text="VEHICLE RECORD SYSTEM", 
                 font=("Poppins", 30, "bold"), bg="#0e1a2b", fg="#00ffcc")
title.pack(pady=20)

# ------------------ Form Frame ------------------
form_frame = tk.Frame(root, bg="#112240", bd=6, relief="ridge")
form_frame.pack(fill="x", padx=40, pady=10, ipady=10)

label_font = ("Segoe UI Semibold", 16)
entry_font = ("Poppins", 14)

tk.Label(form_frame, text="Reg No:", font=label_font, bg="#112240", fg="white").grid(row=0, column=0, padx=20, pady=15)
reg_entry = tk.Entry(form_frame, font=entry_font, width=25)
reg_entry.grid(row=0, column=1, padx=20, pady=15)

tk.Label(form_frame, text="Owner Name:", font=label_font, bg="#112240", fg="white").grid(row=0, column=2, padx=20, pady=15)
owner_entry = tk.Entry(form_frame, font=entry_font, width=25)
owner_entry.grid(row=0, column=3, padx=20, pady=15)

tk.Label(form_frame, text="Vehicle Type:", font=label_font, bg="#112240", fg="white").grid(row=1, column=0, padx=20, pady=15)
type_entry = tk.Entry(form_frame, font=entry_font, width=25)
type_entry.grid(row=1, column=1, padx=20, pady=15)

tk.Label(form_frame, text="Color:", font=label_font, bg="#112240", fg="white").grid(row=1, column=2, padx=20, pady=15)
color_entry = tk.Entry(form_frame, font=entry_font, width=25)
color_entry.grid(row=1, column=3, padx=20, pady=15)

# ------------------ Hover Button ------------------
def on_enter(e):
    e.widget["background"] = e.widget.hover_color

def on_leave(e):
    e.widget["background"] = e.widget.default_color

def create_button(parent, text, bg, hover, cmd):
    btn = tk.Button(parent, text=text, bg=bg, fg="white", font=("Poppins", 14, "bold"),
                    width=12, bd=0, relief="flat", command=cmd, activebackground=hover, cursor="hand2")
    btn.default_color = bg
    btn.hover_color = hover
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.configure(highlightthickness=0, padx=10, pady=8)
    return btn

# ------------------ Button Frame ------------------
btn_frame = tk.Frame(root, bg="#0e1a2b")
btn_frame.pack(pady=15)

create_button(btn_frame, "Add", "#28a745", "#34d058", add_vehicle).grid(row=0, column=0, padx=15)
create_button(btn_frame, "Update", "#007bff", "#339dff", update_vehicle).grid(row=0, column=1, padx=15)
create_button(btn_frame, "Delete", "#dc3545", "#ff4b5c", delete_vehicle).grid(row=0, column=2, padx=15)
create_button(btn_frame, "Clear", "#6f42c1", "#8e60e6", clear_fields).grid(row=0, column=3, padx=15)

# ------------------ Search Frame ------------------
search_frame = tk.Frame(root, bg="#0e1a2b")
search_frame.pack(pady=15)

tk.Label(search_frame, text="Search:", font=("Poppins", 16, "bold"), bg="#0e1a2b", fg="white").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, font=("Poppins", 14), width=30)
search_entry.pack(side=tk.LEFT, padx=10)
search_btn = create_button(search_frame, "Search", "#ff9800", "#ffb74d", search_vehicle)
search_btn.pack(side=tk.LEFT, padx=5)

# ------------------ Table Frame ------------------
table_frame = tk.Frame(root, bg="#112240", bd=6, relief="ridge")
table_frame.pack(fill="both", expand=True, padx=40, pady=10)

columns = ("id", "reg_no", "owner", "vehicle_type", "color")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Poppins", 15, "bold"), background="#00ffcc", foreground="black")
style.configure("Treeview", font=("Segoe UI", 13), rowheight=30, background="#0e1a2b", foreground="white", fieldbackground="#0e1a2b")

for col in columns:
    table.heading(col, text=col.title())
    table.column(col, anchor="center", width=250)

table.pack(fill="both", expand=True)
table.bind("<ButtonRelease-1>", get_cursor)

fetch_data()
root.mainloop()
