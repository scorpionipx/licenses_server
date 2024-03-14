import datetime
import json
import random
import string

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding as asymetric_padding
from cryptography.hazmat.primitives.ciphers import modes, algorithms, Cipher


from licenses_server.utils.cryptor import PRIVATE_KEY_FILE_PATH, PUBLIC_KEY_FILE_PATH


# noinspection PyUnreachableCode
if False:
    from licenses.models import License  # fake import for type hint


def as_dict(entry, serializable=False):
    related_fields = [field for field in entry.meta.get_fields() if 'Rel' in f'{type(field)}']
    entry: License
    data = {}
    for key, value in entry.__dict__.items():
        if not key.startswith('_'):
            if serializable:
                if isinstance(value, datetime.date):
                    value = f'{value}'
                if isinstance(value, datetime.datetime):
                    value = f'{value}'
            data[key] = value
            if key.endswith('_id'):
                new_key = key.replace('_id', '')
                data[new_key] = f'{getattr(entry, new_key)}'
    for related_field in related_fields:
        data[related_field.name] = []
        for related_entry in getattr(entry, f'{related_field.name}').all():
            if hasattr(related_entry, 'as_dict'):
                if serializable:
                    related_entry_as_dict = related_entry.as_dict(serializable=True)
                else:
                    related_entry_as_dict = related_entry.as_dict
            else:
                related_entry_as_dict = {}
                for key, value in related_entry.__dict__.items():
                    if not key.startswith('_'):
                        if serializable:
                            if isinstance(value, datetime.date):
                                value = f'{value}'
                            if isinstance(value, datetime.datetime):
                                value = f'{value}'
                        related_entry_as_dict[key] = value

            data[related_field.name].append(related_entry_as_dict)

    return data


class Cryptor:
    """
    Cryptor
    """
    def __init__(self):
        # Convert from PEM format to DER format
        public_pem_bytes = PRIVATE_KEY_FILE_PATH.read_bytes()
        self._privateKey = serialization.load_pem_private_key(
            public_pem_bytes,
            password=None,
            backend=default_backend()
        )

    def decrypt(self, cipher_text):
        """
            Decrypt using RSA Private Key
        """
        plainText = self._privateKey.decrypt(
            cipher_text,
            asymetric_padding.OAEP(
                mgf=asymetric_padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            ))
        return plainText.decode("utf-8")

    def encrypt(self, plain_text, aes_key, init_vector):
        """
            Encrypt Using AES Client Key.
        """
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        plaintext_padded = padder.update(plain_text) + padder.finalize()

        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(init_vector), backend=default_backend())
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(plaintext_padded) + encryptor.finalize()

        # Return ciphertext as bytes
        return ciphertext

    def aes_decrypt(self, ciphertext, aes_key, init_vector):
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


def generate_serial_no(request, model):
    """
    generate_serial_no
    """
    letters = string.ascii_uppercase
    serial_no = ''.join(random.choice(letters) for _ in range(59)) + f'{model.objects.first().pk:05d}'

    return serial_no

