import json

import requests
import pathlib


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import padding as asymetric_padding
from cryptography.hazmat.primitives.ciphers import modes, algorithms, Cipher


def aes_decrypt(ciphertext, aes_key, init_vector):
    # Ensure key is 16, 24, or 32 bytes long (for AES-128, AES-192, or AES-256)
    if len(aes_key) not in {16, 24, 32}:
        raise ValueError("AES key must be 16, 24, or 32 bytes long")

    # Create a cipher object with the specified key and IV
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(init_vector), backend=default_backend())

    # Create a decryptor object
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove PKCS7 padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted


def get_license():
    """

    """
    url = 'http://localhost:6969/licenses/get/'
    payload = {
        'AESKey': '08fa994993833d9352fa9b7225da65ab',
        'SerialNo': 'DAFQEFIQEMFQ349',
        'InitVector': '4778a8d6a5d8a890f68cc9dd39c88375',
    }

    response = requests.post(
        url=url,
        json=payload,
    )
    if response.status_code != 200:
        print(response.content)
        return

    print(response.content)

    decrypted = aes_decrypt(
        ciphertext=response.content,
        aes_key=bytes.fromhex(payload['AESKey']),
        init_vector=bytes.fromhex(payload['InitVector']),
    )
    print(decrypted)

    entry_data = json.loads(decrypted.decode('utf-8'))
    print(entry_data)


if __name__ == '__main__':
    get_license()
