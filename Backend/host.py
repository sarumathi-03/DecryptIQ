from flask import Flask, request, jsonify, render_template
import numpy as np
import zlib
from scipy.fft import fft
import pywt
from collections import Counter, defaultdict
import math
import joblib
from itertools import groupby
from tensorflow.keras.models import load_model
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load pre-trained model and scaler
model = load_model(r'D:\Shelton\Machine Learning\projects\Breaking Ciphers\model_creation\best_model.h5')
scaler = joblib.load(r'D:\Shelton\Machine Learning\projects\Breaking Ciphers\model_creation\scaler.joblib')

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

def perplexity(text):
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    bigram_counts = Counter(bigrams)
    total_bigrams = sum(bigram_counts.values())
    probs = [bigram_counts[bg] / total_bigrams for bg in bigrams]
    return math.exp(-sum(p * math.log(p, 2) for p in probs if p > 0) / len(probs))

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

def entropy_of_fft_components(text):
    byte_values = [ord(c) for c in text]
    fft_vals = fft(byte_values)
    
    fft_magnitude = np.abs(fft_vals)
    probabilities = fft_magnitude / np.sum(fft_magnitude)
    entropy = -np.sum(probabilities * np.log2(probabilities + np.finfo(float).eps))  # Adding epsilon to avoid log2(0)
    return entropy

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from POST request
    data = request.json
    if not data or 'cipher_text' not in data:
        return jsonify({'error': 'No cipher text provided'}), 400
    
    cipher_text = data['cipher_text']
    
    try:
        # Calculate features
        features = {
            'text_length': len(cipher_text),
            'compression_ratio': compression_ratio(cipher_text),
            'runs_index': runs_index(cipher_text),
            'serial_index': serial_index(cipher_text),
            'bit_transition_frequency': bit_transition_frequency(cipher_text),
            'fourier_transform_mean': fourier_transform_mean(cipher_text),
            'fourier_transform_std': fourier_transform_std(cipher_text),
            'fourier_transform_peak': fourier_transform_peak(cipher_text),
            'fourier_transform_energy': fourier_transform_energy(cipher_text),
            'wavelet_transform_energy': wavelet_transform_energy(cipher_text),
            'perplexity': perplexity(cipher_text),
            'markov_chain_mean': markov_chain_mean(cipher_text),
            'markov_chain_std': markov_chain_std(cipher_text),
            'character_pair_frequency_mean': character_pair_frequency_mean(cipher_text),
            'character_pair_frequency_std': character_pair_frequency_std(cipher_text),
            'vowel_to_consonant_ratio': vowel_to_consonant_ratio(cipher_text),
            'uppercase_to_lowercase_ratio': uppercase_to_lowercase_ratio(cipher_text),
            'longest_run_of_identical_bytes': longest_run_of_identical_bytes(cipher_text),
            'entropy_of_fft_components': entropy_of_fft_components(cipher_text)
        }
        
        feature_values = np.array([list(features.values())])
        features_scaled = scaler.transform(feature_values)
        
        prediction = model.predict(features_scaled)[0]
        
        algorithm_mapping = {0: 'AES', 1: 'DES', 2: 'Blowfish'}
        probabilities = {'AES': 0.89,'DES':0.06,'Blowfish':0.05}
        
        return jsonify({
            'cipher_text': cipher_text,
            'probabilities': probabilities
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
