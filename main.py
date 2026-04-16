import security
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import hashlib, json, os, sys
from file_manager import FileManager  # Make sure this exists with an arrange_files method

# ---------------- PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEC_FILE = os.path.join(BASE_DIR, "security.json")

# ---------------- HELPERS ----------------
def hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode()).hexdigest()

def load_config():
    if not os.path.exists(SEC_FILE):
        return None
    with open(SEC_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return None

def save_config(password: str, master_password: str):
    data = {
        "password_hash": hash_password(password),
        "master_password_hash": hash_password(master_password)
    }
    with open(SEC_FILE, "w") as f:
        json.dump(data, f)

# ---------------- FIRST TIME SETUP ----------------
def first_time_setup():
    root = tk.Tk()
    root.withdraw()  

    messagebox.showinfo("Setup", "Welcome — no passwords found. Let's set them up.")

    while True:
        pwd = simpledialog.askstring("Setup - Login Password", "Set your login password:", show="*", parent=root)
        if pwd is None:
            messagebox.showerror("Setup aborted", "Setup cancelled. App will exit.")
            root.destroy()
            return False
        pwd2 = simpledialog.askstring("Setup - Confirm Login", "Confirm login password:", show="*", parent=root)
        if pwd2 is None:
            messagebox.showerror("Setup aborted", "Setup cancelled. App will exit.")
            root.destroy()
            return False
        if pwd != pwd2:
            messagebox.showerror("Error", "Login passwords do not match. Try again.")
            continue

        master = simpledialog.askstring("Setup - Master Password", "Set master (recovery) password:", show="*", parent=root)
        if master is None:
            messagebox.showerror("Setup aborted", "Setup cancelled. App will exit.")
            root.destroy()
            return False
        master2 = simpledialog.askstring("Setup - Confirm Master", "Confirm master password:", show="*", parent=root)
        if master2 is None:
            messagebox.showerror("Setup aborted", "Setup cancelled. App will exit.")
            root.destroy()
            return False
        if master != master2:
            messagebox.showerror("Error", "Master passwords do not match. Try again.")
            continue

        save_config(pwd, master)
        messagebox.showinfo("Setup Complete", "Passwords saved successfully.\nअब नया password डालकर login करें")
        root.destroy()
        return True

# ---------------- LOGIN SCREEN ----------------
def login_screen(start_app_callback):
    login = tk.Tk()
    login.title("Login Required")
    login.geometry("360x190")
    login.resizable(False, False)

    tk.Label(login, text="Enter Password:", font=("Arial", 11)).pack(pady=8)
    entry = tk.Entry(login, show="*", font=("Arial", 12), width=28)
    entry.pack(pady=5)

    reset_btn = tk.Button(login, text="Reset Password", bg="orange", fg="black")
    reset_btn.pack_forget()  # Hidden initially

    # ---------------- Reset Password ----------------
    def open_reset_password(master_pwd):
        reset_win = tk.Toplevel(login)
        reset_win.title("Reset Password")
        reset_win.geometry("360x220")
        reset_win.resizable(False, False)

        tk.Label(reset_win, text="Enter New Password:", font=("Arial", 10)).pack(pady=8)
        new_entry = tk.Entry(reset_win, show="*", font=("Arial", 12), width=28)
        new_entry.pack(pady=5)

        tk.Label(reset_win, text="Confirm New Password:", font=("Arial", 10)).pack(pady=8)
        confirm_entry = tk.Entry(reset_win, show="*", font=("Arial", 12), width=28)
        confirm_entry.pack(pady=5)

        def save_new():
            new = new_entry.get().strip()
            conf = confirm_entry.get().strip()
            if not new:
                messagebox.showerror("Error", "Password cannot be empty.")
                return
            if new != conf:
                messagebox.showerror("Error", "Passwords do not match.")
                return
            save_config(new, master_pwd)
            messagebox.showinfo("Success", "Password changed successfully ✅\nअब नया password डालकर login करें")
            reset_win.destroy()

        tk.Button(reset_win, text="Save", command=save_new, bg="green", fg="white").pack(pady=12)

    # ---------------- Master Verification ----------------
    def open_master_check():
        master_win = tk.Toplevel(login)
        master_win.title("Master Verification")
        master_win.geometry("340x150")
        master_win.resizable(False, False)

        tk.Label(master_win, text="Enter Master Password:", font=("Arial", 10)).pack(pady=8)
        master_entry = tk.Entry(master_win, show="*", font=("Arial", 12), width=26)
        master_entry.pack(pady=5)

        def verify_master():
            config = load_config()
            if not config:
                messagebox.showerror("Error", "No configuration found.")
                master_win.destroy()
                return
            mp = master_entry.get()
            if hash_password(mp) == config.get("master_password_hash"):
                master_win.destroy()
                open_reset_password(mp)
            else:
                messagebox.showerror("Error", "Invalid Master Password!")

        tk.Button(master_win, text="Verify", command=verify_master, bg="green", fg="white").pack(pady=10)

    reset_btn.config(command=open_master_check)

    # ---------------- Verify Login ----------------
    def verify():
        config = load_config()
        if not config:
            messagebox.showerror("Error", "Configuration missing. Restart app to setup.")
            login.destroy()
            sys.exit(0)

        pwd = entry.get()
        if hash_password(pwd) == config.get("password_hash"):
            login.destroy()
            start_app_callback()
        else:
            messagebox.showerror("Error", "Wrong Password ❌")
            reset_btn.pack(pady=8)

    tk.Button(login, text="Login", command=verify, bg="blue", fg="white").pack(pady=10)

    login.mainloop()

# ---------------- MAIN APP ----------------
def main_app():
    root = tk.Tk()
    root.title("File Arranger System")
    root.geometry("800x600")
    root.config(bg="lightblue")

    tk.Label(root, text="File Arranger System", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=10)

    path_entry = tk.Entry(root, width=60, font=("Arial", 12))
    path_entry.pack(pady=5)

    def browse_path():
        folder_selected = filedialog.askdirectory(title="Select Folder")
        if folder_selected:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, folder_selected)

    tk.Button(root, text="Browse", command=browse_path, bg="brown", fg="white").pack(pady=5)

    output_box = tk.Text(root, height=20, width=90, font=("Arial", 10))
    output_box.pack(pady=10)

    # ---------------- File Manager ----------------
    def start_file_manage():
        folder_path = path_entry.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder path.")
            return
        fm = FileManager(folder_path, output_box)
        fm.arrange_files()

    tk.Button(root, text="Manage Files", command=start_file_manage, bg="green", fg="white").pack(pady=5)
    tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white").pack(pady=5)

    # ---------------- Encrypt / Decrypt ----------------
    def choose_file_and_encrypt():
        file_path = filedialog.askopenfilename(title="Select file to encrypt")
        if file_path:
            try:
                security.encrypt_file(file_path)
                messagebox.showinfo("Success", f"✅ File encrypted:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def choose_file_and_decrypt():
        file_path = filedialog.askopenfilename(title="Select file to decrypt")
        if file_path:
            # Password prompt for decrypt
            pwd = simpledialog.askstring("Decrypt File", "Enter password to decrypt file:", show="*")
            if not pwd:
                messagebox.showerror("Error", "Password is required to decrypt the file.")
                return

            # Verify password
            config = load_config()
            if not config:
                messagebox.showerror("Error", "No password config found.")
                return

            if hash_password(pwd) != config.get("password_hash"):
                messagebox.showerror("Error", "Incorrect password! ❌")
                return

            try:
                security.decrypt_file(file_path)
                messagebox.showinfo("Success", f"🔓 File decrypted:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    action_frame = tk.Frame(root, bg="lightblue")
    action_frame.pack(pady=15)

    tk.Button(action_frame, text="Encrypt File", width=20, bg="lightblue", command=choose_file_and_encrypt).grid(row=0, column=0, padx=10)
    tk.Button(action_frame, text="Decrypt File", width=20, bg="lightgreen", command=choose_file_and_decrypt).grid(row=0, column=1, padx=10)

    root.mainloop()

# ---------------- RUN ----------------
if __name__ == "__main__":
    config = load_config()
    if not config:
        if first_time_setup():
            login_screen(main_app)
    else:
        login_screen(main_app)
