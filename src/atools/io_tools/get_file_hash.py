import hashlib


def get_file_hash(file_path):
    Hash = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            Hash.update(chunk)
    return Hash.hexdigest()
