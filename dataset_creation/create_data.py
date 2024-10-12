import numpy as np
import pandas as pd
import random
import string
import math
import zlib
from scipy.stats import entropy, kurtosis, skew
from collections import Counter, defaultdict
from itertools import groupby
from scipy.fftpack import fft
import pywt
from Crypto.Cipher import Blowfish, AES, DES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import base64

# Helper functions
def generate_random_text(length=100):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

def shannon_entropy(text):
    prob = [float(text.count(c)) / len(text) for c in set(text)]
    return -sum(p * np.log2(p) for p in prob)

def length_mod_block_size(text, block_size=16):
    return len(text) % block_size

def compression_ratio(text):
    compressed = zlib.compress(text.encode('utf-8'))
    return len(compressed) / len(text.encode('utf-8'))

def runs_index(text):
    return len([sum(1 for _ in group) for _, group in groupby(text)])

def serial_index(text):
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    return len(set(bigrams))


def bit_transition_frequency(text):
    bits = ''.join(format(byte, '08b') for byte in text.encode('utf-8'))
    return sum(bits[i] != bits[i-1] for i in range(1, len(bits)))

def run_length_encoding(text):
    return sum(1 for _ in groupby(text))

def fourier_transform_mean(text):
    byte_values = [ord(c) for c in text]
    fft_vals = fft(byte_values)
    return np.mean(np.abs(fft_vals))

def fourier_transform_std(text):
    byte_values = [ord(c) for c in text]
    fft_vals = fft(byte_values)
    return np.std(np.abs(fft_vals))

def fourier_transform_peak(text):
    byte_values = [ord(c) for c in text]
    fft_vals = fft(byte_values)
    return np.max(np.abs(fft_vals))

def fourier_transform_energy(text):
    byte_values = [ord(c) for c in text]
    fft_vals = fft(byte_values)
    return np.sum(np.square(np.abs(fft_vals)))

def wavelet_transform_mean(text):
    byte_values = np.array([ord(c) for c in text])
    coeffs = pywt.dwt(byte_values, 'haar')
    return np.mean(coeffs[0])

def wavelet_transform_std(text):
    byte_values = np.array([ord(c) for c in text])
    coeffs = pywt.dwt(byte_values, 'haar')
    return np.std(coeffs[0])

def wavelet_transform_peak(text):
    byte_values = np.array([ord(c) for c in text])
    coeffs = pywt.dwt(byte_values, 'haar')
    return np.max(coeffs[0])

def wavelet_transform_energy(text):
    byte_values = np.array([ord(c) for c in text])
    coeffs = pywt.dwt(byte_values, 'haar')
    return np.sum(np.square(coeffs[0]))

def xor_with_constant(text, constant=0xFF):
    return ''.join(chr(ord(c) ^ constant) for c in text)

def perplexity(text):
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    bigram_counts = Counter(bigrams)
    total_bigrams = sum(bigram_counts.values())
    probs = [bigram_counts[bg] / total_bigrams for bg in bigrams]
    return math.exp(-sum(p * math.log(p, 2) for p in probs if p > 0) / len(probs))

def burstiness(text):
    counts = Counter(text)
    inter_arrival_times = [1 / counts[c] for c in text]
    mean_inter_arrival = np.mean(inter_arrival_times)
    std_inter_arrival = np.std(inter_arrival_times)
    return std_inter_arrival / mean_inter_arrival if mean_inter_arrival else 0

def markov_chain_mean(text):
    transitions = defaultdict(lambda: defaultdict(int))
    for i in range(len(text) - 1):
        transitions[text[i]][text[i+1]] += 1
    for current_char, next_chars in transitions.items():
        total = sum(next_chars.values())
        for char in next_chars:
            transitions[current_char][char] /= total
    return np.mean([transitions[c1].get(c2, 0) for c1 in sorted(transitions) for c2 in sorted(transitions)])

def markov_chain_std(text):
    transitions = defaultdict(lambda: defaultdict(int))
    for i in range(len(text) - 1):
        transitions[text[i]][text[i+1]] += 1
    for current_char, next_chars in transitions.items():
        total = sum(next_chars.values())
        for char in next_chars:
            transitions[current_char][char] /= total
    return np.std([transitions[c1].get(c2, 0) for c1 in sorted(transitions) for c2 in sorted(transitions)])

def markov_chain_peak(text):
    transitions = defaultdict(lambda: defaultdict(int))
    for i in range(len(text) - 1):
        transitions[text[i]][text[i+1]] += 1
    for current_char, next_chars in transitions.items():
        total = sum(next_chars.values())
        for char in next_chars:
            transitions[current_char][char] /= total
    return np.max([transitions[c1].get(c2, 0) for c1 in sorted(transitions) for c2 in sorted(transitions)])

def character_pair_frequency_mean(text):
    pairs = [text[i:i+2] for i in range(len(text)-1)]
    return np.mean([pairs.count(pair) for pair in set(pairs)])

def character_pair_frequency_std(text):
    pairs = [text[i:i+2] for i in range(len(text)-1)]
    return np.std([pairs.count(pair) for pair in set(pairs)])

