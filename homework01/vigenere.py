import string
from caesar import encrypt_english_letter_caesar, decrypt_english_letter_caesar


def encrypt_english_letter_vigenere(letter: str, keyword: str, index: int) -> str:
    """
    Encrypts one english letter at a time using a Vigenere cipher.
    """

    alphabet_start_pos = ord("A") if letter.isupper() else ord("a")

    shift = ord(keyword[index % len(keyword)]) - alphabet_start_pos

    return encrypt_english_letter_caesar(letter, shift=shift)


def decrypt_english_letter_vigenere(letter: string, keyword: str, index: int) -> str:
    """
    Encrypts one english letter at a time using a Vigenere cipher.
    """

    alphabet_start_pos = ord("A") if letter.isupper() else ord("a")

    shift = ord(keyword[index % len(keyword)]) - alphabet_start_pos

    return decrypt_english_letter_caesar(letter, shift=shift)


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """

    ciphertext = ""
    alphabet = string.ascii_letters

    for ind, letter in enumerate(plaintext):
        if letter in alphabet:
            ciphertext += encrypt_english_letter_vigenere(letter, keyword, ind)
        else:
            ciphertext += letter

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """

    plaintext = ""
    alphabet = string.ascii_letters

    for ind, letter in enumerate(ciphertext):
        if letter in alphabet:
            plaintext += decrypt_english_letter_vigenere(letter, keyword, ind)
        else:
            plaintext += letter

    return plaintext
