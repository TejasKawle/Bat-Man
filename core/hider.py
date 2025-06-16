from PIL import Image
import os

def _int_to_bin(rgb):
    return [format(channel, '08b') for channel in rgb]

def _bin_to_int(bin_rgb):
    return tuple(int(b, 2) for b in bin_rgb)

def encode_image(input_image_path, data_path, output_image_path):
    with open(data_path, 'rb') as f:
        data = f.read()
    data += b'###'  # Delimiter

    img = Image.open(input_image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = list(img.getdata())

    binary_data = ''.join(format(byte, '08b') for byte in data)
    data_len = len(binary_data)

    if data_len > len(pixels) * 3:
        raise ValueError("Data is too large to hide in this image.")

    encoded_pixels = []
    data_index = 0
    for pixel in pixels:
        r_bin, g_bin, b_bin = _int_to_bin(pixel)
        if data_index < data_len:
            r_bin = r_bin[:-1] + binary_data[data_index]
            data_index += 1
        if data_index < data_len:
            g_bin = g_bin[:-1] + binary_data[data_index]
            data_index += 1
        if data_index < data_len:
            b_bin = b_bin[:-1] + binary_data[data_index]
            data_index += 1
        encoded_pixels.append(_bin_to_int([r_bin, g_bin, b_bin]))

    img.putdata(encoded_pixels + pixels[len(encoded_pixels):])
    img.save(output_image_path)
    print(f"[+] Data encoded into image: {output_image_path}")

def decode_image(image_path, output_data_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_data = ""
    for pixel in pixels:
        for channel in _int_to_bin(pixel):
            binary_data += channel[-1]

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    extracted_data = bytearray()
    for byte in all_bytes:
        extracted_data.append(int(byte, 2))
        if extracted_data[-3:] == b'###':
            extracted_data = extracted_data[:-3]
            break

    with open(output_data_path, 'wb') as f:
        f.write(extracted_data)
    print(f"[+] Hidden data extracted to: {output_data_path}")

if __name__ == "__main__":
    print("[*] Starting steganography...")

    cover_image = "c:/Users/Tejas/Desktop/Bat-Man/core/batman.jpg"
    data_file = "c:/Users/Tejas/Desktop/Bat-Man/core/test.encrypted"
    stego_image = "c:/Users/Tejas/Desktop/Bat-Man/core/stego_image.png"
    recovered_file = "c:/Users/Tejas/Desktop/Bat-Man/core/recovered.encrypted"

    if not os.path.exists(cover_image):
        print(f"[!] Cover image not found: {cover_image}")
    elif not os.path.exists(data_file):
        print(f"[!] Data file to hide not found: {data_file}")
    else:
        try:
            print("[*] Encoding...")
            encode_image(cover_image, data_file, stego_image)

            print("[*] Decoding...")
            decode_image(stego_image, recovered_file)

            print("[+] Done.")
        except Exception as e:
            print(f"[!] Error: {e}")
