import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ─────────────────────────────────────────
#  Database Setup
# ─────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT NOT NULL UNIQUE,
        course TEXT NOT NULL,
        email TEXT,
        phone TEXT
    )''')
    conn.commit()
    conn.close()

# ─────────────────────────────────────────
#  CRUD Functions
# ─────────────────────────────────────────
def add_student():
    name = entry_name.get().strip()
    roll = entry_roll.get().strip()
    course = entry_course.get().strip()
    email = entry_email.get().strip()
    phone = entry_phone.get().strip()

    if not name or not roll or not course:
        messagebox.showwarning("Input Error", "Name, Roll No and Course are required!")
        return

    try:
        conn = sqlite3.connect("students.db")
        c = conn.cursor()
        c.execute("INSERT INTO students (name, roll_no, course, email, phone) VALUES (?,?,?,?,?)",
                  (name, roll, course, email, phone))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_fields()
        load_students()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll No already exists!")

def load_students(search_term=""):
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    if search_term:
        c.execute("SELECT * FROM students WHERE name LIKE ? OR roll_no LIKE ?",
                  (f"%{search_term}%", f"%{search_term}%"))
    else:
        c.execute("SELECT * FROM students")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree.insert("", tk.END, values=row)

def select_student(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    clear_fields()
    entry_name.insert(0, values[1])
    entry_roll.insert(0, values[2])
    entry_course.insert(0, values[3])
    entry_email.insert(0, values[4])
    entry_phone.insert(0, values[5])

def update_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select", "Please select a student to update!")
        return
    values = tree.item(selected, "values")
    student_id = values[0]

    name = entry_name.get().strip()
    roll = entry_roll.get().strip()
    course = entry_course.get().strip()
    email = entry_email.get().strip()
    phone = entry_phone.get().strip()

    if not name or not roll or not course:
        messagebox.showwarning("Input Error", "Name, Roll No and Course are required!")
        return

    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("UPDATE students SET name=?, roll_no=?, course=?, email=?, phone=? WHERE id=?",
              (name, roll, course, email, phone, student_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student updated successfully!")
    clear_fields()
    load_students()

def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select", "Please select a student to delete!")
        return
    values = tree.item(selected, "values")
    confirm = messagebox.askyesno("Confirm", f"Delete student '{values[1]}'?")
    if confirm:
        conn = sqlite3.connect("students.db")
        c = conn.cursor()
        c.execute("DELETE FROM students WHERE id=?", (values[0],))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Student deleted successfully!")
        clear_fields()
        load_students()

def search_student():
    term = entry_search.get().strip()
    load_students(term)

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_roll.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_search.delete(0, tk.END)

# ─────────────────────────────────────────
#  GUI Setup
# ─────────────────────────────────────────
init_db()

root = tk.Tk()
root.title("Student Record Management System")
root.geometry("900x600")
root.configure(bg="#f0f4f8")
root.resizable(False, False)

# Title
title = tk.Label(root, text="Student Record Management System",
                 font=("Arial", 18, "bold"), bg="#2c3e50", fg="white", pady=10)
title.pack(fill=tk.X)

# Main Frame
main_frame = tk.Frame(root, bg="#f0f4f8")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Left Frame - Form
form_frame = tk.LabelFrame(main_frame, text="Student Details", font=("Arial", 11, "bold"),
                            bg="#f0f4f8", fg="#2c3e50", padx=10, pady=10)
form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

fields = ["Full Name", "Roll No", "Course", "Email", "Phone"]
entries = []

for i, field in enumerate(fields):
    tk.Label(form_frame, text=field + " :", font=("Arial", 10), bg="#f0f4f8", anchor="w").grid(
        row=i, column=0, sticky="w", pady=5)

entry_name   = tk.Entry(form_frame, width=25, font=("Arial", 10))
entry_roll   = tk.Entry(form_frame, width=25, font=("Arial", 10))
entry_course = tk.Entry(form_frame, width=25, font=("Arial", 10))
entry_email  = tk.Entry(form_frame, width=25, font=("Arial", 10))
entry_phone  = tk.Entry(form_frame, width=25, font=("Arial", 10))

for i, entry in enumerate([entry_name, entry_roll, entry_course, entry_email, entry_phone]):
    entry.grid(row=i, column=1, pady=5, padx=5)

# Buttons
btn_frame = tk.Frame(form_frame, bg="#f0f4f8")
btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

btn_style = {"font": ("Arial", 10, "bold"), "width": 10, "pady": 5, "bd": 0, "cursor": "hand2"}

tk.Button(btn_frame, text="Add",    bg="#27ae60", fg="white", command=add_student,    **btn_style).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", bg="#2980b9", fg="white", command=update_student, **btn_style).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", bg="#e74c3c", fg="white", command=delete_student, **btn_style).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Clear",  bg="#95a5a6", fg="white", command=clear_fields,   **btn_style).grid(row=1, column=1, padx=5, pady=5)

# Right Frame - Table
right_frame = tk.Frame(main_frame, bg="#f0f4f8")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Search Bar
search_frame = tk.Frame(right_frame, bg="#f0f4f8")
search_frame.pack(fill=tk.X, pady=(0, 5))

tk.Label(search_frame, text="🔍 Search:", font=("Arial", 10, "bold"), bg="#f0f4f8").pack(side=tk.LEFT)
entry_search = tk.Entry(search_frame, width=30, font=("Arial", 10))
entry_search.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", bg="#8e44ad", fg="white",
          font=("Arial", 10, "bold"), command=search_student, cursor="hand2").pack(side=tk.LEFT)
tk.Button(search_frame, text="Show All", bg="#16a085", fg="white",
          font=("Arial", 10, "bold"), command=lambda: load_students(), cursor="hand2").pack(side=tk.LEFT, padx=5)

# Treeview Table
cols = ("ID", "Name", "Roll No", "Course", "Email", "Phone")
tree = ttk.Treeview(right_frame, columns=cols, show="headings", height=18)

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=100 if col != "Name" else 140)

tree.pack(fill=tk.BOTH, expand=True)
tree.bind("<ButtonRelease-1>", select_student)

# Scrollbar
scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Status Bar
status = tk.Label(root, text="Student Record Management System | Python + Tkinter + SQLite",
                  bg="#2c3e50", fg="white", font=("Arial", 9), pady=4)
status.pack(fill=tk.X, side=tk.BOTTOM)

load_students()
root.mainloop()