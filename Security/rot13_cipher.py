import string
import codecs

# Rot13 Cipher: Rotate by 13 places

def rot13_translator() -> dict:
    lowercase: str = string.ascii_lowercase
    uppercase: str = string.ascii_uppercase

    shift: int = 13

    shift_lowercase: str = lowercase[shift:] + lowercase[:shift]
    shift_uppercase: str = uppercase[shift:] + uppercase[:shift]

    translator: dict = str.maketrans(lowercase+uppercase,
                                     shift_lowercase+shift_uppercase)
    
    return translator


def rot13(message: str) -> str:
    table: dict = rot13_translator()
    return message.translate(table)


def main() -> None:
    user_input: str = input("Your message: ")

    encrypted_message: str = rot13(user_input)
    print(f'Encrypted Message: {encrypted_message}')

    decrypted_message: str = rot13(encrypted_message)
    print(f'Decrypted Message: {decrypted_message}')

    encoded: str = codecs.encode(user_input, 'rot13')
    print(encoded)

    decoded: str = codecs.decode(encoded, 'rot13')
    print(decoded)


if __name__ == "__main__":
    main()