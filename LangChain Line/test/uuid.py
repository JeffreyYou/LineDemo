import hashlib

def generate_id_from_phone(phone_number):
    # Encode the phone number to a bytes-like object
    encoded_phone = phone_number.encode()
    
    # Create a SHA256 hash object
    hash_object = hashlib.sha256(encoded_phone)
    
    # Get the hexadecimal representation of the hash
    phone_hash = hash_object.hexdigest()

    return phone_hash

# Example usage
phone_number = "1234567890"
unique_id = generate_id_from_phone(phone_number)
print(unique_id)
