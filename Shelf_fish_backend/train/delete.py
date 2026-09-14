import hashlib
import os

def file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
        return hasher.hexdigest()

def delete_duplicate(folder_path):
    hashes = {}
    deleted = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            hash = file_hash(file_path)

            if hash in hashes:
                print(f"Duplicate found: {file_path} (duplicate of {hashes[hash]})")

                os.remove(file_path)
                deleted +=1
            else:
                hashes[hash] = file_path
    print(f"Total duplicates found: {deleted}")



if __name__ == "__main__":
    folder = "images"
    delete_duplicate(folder)