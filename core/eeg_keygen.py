import hashlib
import os
import base64

def generate_eeg_key(eeg_sample: bytes, salt: bytes = None, iterations: int = 100_000) -> bytes:
    """
    Derives a strong encryption key from EEG signal sample using PBKDF2-HMAC-SHA512.
    
    Args:
        eeg_sample (bytes): Raw or preprocessed EEG data (simulated or from a headset).
        salt (bytes): Optional salt. If not provided, a new one will be generated.
        iterations (int): Number of iterations for PBKDF2.

    Returns:
        Tuple of (key, salt) - 256-bit encryption key (32 bytes) and the salt used.
    """
    if salt is None:
        salt = os.urandom(16)

    key = hashlib.pbkdf2_hmac(
        'sha512',
        eeg_sample,
        salt,
        iterations,
        dklen=32  # AES-256 requires 32-byte key
    )
    return key, salt
if __name__ == "__main__":
    fake_eeg = b"simulated-brainwave-pattern"
    key, salt = generate_eeg_key(fake_eeg)
    print("Generated Key:", base64.urlsafe_b64encode(key).decode())
    print("Salt:", base64.urlsafe_b64encode(salt).decode())