def character_pair_frequency_peak(text):
    pairs = [text[i:i+2] for i in range(len(text)-1)]
    return np.max([pairs.count(pair) for pair in set(pairs)])

def vowel_to_consonant_ratio(text):
    vowels = 'aeiou'
    vowel_count = sum(1 for c in text.lower() if c in vowels)
    consonant_count = sum(1 for c in text.lower() if c.isalpha() and c not in vowels)
    return vowel_count / consonant_count if consonant_count else 0

def uppercase_to_lowercase_ratio(text):
    uppercase_count = sum(1 for c in text if c.isupper())
    lowercase_count = sum(1 for c in text if c.islower())
    return uppercase_count / lowercase_count if lowercase_count else 0

def unique_character_count(text):
    return len(set(text))

def longest_repeated_sequence(text):
    longest_seq = ''
    for i in range(len(text)):
        for j in range(i + 1, len(text) + 1):
            seq = text[i:j]
            if seq in text[j:]:
                if len(seq) > len(longest_seq):
                    longest_seq = seq
    return len(longest_seq)

def longest_run_of_identical_bytes(text):
    longest_run = 0
    current_run = 1
    for i in range(1, len(text)):
        if text[i] == text[i-1]:
            current_run += 1
        else:
            longest_run = max(longest_run, current_run)
            current_run = 1
    return max(longest_run, current_run)

def repeated_pattern_count(text):
    patterns = [text[i:i+2] for i in range(len(text)-1)]
    return len([pattern for pattern in set(patterns) if patterns.count(pattern) > 1])

def variance_of_byte_values(text):
    byte_values = [ord(c) for c in text]
    return np.var(byte_values)

def skewness_and_kurtosis(text):
    byte_values = [ord(c) for c in text]
    return skew(byte_values), kurtosis(byte_values)

def entropy_of_fft_components(text):
    byte_values = [ord(c) for c in text]
    fft_vals = fft(byte_values)
    return entropy(np.abs(fft_vals))


def encrypt_aes(text):
    key = get_random_bytes(16) 
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(text.encode(), AES.block_size)
    encrypted = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted).decode()

def encrypt_des(text):
    key = get_random_bytes(8) 
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = pad(text.encode(), DES.block_size)
    encrypted = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted).decode()

def encrypt_blowfish(text):
    key = get_random_bytes(16)  
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    padded_text = pad(text.encode(), Blowfish.block_size)
    encrypted = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted).decode()


texts = [generate_random_text() for _ in range(500)]  # Generate 100 random texts
data = []

for text in texts:
    byte_values = [ord(c) for c in text]
    for encrypt_func, algo_name in [(encrypt_aes, 'AES'), (encrypt_des, 'DES'), (encrypt_blowfish, 'Blowfish')]:
        Etext = encrypt_func(text)

        features = {
            'text_length': len(Etext),
            # 'shannon_entropy': shannon_entropy(Etext),
            'compression_ratio': compression_ratio(Etext),
            'runs_index': runs_index(Etext),
            'serial_index': serial_index(Etext),
            'bit_transition_frequency': bit_transition_frequency(Etext),
            'fourier_transform_mean': fourier_transform_mean(Etext),
            'fourier_transform_std': fourier_transform_std(Etext),
            'fourier_transform_peak': fourier_transform_peak(Etext),
            'fourier_transform_energy': fourier_transform_energy(Etext),
            # 'wavelet_transform_mean': wavelet_transform_mean(Etext),
            # 'wavelet_transform_std': wavelet_transform_std(Etext),
            # 'wavelet_transform_peak': wavelet_transform_peak(Etext),
            'wavelet_transform_energy': wavelet_transform_energy(Etext),
            'perplexity': perplexity(Etext),
            # 'burstiness': burstiness(Etext),
            'markov_chain_mean': markov_chain_mean(Etext),
            'markov_chain_std': markov_chain_std(Etext),
            # 'markov_chain_peak': markov_chain_peak(Etext),
            'character_pair_frequency_mean': character_pair_frequency_mean(Etext),
            'character_pair_frequency_std': character_pair_frequency_std(Etext),
            # 'character_pair_frequency_peak': character_pair_frequency_peak(Etext),
            'vowel_to_consonant_ratio': vowel_to_consonant_ratio(Etext),
            'uppercase_to_lowercase_ratio': uppercase_to_lowercase_ratio(Etext),
            # 'unique_character_count': unique_character_count(Etext),
            # 'longest_repeated_sequence': longest_repeated_sequence(Etext),
            'longest_run_of_identical_bytes': longest_run_of_identical_bytes(Etext),
            # 'repeated_pattern_count': repeated_pattern_count(Etext),
            # 'variance_of_byte_values': variance_of_byte_values(Etext),
            # 'skewness': skewness_and_kurtosis(Etext)[0],
            # 'kurtosis': skewness_and_kurtosis(Etext)[1],
            'entropy_of_fft_components': entropy_of_fft_components(Etext),
            'algorithm': algo_name
        }
        data.append(features)
        

df = pd.DataFrame(data)
cols = [col for col in df.columns if col != 'algorithm'] + ['algorithm']
data_df = df[cols]

df.to_csv('dataset.csv', index=False)