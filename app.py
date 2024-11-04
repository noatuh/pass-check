import time

# Custom exceptions
class RepeatedPasswordError(Exception):
    pass

class WeakPasswordError(Exception):
    pass

class InvalidStructureError(Exception):
    pass

# List of common weak passwords for validation
COMMON_PASSWORDS = ["password", "123456", "admin", "password123", "admin!", "letmein"]

def validate_password(password, previous_attempts):
    # Structural validation
    if len(password) < 10 or not any(char in "!@#$%^&*" for char in password) or " " in password:
        raise InvalidStructureError("Password must be at least 10 characters, contain a special character, and have no spaces.")

    # Weak password check
    if password.lower() in COMMON_PASSWORDS or any(pattern in password.lower() for pattern in ["password123", "admin!"]):
        raise WeakPasswordError("Password is too weak or commonly used. Please choose a more secure password.")

    # Repeated password check
    if password in previous_attempts:
        raise RepeatedPasswordError("This password has already been attempted and is invalid. Try a new password.")

def main():
    previous_attempts = []
    attempt_count = 0
    lockout_time = 5

    while attempt_count < 5:
        password = input("Enter a password: ")
        
        try:
            validate_password(password, previous_attempts)
            print("Password is valid and secure.")
            break  # Exit loop if password is valid

        except InvalidStructureError as e:
            print(f"Invalid Structure Error: {e}")
            previous_attempts.append(password)
            attempt_count += 1

        except WeakPasswordError as e:
            print(f"Weak Password Error: {e}")
            previous_attempts.append(password)
            attempt_count += 1

        except RepeatedPasswordError as e:
            print(f"Repeated Password Error: {e}")
            attempt_count += 1

        else:
            print("Password validation passed all checks.")

        finally:
            # Check for lockout after 3 failed attempts
            if attempt_count % 3 == 0 and attempt_count != 0:
                print(f"Too many invalid attempts. Locking out for {lockout_time} seconds.")
                time.sleep(lockout_time)

    if attempt_count >= 5:
        print("Too many failed attempts. Please try again later.")

if __name__ == "__main__":
    main()
