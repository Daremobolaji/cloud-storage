import streamlit as st
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64
import io

# Generate or load RSA keys (for demo purpose; in prod, securely store/retrieve)
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# AES encryption
def encrypt_data(data, rsa_pub_key):
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    
    rsa_cipher = PKCS1_OAEP.new(RSA.import_key(rsa_pub_key))
    enc_aes_key = rsa_cipher.encrypt(aes_key)

    return {
        'enc_key': base64.b64encode(enc_aes_key).decode(),
        'nonce': base64.b64encode(cipher_aes.nonce).decode(),
        'tag': base64.b64encode(tag).decode(),
        'ciphertext': base64.b64encode(ciphertext).decode()
    }

# Decryption
def decrypt_data(enc_data, rsa_priv_key):
    rsa_cipher = PKCS1_OAEP.new(RSA.import_key(rsa_priv_key))
    aes_key = rsa_cipher.decrypt(base64.b64decode(enc_data['enc_key']))
    
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=base64.b64decode(enc_data['nonce']))
    plaintext = cipher_aes.decrypt_and_verify(
        base64.b64decode(enc_data['ciphertext']),
        base64.b64decode(enc_data['tag'])
    )
    return plaintext

# Streamlit UI
st.title("🔐 Secure Cloud Storage with AES & RSA")

text_input = st.text_area("Enter your sensitive text")
uploaded_file = st.file_uploader("Upload a file", type=['txt', 'pdf', 'docx'])

if st.button("Encrypt & Store"):
    if text_input:
        result = encrypt_data(text_input.encode(), public_key)
        st.success(result)
        st.success("Text encrypted and stored successfully!")

    if uploaded_file:
        file_data = uploaded_file.read()
        result = encrypt_data(file_data, public_key)
        st.success("File encrypted and stored successfully!")

# Simulate storage by session state
if 'stored_data' not in st.session_state:
    st.session_state['stored_data'] = result if 'result' in locals() else {}

if st.button("Decrypt & Show"):
    if st.session_state['stored_data']:
        decrypted = decrypt_data(st.session_state['stored_data'], private_key)
        st.text_area("Decrypted Output", decrypted.decode())
