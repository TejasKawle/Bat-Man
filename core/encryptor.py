from cryptography.fernet import Fernet, InvalidToken
import base64
import os

def create_fernet_key(raw_key: bytes) -> bytes:
    """Create a Fernet-compatible key from raw 32-byte AES key."""
    return base64.urlsafe_b64encode(raw_key)

def encrypt_file(input_path: str, output_path: str, key: bytes):
    """Encrypts a file using Fernet with the provided EEG-derived key."""
    try:
        with open(input_path, 'rb') as file:
            data = file.read()
        fernet = Fernet(create_fernet_key(key))
        encrypted = fernet.encrypt(data)
        with open(output_path, 'wb') as file:
            file.write(encrypted)
        print(f"[+] Encrypted '{input_path}' -> '{output_path}'")
    except FileNotFoundError:
        print(f"[!] File not found: {input_path}")
    except Exception as e:
        print(f"[!] Encryption failed: {e}")

def decrypt_file(encrypted_path: str, output_path: str, key: bytes):
    """Decrypts a file using Fernet with the provided EEG-derived key."""
    try:
        with open(encrypted_path, 'rb') as file:
            encrypted_data = file.read()
        fernet = Fernet(create_fernet_key(key))
        decrypted = fernet.decrypt(encrypted_data)
        with open(output_path, 'wb') as file:
            file.write(decrypted)
        print(f"[+] Decrypted '{encrypted_path}' -> '{output_path}'")
    except FileNotFoundError:
        print(f"[!] File not found: {encrypted_path}")
    except InvalidToken:
        print("[!] Invalid decryption key or corrupted data.")
    except Exception as e:
        print(f"[!] Decryption failed: {e}")

# Test block
if __name__ == "__main__":
    from eeg_keygen import generate_eeg_key

    # Simulate EEG input
    eeg = b"my-brainwave"
    key, salt = generate_eeg_key(eeg)

    # File paths
    input_file = "c:/Users/Tejas/Desktop/Bat-Man/core/test.txt"
    encrypted_file = "c:/Users/Tejas/Desktop/Bat-Man/core/test.encrypted"
    decrypted_file = "c:/Users/Tejas/Desktop/Bat-Man/core/test.decrypted.txt"

    # Run encryption and decryption
    encrypt_file(input_file, encrypted_file, key)
    decrypt_file(encrypted_file, decrypted_file, key)

    print("[OK] Encryption/Decryption complete.")
