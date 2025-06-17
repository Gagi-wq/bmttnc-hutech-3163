from flask import Flask, render_template, request, jsonify
import requests
import os
import logging

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Khởi tạo Flask với thư mục template rõ ràng
app = Flask(__name__, template_folder='templates')

# Router for home page
@app.route("/")
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Template error: {str(e)}")
        return jsonify({"error": f"Template error: {str(e)}"}), 500

# Routes to open PyQt5 forms via cipher_launcher
@app.route("/open-cipher/<cipher>")
def open_cipher(cipher):
    try:
        logger.info(f"Sending request to http://localhost:5001/{cipher}")
        response = requests.get(f"http://localhost:5001/{cipher}", timeout=5)
        logger.info(f"Received response: {response.status_code} - {response.text}")
        if response.status_code == 200 and "Success" in response.text:
            return jsonify({"message": f"Opening {cipher} form successfully"}), 200
        else:
            return jsonify({"error": f"Failed to open {cipher}: {response.text}"}), 500
    except requests.RequestException as e:
        logger.error(f"Error connecting to launcher: {str(e)}")
        return jsonify({"error": f"Error connecting to launcher: {str(e)}"}), 500

# Routes for Caesar Cipher
@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    from cipher.caesar.caesar_cipher import CaesarCipher
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    caesar = CaesarCipher()
    encrypted_text = caesar.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    from cipher.caesar.caesar_cipher import CaesarCipher
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    caesar = CaesarCipher()
    decrypted_text = caesar.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# Routes for Vigenère Cipher
@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    from cipher.vigenere.vigenere_cipher import VigenereCipher
    text = request.form['plain_text']
    key = request.form['key']
    vigenere = VigenereCipher()
    encrypted_text = vigenere.vigenere_encrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    from cipher.vigenere.vigenere_cipher import VigenereCipher
    text = request.form['cipher_text']
    key = request.form['key']
    vigenere = VigenereCipher()
    decrypted_text = vigenere.vigenere_decrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# Routes for Rail Fence Cipher
@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    from cipher.railfence.railfence_cipher import RailFenceCipher
    text = request.form['plain_text']
    rails = int(request.form['rails'])
    railfence = RailFenceCipher()
    encrypted_text = railfence.rail_fence_encrypt(text, rails)
    return f"text: {text}<br/>rails: {rails}<br/>encrypted text: {encrypted_text}"

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    from cipher.railfence.railfence_cipher import RailFenceCipher
    text = request.form['cipher_text']
    rails = int(request.form['rails'])
    railfence = RailFenceCipher()
    decrypted_text = railfence.rail_fence_decrypt(text, rails)
    return f"text: {text}<br/>rails: {rails}<br/>decrypted text: {decrypted_text}"

# Routes for Playfair Cipher
@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    from cipher.playfair.playfair_cipher import PlayfairCipher
    text = request.form['plain_text']
    key = request.form['key']
    playfair = PlayfairCipher()
    matrix = playfair.create_playfair_matrix(key)
    encrypted_text = playfair.playfair_encrypt(text, matrix)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    from cipher.playfair.playfair_cipher import PlayfairCipher
    text = request.form['cipher_text']
    key = request.form['key']
    playfair = PlayfairCipher()
    matrix = playfair.create_playfair_matrix(key)
    decrypted_text = playfair.playfair_decrypt(text, matrix)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)