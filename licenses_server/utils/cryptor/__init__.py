import pathlib


KEYS_DIR = pathlib.Path(__file__).parent.joinpath('keys')

PRIVATE_KEY_FILE_PATH = KEYS_DIR.joinpath('private.pem')
PUBLIC_KEY_FILE_PATH = KEYS_DIR.joinpath('public.pem')
