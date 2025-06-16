import hashlib

def sha256_checksum(file_path):
    """Generate SHA-256 hash of the file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

if __name__ == "__main__":
    original = "c:/Users/Tejas/Desktop/Bat-Man/core/test.encrypted"
    recovered = "c:/Users/Tejas/Desktop/Bat-Man/core/recovered.encrypted"

    original_hash = sha256_checksum(original)
    recovered_hash = sha256_checksum(recovered)

    print(f"[Original]  {original_hash}")
    print(f"[Recovered] {recovered_hash}")

    if original_hash == recovered_hash:
        print("[+] Integrity verified: Files are identical.")
    else:
        print("[-] Integrity failed: Files differ.")
