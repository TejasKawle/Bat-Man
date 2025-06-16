import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
import os
from PIL import Image

def _int_to_bin(rgb):
    return [format(channel, '08b') for channel in rgb]

def _bin_to_int(bin_rgb):
    return tuple(int(b, 2) for b in bin_rgb)

def encode_image(input_image_path, data_path, output_image_path):
    with open(data_path, 'rb') as f:
        data = f.read()
    data += b'###'

    img = Image.open(input_image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = list(img.getdata())

    binary_data = ''.join(format(byte, '08b') for byte in data)
    data_len = len(binary_data)
    if data_len > len(pixels) * 3:
        raise ValueError("Data too large to hide in image.")

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
    encoded_pixels += pixels[len(encoded_pixels):]

    img.putdata(encoded_pixels)
    img.save(output_image_path)

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

class StegoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steganography Tool")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()

        self.status = QLabel("Choose an operation")
        self.status.setAlignment(Qt.AlignCenter)

        self.encode_btn = QPushButton("Encode File in Image")
        self.encode_btn.clicked.connect(self.encode_data)

        self.decode_btn = QPushButton("Decode File from Image")
        self.decode_btn.clicked.connect(self.decode_data)

        layout.addWidget(self.status)
        layout.addWidget(self.encode_btn)
        layout.addWidget(self.decode_btn)
        self.setLayout(layout)

    def encode_data(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Select Image")
        data_path, _ = QFileDialog.getOpenFileName(self, "Select File to Hide")
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Stego Image", filter="PNG Files (*.png)")

        if image_path and data_path and output_path:
            try:
                encode_image(image_path, data_path, output_path)
                QMessageBox.information(self, "Success", "Data encoded successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def decode_data(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Select Stego Image")
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Extracted File")

        if image_path and output_path:
            try:
                decode_image(image_path, output_path)
                QMessageBox.information(self, "Success", "Data extracted successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StegoApp()
    window.show()
    sys.exit(app.exec_())
