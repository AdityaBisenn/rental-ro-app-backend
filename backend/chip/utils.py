from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import json

def encrypt_json(data, key):
    # Convert the JSON data to a string
    data_str = json.dumps(data)
    
    # Convert string to bytes
    data_bytes = data_str.encode('utf-8')
    
    # Generate a random IV
    iv = get_random_bytes(16)
    
    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad the data
    padded_data = pad(data_bytes, AES.block_size)
    
    # Encrypt the data
    ciphertext = cipher.encrypt(padded_data)
    
    # Encode the ciphertext and IV to base64 for easy transmission
    encrypted_data = base64.b64encode(iv + ciphertext).decode('utf-8')
    
    return encrypted_data


def decrypt_json(encrypted_data, key):
    # Decode the base64 encoded data
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    
    # Extract the IV and ciphertext
    iv = encrypted_data_bytes[:16]
    ciphertext = encrypted_data_bytes[16:]
    
    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt the data
    padded_data = cipher.decrypt(ciphertext)
    
    # Unpad the data
    data_bytes = unpad(padded_data, AES.block_size)
    
    # Convert bytes to string
    data_str = data_bytes.decode('utf-8')
    
    # Convert string to JSON
    data = json.loads(data_str)
    
    return data
