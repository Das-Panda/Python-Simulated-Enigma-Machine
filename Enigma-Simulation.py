import random

class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.initial_rotors = rotors
        self.rotors = list(rotors)
        self.reflector = reflector
        self.plugboard = plugboard
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def set_rotor_positions(self, positions):
        # Set the initial positions of the rotors
        for i in range(len(self.rotors)):
            position = positions[i]
            self.rotors[i] = self.initial_rotors[i][position:] + self.initial_rotors[i][:position]

    def rotate_rotors(self):
        # Rotate the rightmost rotor by one position
        # For simplicity, we're not implementing the full odometer-like stepping mechanism
        self.rotors[-1] = self.rotors[-1][1:] + self.rotors[-1][0]

    def plugboard_swap(self, char):
        # Swap letters based on the plugboard configuration
        if char in self.plugboard:
            return self.plugboard[char]
        return char

    def reflector_swap(self, char):
        # Reflect the character using the reflector configuration
        return self.reflector[self.alphabet.index(char)]

    def rotor_pass(self, char, reverse=False):
        # Pass the character through all rotors
        for rotor in reversed(self.rotors) if reverse else self.rotors:
            char = rotor[self.alphabet.index(char)] if not reverse else self.alphabet[rotor.index(char)]
        return char

    def encrypt_decrypt(self, text):
        encrypted_text = ''
        for char in text:
            if char in self.alphabet:
                char = self.plugboard_swap(char)
                char = self.rotor_pass(char)
                char = self.reflector_swap(char)
                char = self.rotor_pass(char, reverse=True)
                char = self.plugboard_swap(char)
                self.rotate_rotors()
            encrypted_text += char
        return encrypted_text

def generate_random_plugboard_swaps(num_swaps=10):
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    swaps = {}
    for _ in range(num_swaps):
        pair = random.sample(letters, 2)
        swaps[pair[0]] = pair[1]
        swaps[pair[1]] = pair[0]
        letters.remove(pair[0])
        letters.remove(pair[1])
    return swaps

# Example configuration
rotors = [
    'EKMFLGDQVZNTOWYHXUSPAIBRCJ',  # Rotor 1
    'AJDKSIRUXBLHWTMCQGZNPYFVOE',  # Rotor 2
    'BDFHJLCPRTXVZNYEIWGAKMUSQO'   # Rotor 3
]
reflector = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'  # Reflector

# User decides to use the plugboard and provides input or opt for random swaps
use_plugboard = True  # Example: user decides to use the plugboard
if use_plugboard:
    plugboard_swaps = generate_random_plugboard_swaps()
else:
    plugboard_swaps = {}

# Create an Enigma machine instance
enigma = EnigmaMachine(rotors, reflector, plugboard_swaps)

# Set initial rotor positions and encrypt a message
initial_positions = [0, 0, 0]  # Example initial positions for the rotors
plaintext = 'HELLOENIGMA'
enigma.set_rotor_positions(initial_positions)
ciphertext = enigma.encrypt_decrypt(plaintext)

# Output the encrypted message, rotor positions, and plugboard settings
print("Ciphertext:", ciphertext)
print("Rotor Positions:", initial_positions)
print("Plugboard Swaps:", plugboard_swaps)

# Decrypting the message (assuming the recipient sets the same initial configurations)
enigma.set_rotor_positions(initial_positions)
decrypted_text = enigma.encrypt_decrypt(ciphertext)
print("Decrypted text:", decrypted_text)
