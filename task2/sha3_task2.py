import hashlib
import os
import sys

def sorting_key(hexdigit):
    product = 1
    for ch in hexdigit:
        digit = int(ch, 16)
        product *= (digit + 1)
    return product

def compute_hashes_from_folder(folder_path):
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f'Folder not found: {folder_path}')

    hashes = []

    for filename in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)

        if not os.path.isfile(file_path):
            continue

        with open(file_path, 'rb') as f:
            data = f.read()
            file_hash = hashlib.sha3_256(data).hexdigest()
            hashes.append(file_hash)

    return hashes

def main():
    # --- Getting folder path from CLI or user input ---
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = input('Enter folder path containing files: ').strip()

    # Step 1 & 2
    hashes = compute_hashes_from_folder(folder)

    # Step 3
    hashes.sort(key=sorting_key)

    # --- Ask for email (task requirement) ---
    email = input("Enter your email: ").strip().lower()

    # Step 4 & 5
    combined = "".join(hashes) + email

    # step 6
    final_hash = hashlib.sha3_256(combined.encode()).hexdigest()

    print("\nFinal SHA3-256:", final_hash)


if __name__ == '__main__':
    main()
