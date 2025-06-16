import os

def fragment_file(input_path, output_dir, chunk_size=1024):
    """
    Splits a file into smaller fragments of fixed size.

    Args:
        input_path (str): Path to the file to be fragmented.
        output_dir (str): Directory to store the fragments.
        chunk_size (int): Size of each fragment in bytes.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_path, 'rb') as f:
        index = 0
        while chunk := f.read(chunk_size):
            fragment_path = os.path.join(output_dir, f"fragment_{index}")
            with open(fragment_path, 'wb') as frag:
                frag.write(chunk)
            index += 1

    print(f"[+] Fragmented '{input_path}' into {index} parts in '{output_dir}'.")


def rebuild_file(fragments_dir, output_path):
    """
    Reconstructs the original file from fragments in order.

    Args:
        fragments_dir (str): Directory containing fragment files.
        output_path (str): Output file path to write the combined data.
    """
    fragments = sorted(os.listdir(fragments_dir), key=lambda x: int(x.split('_')[1]))

    with open(output_path, 'wb') as out_file:
        for fragment in fragments:
            fragment_path = os.path.join(fragments_dir, fragment)
            with open(fragment_path, 'rb') as frag:
                out_file.write(frag.read())

    print(f"[+] Rebuilt file as '{output_path}' from {len(fragments)} fragments.")


# Test block
if __name__ == "__main__":
    encrypted_file = "c:/Users/Tejas/Desktop/Bat-Man/core/test.encrypted"
    fragments_folder = "c:/Users/Tejas/Desktop/Bat-Man/core/fragments"
    rebuilt_file = "c:/Users/Tejas/Desktop/Bat-Man/core/rebuilt.encrypted"

    fragment_file(encrypted_file, fragments_folder)
    rebuild_file(fragments_folder, rebuilt_file)
