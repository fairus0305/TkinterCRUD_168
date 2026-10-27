import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_db()

def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Dapat Ditentukan"

def submit_nilai():
    nama = entry_nama.get().strip()
    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return

    if not nama:
        messagebox.showerror("Error", "Nama siswa tidak boleh kosong!")
        return

    hasil_prediksi = prediksi_fakultas(bio, fis, ing)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil_prediksi))
    conn.commit()
    conn.close()

    messagebox.showinfo("Hasil Prediksi", f"Prediksi Fakultas: {hasil_prediksi}")

    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)


root = tk.Tk()
root.title("Aplikasi Nilai Siswa")
root.geometry("400x350")

label_judul = tk.Label(
    root,
    text="Aplikasi Nilai Siswa",
    font=("Arial", 18, "bold"),
)
label_judul.pack(pady=10)

def buat_input(teks):
    frame = tk.Frame(root)
    frame.pack(pady=3)
    tk.Label(frame, text=teks, width=20, anchor="w").pack(side="left")
    entry = tk.Entry(frame, width=15)
    entry.pack(side="left")
    return entry

entry_nama = buat_input("Nama Siswa")
entry_bio  = buat_input("Biologi")
entry_fis  = buat_input("Fisika")
entry_ing  = buat_input("Inggris")

# Tombol + hover
def on_enter(e):
    btn_submit["bg"] = "#50fa7b"
    btn_submit["fg"] = "black"

def on_leave(e):
    btn_submit["bg"] = "SystemButtonFace"
    btn_submit["fg"] = "black"

btn_submit = tk.Button(root, text="Submit Nilai", command=submit_nilai)
btn_submit.pack(pady=10)
btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

root.mainloop()