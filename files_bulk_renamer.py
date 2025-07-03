import os
import customtkinter
from tkinter import filedialog, messagebox

# Atur tampilan aplikasi ke mode gelap dan tema biru
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# Inisialisasi window utama
app = customtkinter.CTk()
app.title("📁 Bulk File Renamer")
app.resizable(False, False)  # Tidak dapat di-resize

# Tetapkan lebar window tetap
fixed_width = 600

# Fungsi untuk memilih folder
def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path_entry.delete(0, 'end')
    folder_path_entry.insert(0, folder_selected)
    show_files(folder_selected)

# Fungsi untuk menampilkan file dengan checkbox dan fitur pencarian
def show_files(folder_path, search_keyword=None):
    # Bersihkan isi files_frame sebelum menampilkan file baru
    for widget in files_frame.winfo_children():
        widget.destroy()

    global files, check_vars, select_all_var

    # Ambil daftar file dalam folder
    files = os.listdir(folder_path)
    
    # Filter berdasarkan keyword pencarian jika diisi
    if search_keyword:
        files = [f for f in files if search_keyword.lower() in f.lower()]

    check_vars = []

    # Buat checkbox "Select All"
    select_all_var = customtkinter.IntVar()

    def toggle_all():
        value = select_all_var.get()
        for var, _ in check_vars:
            var.set(value)

    select_all_chk = customtkinter.CTkCheckBox(
        files_frame,
        text="Select All",
        variable=select_all_var,
        command=toggle_all
    )
    select_all_chk.pack(anchor='w', padx=10, pady=5)

    # Buat checkbox untuk setiap file
    for filename in files:
        var = customtkinter.IntVar()
        chk = customtkinter.CTkCheckBox(
            files_frame,
            text=filename,
            variable=var
        )
        chk.pack(anchor='w', padx=20, pady=2)
        check_vars.append((var, filename))

# Fungsi untuk merename file
def rename_files():
    folder_path = folder_path_entry.get()
    prefix = prefix_entry.get()

    # Validasi input folder dan prefix
    if not folder_path or not prefix:
        messagebox.showerror("Error", "Folder path dan prefix tidak boleh kosong.")
        return

    try:
        index = 1
        # Rename file yang tercentang
        for var, filename in check_vars:
            if var.get() == 1:
                old_path = os.path.join(folder_path, filename)
                if os.path.isfile(old_path):
                    extension = os.path.splitext(filename)[1]
                    new_name = f"{prefix}{index}{extension}"
                    new_path = os.path.join(folder_path, new_name)
                    os.rename(old_path, new_path)
                    index += 1

        messagebox.showinfo("Success", "Rename berhasil!")
        show_files(folder_path)  # Refresh daftar file setelah rename
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Frame untuk input path folder
folder_frame = customtkinter.CTkFrame(app)
folder_frame.pack(pady=10, fill='x', padx=20)

folder_path_entry = customtkinter.CTkEntry(folder_frame, placeholder_text="Folder path")
folder_path_entry.pack(side='left', expand=True, fill='x', padx=10, pady=10)

browse_button = customtkinter.CTkButton(folder_frame, text="Browse", command=browse_folder)
browse_button.pack(side='right', padx=10)

# Frame untuk input prefix rename
prefix_frame = customtkinter.CTkFrame(app)
prefix_frame.pack(pady=10, fill='x', padx=20)

prefix_entry = customtkinter.CTkEntry(prefix_frame, placeholder_text="Enter prefix")
prefix_entry.pack(side='left', expand=True, fill='x', padx=10, pady=10)

# Frame untuk input search
search_frame = customtkinter.CTkFrame(app)
search_frame.pack(pady=5, fill='x', padx=20)

search_entry = customtkinter.CTkEntry(search_frame, placeholder_text="Search filename...")
search_entry.pack(side='left', expand=True, fill='x', padx=10, pady=10)

# Fungsi search file berdasarkan keyword
def search_files():
    keyword = search_entry.get()
    show_files(folder_path_entry.get(), search_keyword=keyword)

search_button = customtkinter.CTkButton(search_frame, text="Search", command=search_files)
search_button.pack(side='right', padx=10)

# Frame scrollable untuk menampilkan daftar file
files_scroll = customtkinter.CTkScrollableFrame(app, width=500, height=350, fg_color="gray20")
files_scroll.pack(pady=10)
files_frame = files_scroll

# Tombol untuk menjalankan fungsi rename
rename_button = customtkinter.CTkButton(app, text="Rename Files", command=rename_files)
rename_button.pack(pady=20)

# Update layout untuk mendapatkan tinggi window sebenarnya
app.update_idletasks()

# Hitung posisi x agar window tampil di tengah layar secara horizontal
window_width = fixed_width
window_height = app.winfo_height()
screen_width = app.winfo_screenwidth()
x = int((screen_width / 2) - (window_width / 2))
current_y = app.winfo_y()

# Set posisi window agar berada di tengah x dan tetap di posisi y saat ini
app.geometry(f"{window_width}x{window_height}+{x}+{current_y}")

# Jalankan aplikasi
app.mainloop()
