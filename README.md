# 🔐 Simple Password Vault

A secure, lightweight password manager application with a graphical user interface (GUI) built using Python's Tkinter library. All passwords are encrypted using AES-256 encryption.

## 📋 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Security Information](#security-information)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- **🔐 Master Password Protection**: Secure your entire vault with a single master password
- **🔒 AES-256 Encryption**: Industry-standard encryption for all stored passwords
- **➕ Add Passwords**: Store site names, usernames, and passwords
- **🗑️ Delete Passwords**: Remove unwanted entries from your vault
- **🔍 Search Functionality**: Quickly find passwords by site name or username
- **📊 Sort Capabilities**: Sort passwords by Site, Username, or Password
- **📋 Copy to Clipboard**: Easily copy usernames and passwords to clipboard
- **🔄 Refresh**: Update the password list display
- **💾 Persistent Storage**: All passwords are saved to an encrypted file (`vault.dat`)

---

## 🖥️ System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**:
  - `tkinter` (usually comes with Python)
  - `cryptography` library

---

## 📦 Installation

### Step 1: Install Python
Download and install Python 3.7+ from [python.org](https://www.python.org/downloads/)

### Step 2: Install Required Libraries
Open a terminal/command prompt and run:

```bash
pip install cryptography
```

### Step 3: Run the Application
Navigate to the directory containing `app_en.py` and run:

```bash
python app_en.py
```

The application window should appear immediately.

---

## 📖 Usage Guide

### First Launch - Creating Your Vault

1. **Launch the Application**
   - Run `python app_en.py`
   - The login screen will appear with a security warning

2. **Set Your Master Password**
   - Enter a strong master password in the text field
   - **Important**: Remember this password! If you forget it, you won't be able to access your vault
   - Click the **"Login"** button or press Enter

3. **Important Security Note**
   - If this is your first time, an empty vault will be created
   - The next time you launch the app, use the same master password to access your existing vault
   - If you enter a wrong password, you'll get an error message

### Main Interface

Once logged in, you'll see the main vault interface with:

| Element | Description |
|---------|-------------|
| **Title Bar** | Shows "🔐 Password Vault" |
| **Buttons** | ➕ Add, 🗑️ Delete, 🔄 Refresh, 🚪 Logout |
| **Search Bar** | Filter passwords by site or username |
| **Table** | Displays all stored passwords (Site, Username, Password) |
| **Statistics** | Shows total number of stored passwords |

### Adding a New Password

1. Click the **"➕ Add Password"** button
2. A dialog window will open with three fields:
   - **Site/Name**: Name of the website or service (e.g., "Gmail", "Facebook")
   - **Username**: Your username or email for that service
   - **Password**: Your password for that service

3. Fill in all three fields
4. Click **"Save"** or press Enter
5. Confirm the dialog, and the password will be added to your vault

**Note**: If you add a password for a site that already exists, the app will ask if you want to overwrite it.

### Viewing Password Details

1. **Double-click** on any password entry in the table
2. A detail window will open showing:
   - The site/name
   - The username
   - The password with a "📋 Copy" button
   - A "👤 Copy Username" button

3. Click the **"Copy"** button to copy the password to your clipboard
4. Click the **"Copy Username"** button to copy the username to your clipboard
5. Click **"Close"** to exit the detail window

### Searching for Passwords

1. Use the **"Search:"** field at the top of the main window
2. Type any part of the site name or username
3. The table will automatically filter to show only matching results
4. The search is case-insensitive

**Example**: Typing "gm" will show all passwords with "gm" in the site name or username.

### Sorting Passwords

1. Click on any column header to sort by that column:
   - **"🏷️ Site/Name"** - Sort alphabetically by site name
   - **"👤 Username"** - Sort alphabetically by username
   - **"🔑 Password"** - Sort alphabetically by password

2. Click again to reverse the sort order

### Deleting a Password

1. **Select** the password you want to delete by clicking on it in the table
2. Click the **"🗑️ Delete"** button
3. Confirm the deletion in the dialog box
4. The password will be permanently removed from your vault

### Refreshing the List

- Click the **"🔄 Refresh"** button to reload and display all passwords
- Useful if you've made multiple changes and want to see the current state

### Logging Out

1. Click the **"🚪 Logout"** button
2. Confirm the logout in the dialog box
3. You'll be returned to the login screen
4. To access your vault again, enter your master password

---

## 🔒 Security Information

### How It Works

- **Encryption**: All passwords are encrypted using AES-256 in CFB mode
- **Key Derivation**: Your master password is converted into an encryption key using PBKDF2 with SHA-256
- **Storage**: Encrypted data is saved to `vault.dat` file
- **No Cloud**: Everything stays on your local machine

### Security Best Practices

⚠️ **IMPORTANT**:

1. **Use a Strong Master Password**
   - Avoid simple or common passwords
   - Use a mix of uppercase, lowercase, numbers, and special characters
   - Use at least 12 characters
   - Don't use words from the dictionary

2. **Protect the vault.dat File**
   - This file contains all your encrypted passwords
   - Keep it in a secure location
   - Don't share it with anyone
   - Back it up regularly

3. **Keep Your Computer Secure**
   - Use antivirus software
   - Keep your operating system and software updated
   - Use a strong computer password

4. **Never Share Your Master Password**
   - This password is the key to your entire vault
   - No one should ever ask for it

### Limitations

- This tool provides basic password management and encryption
- For highly critical passwords (banking, cryptocurrency), consider hardware security keys
- The salt value is fixed in the code - for production use, generate it randomly
- Always test your backups to ensure they work

---

## 🐛 Troubleshooting

### Issue: "Master password cannot be empty!"
**Solution**: You tried to login without entering a password. Enter a password and try again.

### Issue: "Incorrect master password or corrupted file!"
**Solution**:
- You entered the wrong master password
- The `vault.dat` file may be corrupted
- Try using the correct master password
- If you're sure you have the right password, your file may be corrupted and you may need to delete `vault.dat` and start over

### Issue: Application won't start
**Solution**:
1. Ensure Python 3.7+ is installed: `python --version`
2. Ensure cryptography is installed: `pip install cryptography`
3. Try running from command line to see error messages: `python app_en.py`

### Issue: "ModuleNotFoundError: No module named 'cryptography'"
**Solution**: Install the missing library:
```bash
pip install cryptography
```

### Issue: Cannot copy to clipboard
**Solution**:
- This may be a system-specific issue
- Try copying again
- Check that your system clipboard is working properly
- Restart the application

### Issue: Forgot your master password
**Solution**:
- Unfortunately, there's no password recovery option
- Your vault is permanently locked
- You'll need to delete `vault.dat` and create a new vault with a new master password
- **In the future**: Write down your master password in a secure location (physical safe, password manager, etc.)

---

## 📁 File Structure

```
app_en.py              # Main application file (English version)
vault.dat              # Encrypted password vault (created after first use)
README.md              # This file
```

---

## 🔧 Advanced: Command Line (For Users)

You can also edit the `SALT` variable in the code for added security:

```python
SALT = b'your_custom_salt_here!'
```

However, if you change this after creating a vault, you won't be able to decrypt your existing passwords.

---

## ✉️ Support

If you encounter issues:
1. Check this troubleshooting section first
2. Verify all dependencies are installed
3. Try running the application again
4. Check your master password is correct

---

## 📄 License

This application is provided as-is for personal use.

---

**Last Updated**: April 2026  
**Version**: 1.0  
**Python Version**: 3.7+

---

## 🎯 Quick Start Checklist

- [ ] Python 3.7+ installed
- [ ] `cryptography` library installed (`pip install cryptography`)
- [ ] Run `python app_en.py`
- [ ] Create a strong master password
- [ ] Add your first password
- [ ] Test that you can logout and login again
- [ ] Backup your `vault.dat` file to a safe location
