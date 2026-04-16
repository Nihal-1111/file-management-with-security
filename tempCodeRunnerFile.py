
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