import string
import typing as tp


def encrypt_english_letter_caesar(letter: str, shift: int) -> str:
    """
    Encrypts one english letter at a time using a Caesar cipher.
    """

    alphabet_start_pos = ord("A") if letter.isupper() else ord("a")
    alphabet_length = len(string.ascii_lowercase)

    return chr((ord(letter) + shift - alphabet_start_pos) % alphabet_length + alphabet_start_pos)


def decrypt_english_letter_caesar(letter: str, shift: int) -> str:
    """
    Encrypts one english letter at a time using a Caesar cipher.
    """

    alphabet_start_pos = ord("A") if letter.isupper() else ord("a")
    alphabet_length = len(string.ascii_lowercase)

    return chr((ord(letter) - shift - alphabet_start_pos) % alphabet_length + alphabet_start_pos)


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """

    ciphertext = ""
    alphabet = string.ascii_letters

    for letter in plaintext:
        if letter in alphabet:
            ciphertext += encrypt_english_letter_caesar(letter, shift)
        else:
            ciphertext += letter

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """

    plaintext = ""
    alphabet = string.ascii_letters

    for letter in ciphertext:
        if letter in alphabet:
            plaintext += decrypt_english_letter_caesar(letter, shift)
        else:
            plaintext += letter

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
