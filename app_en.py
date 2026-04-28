import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

SALT = b'fixed_salt_change_me!'  # In production, generate randomly and store in file
ITERATIONS = 100_000

def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive encryption key from master password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(master_password.encode())

def encrypt(data: str, password: str) -> bytes:
    """Encrypt data using AES encryption."""
    key = derive_key(password, SALT)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data.encode()) + encryptor.finalize()
    return base64.b64encode(iv + encrypted)

def decrypt(encrypted_b64: bytes, password: str) -> str:
    """Decrypt data using AES decryption."""
    raw = base64.b64decode(encrypted_b64)
    iv = raw[:16]
    encrypted_data = raw[16:]
    key = derive_key(password, SALT)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted.decode()

def load_vault(password: str, filename="vault.dat"):
    """Load encrypted vault from file."""
    if not os.path.exists(filename):
        return {}
    with open(filename, "rb") as f:
        encrypted = f.read()
    try:
        return json.loads(decrypt(encrypted, password))
    except Exception:
        return None

def save_vault(vault, password: str, filename="vault.dat"):
    """Save vault to encrypted file."""
    data = json.dumps(vault, indent=2)
    encrypted = encrypt(data, password)
    with open(filename, "wb") as f:
        f.write(encrypted)
    return True

class PasswordVault:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Simple Password Vault")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        self.vault = None
        self.master_password = None
        
        # Show login screen
        self.show_login()
    
    def show_login(self):
        """Display login screen."""
        # Clear main frame
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Login frame
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="🔐 Welcome to Password Vault", 
                  font=("Arial", 16, "bold")).pack(pady=20)
        
        ttk.Label(frame, text="Master Password:", font=("Arial", 10)).pack(pady=5)
        self.password_entry = ttk.Entry(frame, show="*", width=30, font=("Arial", 10))
        self.password_entry.pack(pady=5)
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        ttk.Button(frame, text="Login", command=self.login, width=20).pack(pady=10)
        
        # Security warning
        warning_text = """⚠️ SECURITY WARNING ⚠️

• Use a strong master password (weak passwords can be cracked via brute-force)
• Protect the vault.dat file from unauthorized access
• This tool does not guarantee complete security
• For critical passwords, use hardware-based security solutions"""
        
        warning_label = ttk.Label(frame, text=warning_text, foreground="red",
                                  justify=tk.LEFT, font=("Arial", 8))
        warning_label.pack(pady=20)
    
    def login(self):
        """Authenticate with master password."""
        self.master_password = self.password_entry.get()
        if not self.master_password:
            messagebox.showerror("Error", "Master password cannot be empty!")
            return
        
        self.vault = load_vault(self.master_password)
        if self.vault is None:
            messagebox.showerror("Error", "Incorrect master password or corrupted file!")
            return
        
        self.show_main_interface()
    
    def show_main_interface(self):
        """Display main application interface."""
        # Clear main frame
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=5)
        ttk.Label(title_frame, text="🔐 Password Vault", 
                  font=("Arial", 18, "bold")).pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="➕ Add Password", 
                   command=self.add_password, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Delete", 
                   command=self.delete_password, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Refresh", 
                   command=self.refresh_list, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🚪 Logout", 
                   command=self.logout, width=10).pack(side=tk.RIGHT, padx=5)
        
        # Search bar
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_list())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Table (Treeview)
        columns = ("site", "username", "password")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
        
        # Column headers
        self.tree.heading("site", text="🏷️ Site/Name", command=lambda: self.sort_by("site"))
        self.tree.heading("username", text="👤 Username", command=lambda: self.sort_by("username"))
        self.tree.heading("password", text="🔑 Password", command=lambda: self.sort_by("password"))
        
        # Column widths
        self.tree.column("site", width=200)
        self.tree.column("username", width=200)
        self.tree.column("password", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to show password details
        self.tree.bind("<Double-1>", self.show_password_detail)
        
        # Statistics
        self.stats_label = ttk.Label(main_frame, text="", font=("Arial", 9))
        self.stats_label.pack(pady=5)
        
        # Show list
        self.refresh_list()
    
    def refresh_list(self):
        """Refresh the password list display."""
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add data
        for site, info in self.vault.items():
            self.tree.insert("", tk.END, values=(site, info["username"], info["password"]))
        
        # Update statistics
        self.stats_label.config(text=f"Total {len(self.vault)} passwords stored")
    
    def filter_list(self):
        """Filter passwords based on search input."""
        search_text = self.search_var.get().lower()
        
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter and add
        for site, info in self.vault.items():
            if search_text in site.lower() or search_text in info["username"].lower():
                self.tree.insert("", tk.END, values=(site, info["username"], info["password"]))
    
    def sort_by(self, column):
        """Sort password list by specified column."""
        # Simple sorting
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children()]
        items.sort()
        
        for index, (_, item) in enumerate(items):
            self.tree.move(item, "", index)
    
    def add_password(self):
        """Add a new password to the vault."""
        # New window
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Password")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Center the window
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Site/Name:", font=("Arial", 10)).pack(anchor=tk.W, pady=5)
        site_entry = ttk.Entry(frame, width=40, font=("Arial", 10))
        site_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Username:", font=("Arial", 10)).pack(anchor=tk.W, pady=5)
        user_entry = ttk.Entry(frame, width=40, font=("Arial", 10))
        user_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Password:", font=("Arial", 10)).pack(anchor=tk.W, pady=5)
        pass_entry = ttk.Entry(frame, width=40, font=("Arial", 10))
        pass_entry.pack(fill=tk.X, pady=5)
        
        def save():
            site = site_entry.get().strip()
            username = user_entry.get().strip()
            password = pass_entry.get().strip()
            
            if not site or not username or not password:
                messagebox.showwarning("Warning", "Please fill all fields!")
                return
            
            if site in self.vault:
                if not messagebox.askyesno("Warning", "This site already exists. Do you want to overwrite it?"):
                    return
            
            self.vault[site] = {"username": username, "password": password}
            if save_vault(self.vault, self.master_password):
                messagebox.showinfo("Success", "Password added successfully!")
                self.refresh_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Error occurred while saving!")
        
        ttk.Button(frame, text="Save", command=save, width=15).pack(pady=20)
        
        # Save with Enter key
        pass_entry.bind("<Return>", lambda e: save())
    
    def delete_password(self):
        """Delete a password from the vault."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a password to delete!")
            return
        
        site = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete '{site}' password?"):
            del self.vault[site]
            if save_vault(self.vault, self.master_password):
                messagebox.showinfo("Success", "Password deleted!")
                self.refresh_list()
            else:
                messagebox.showerror("Error", "Error occurred while deleting!")
    
    def show_password_detail(self, event):
        """Show password details and allow copying."""
        selected = self.tree.selection()
        if not selected:
            return
        
        values = self.tree.item(selected[0])["values"]
        site, username, password = values
        
        # Detail window
        detail = tk.Toplevel(self.root)
        detail.title(f"{site} - Password Details")
        detail.geometry("400x250")
        detail.resizable(False, False)
        detail.transient(self.root)
        detail.grab_set()
        
        frame = ttk.Frame(detail, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"🏷️ Site: {site}", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=10)
        ttk.Label(frame, text=f"👤 Username: {username}", font=("Arial", 11)).pack(anchor=tk.W, pady=5)
        
        pass_frame = ttk.Frame(frame)
        pass_frame.pack(anchor=tk.W, pady=5)
        ttk.Label(pass_frame, text=f"🔑 Password: {password}", font=("Arial", 11)).pack(side=tk.LEFT)
        
        def copy_password():
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        
        ttk.Button(pass_frame, text="📋 Copy", command=copy_password, width=10).pack(side=tk.LEFT, padx=10)
        
        def copy_username():
            self.root.clipboard_clear()
            self.root.clipboard_append(username)
            messagebox.showinfo("Copied", "Username copied to clipboard!")
        
        ttk.Button(frame, text="👤 Copy Username", command=copy_username, width=20).pack(anchor=tk.W, pady=5)
        
        ttk.Button(frame, text="Close", command=detail.destroy, width=15).pack(pady=20)
    
    def logout(self):
        """Logout from the vault."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout from the password vault?"):
            self.vault = None
            self.master_password = None
            self.show_login()

def main():
    root = tk.Tk()
    app = PasswordVault(root)
    root.mainloop()

if __name__ == "__main__":
    main()
