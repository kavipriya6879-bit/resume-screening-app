import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Global dataframe
df = None

# Upload file
def upload_file():
    global df

    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")]
    )

    if file_path:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Success", "File Uploaded Successfully!")
        show_data()

# Show all data
def show_data():
    if df is not None:
        text.delete(1.0, tk.END)
        text.insert(tk.END, df.to_string())
    else:
        messagebox.showwarning("Warning", "Please upload a file first")

# Filter by skill
def filter_skill():
    if df is None:
        messagebox.showwarning("Warning", "Upload file first")
        return

    skill = entry.get()

    if skill == "":
        messagebox.showwarning("Warning", "Enter a skill")
        return

    filtered = df[df['Skills'].str.contains(skill, case=False, na=False)]

    text.delete(1.0, tk.END)

    if filtered.empty:
        text.insert(tk.END, "No candidates found")
    else:
        text.insert(tk.END, filtered.to_string())

# Best candidates (ranking)
def best_candidates():
    if df is None:
        messagebox.showwarning("Warning", "Upload file first")
        return

    # Score logic: Experience priority
    ranked = df.copy()
    ranked["Score"] = ranked["Experience"] * 10

    best = ranked.sort_values(by="Score", ascending=False).head(5)

    text.delete(1.0, tk.END)
    text.insert(tk.END, "🏆 BEST CANDIDATES:\n\n")
    text.insert(tk.END, best.to_string(index=False))

# UI
app = tk.Tk()
app.title("Automated Resume Screening System")
app.geometry("750x500")

tk.Label(app, text="Resume Screening AI System", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(app, text="📂 Upload CSV File", command=upload_file).pack(pady=5)
tk.Button(app, text="📊 Show All Data", command=show_data).pack(pady=5)

tk.Label(app, text="Enter Skill to Filter").pack()
entry = tk.Entry(app, width=30)
entry.pack(pady=5)

tk.Button(app, text="🔍 Filter Candidates", command=filter_skill).pack(pady=5)
tk.Button(app, text="🏆 Best Candidates", command=best_candidates).pack(pady=5)

text = tk.Text(app, height=20, width=90)
text.pack(pady=10)

app.mainloop()
