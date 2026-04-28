# Protect-your-passwords
## ⚠️ Security Warning

This application stores your passwords locally and utilizes **AES encryption**.  
However, the following precautions should be taken:

* **Weak Master Passwords:** If your master password is not strong enough (e.g., `123456`), it can be cracked via **brute-force** attacks.
* **File Access:** The saved `kasa.dat` file should not be accessible to other users.
* **Limited Features:** This tool **does not back up passwords over a network** and does not provide **multi-factor authentication (MFA)**.
* **High-Security Use Cases:** For situations requiring high security (such as banking or critical systems), prefer **hardware-based** password vaults.

> Nevertheless, this simple structure provides a moderate level of protection for personal use.
