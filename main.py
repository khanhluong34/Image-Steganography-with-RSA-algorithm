import cv2  
import argparse
import os
from src.image_decoder import decode 
from src.image_encoder import encode  

class Control: 
    def __init__(self, filename, n_bits=2):
        self.filename = filename
        self.n_bits = n_bits

    def set_filename(self, filename):
        self.filename = filename
    def encrypt(self, text, output_path, public_key):
        _, file = os.path.split(self.filename)
        # split the filename and the image extension
        filename, ext = file.split(".")
        output_image = os.path.join(output_path, f"{filename}_encoded.{ext}")
        # encode the data into the image
        encoded_image = encode(image_name=self.filename, secret_data=text, public_key=public_key,n_bits=self.n_bits)
        
        # save the output image (encoded image)
        cv2.imwrite(output_image, encoded_image)

    def decrypt(self):
        print(self.filename)
        
        decoded_data = decode(self.filename, n_bits=self.n_bits)

        return decoded_data

        # if self.filename:
        #     # decode the secret data from the image and write it to file
        #     decoded_data = decode(input_image, n_bits=self.n_bits, in_bytes=True)
        #     with open(self.file, "wb") as f:
        #         f.write(decoded_data)
        #     print(f"[+] File decoded, {self.file} is saved successfully.")
        # else:
        #     # decode the secret data from the image and print it in the console
        #     decoded_data = decode(input_image, n_bits=self.n_bits)
        #     print("[+] Decoded data:", decoded_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Steganography encoder/decoder, this Python scripts encode data within images.")
    parser.add_argument("-t", "--text", help="The text data to encode into the image, this only should be specified for encoding", default="Luong Son Thang")
    parser.add_argument("-f", "--file", help="The file to hide into the image, this only should be specified while encoding")
    parser.add_argument("-e", "--encode", help="Encode the following image", default="images/input_images/bk.png")
    parser.add_argument("-d", "--decode", help="Decode the following image", default="images/output_images/bk_encoded.png")
    parser.add_argument("-b", "--n-bits", help="The number of least significant bits of the image to encode", type=int, default=2)
    # parse the args
    args = parser.parse_args()
    if args.encode != "0":
        # if the encode argument is specified
        if args.text:
            secret_data = args.text
        elif args.file:
            with open(args.file, "rb") as f:
                secret_data = f.read()
        input_image = args.encode
        # split the absolute path and the file
        _, file = os.path.split(input_image)
        # split the filename and the image extension
        filename, ext = file.split(".")
        output_image = os.path.join("./images/output_images/", f"{filename}_encoded.{ext}")
        # encode the data into the image
        encoded_image = encode(image_name=input_image,public_key="./src/rsa/public.key", secret_data=secret_data, n_bits=args.n_bits)
        # save the output image (encoded image)
        cv2.imwrite(output_image, encoded_image)
        print("[+] Saved encoded image.")
    if args.decode != "0":
        input_image = args.decode
        if args.file:
            # decode the secret data from the image and write it to file
            decoded_data = decode(input_image, private_key="./src/rsa/private.key", n_bits=args.n_bits, in_bytes=True)
            with open(args.file, "wb") as f:
                f.write(decoded_data)
            print(f"[+] File decoded, {args.file} is saved successfully.")
        else:
            # decode the secret data from the image and print it in the console
            decoded_data = decode(input_image, private_key="./src/rsa/private.key", n_bits=args.n_bits)
            print("[+] Decoded data:", decoded_data)