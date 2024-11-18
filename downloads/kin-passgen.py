import random
import string

def generate_password(length=12, use_lowercase=True, use_uppercase=True, use_numbers=True, use_special_chars=True):
    # Define character sets based on user selection
    lower_case = string.ascii_lowercase if use_lowercase else ""
    upper_case = string.ascii_uppercase if use_uppercase else ""
    digits = string.digits if use_numbers else ""
    special_chars = string.punctuation if use_special_chars else ""
    
    # Combine all selected character sets
    all_chars = lower_case + upper_case + digits + special_chars
    
    if not all_chars:
        raise ValueError("At least one character set must be selected.")
    
    # Generate the password
    password = ''.join(random.choice(all_chars) for _ in range(length))
    return password

# Main function for password generation
if __name__ == "__main__":
    num_passwords = int(input("How many passwords would you like to generate? "))
    length = int(input("Enter password length: "))
    
    # Choose which character sets to include
    use_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
    use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_numbers = input("Include numbers? (y/n): ").lower() == 'y'
    use_special_chars = input("Include special characters? (y/n): ").lower() == 'y'

    batch_size = 10000  # Size of each batch to generate
    total_generated = 0
    generated_passwords = set()  # Set to store unique passwords

    # Open the file to write passwords
    with open('passwords.txt', 'w') as file:
        while total_generated < num_passwords:
            batch = set()  # Set to store a batch of generated passwords
            
            # Generate a batch of passwords
            for _ in range(batch_size):
                password = generate_password(length, use_lowercase, use_uppercase, use_numbers, use_special_chars)
                batch.add(password)
            
            # Add new unique passwords from the batch to the main set
            new_unique_passwords = batch - generated_passwords
            generated_passwords.update(new_unique_passwords)
            
            # Write the new unique passwords to the file
            for password in new_unique_passwords:
                file.write(password + '\n')
            
            # Update the total number of generated unique passwords
            total_generated += len(new_unique_passwords)

            # Clear (delete) the batch to free up memory
            batch.clear()  # This deletes the passwords in the current batch from memory

    print(f"{total_generated} unique passwords have been generated and saved to 'passwords.txt'.")
