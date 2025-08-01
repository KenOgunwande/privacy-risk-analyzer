import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")


import streamlit as st
from app.pii_detection import detect_pii, mask_pii
from app.encryptor import generate_key, encrypt_text, decrypt_text

st.set_page_config(page_title="Privacy Risk Analyzer", layout="centered")
st.title("🔐 Privacy Risk Analyzer")
st.write("Paste text below to detect and mask sensitive personal information.")

user_input = st.text_area("Enter your text here:", height=200)

if st.button("Analyze"):
    detected = detect_pii(user_input)
    masked = mask_pii(user_input)

    if detected:
        st.subheader("🔎 Detected PII:")
        for pii_type, items in detected.items():
            st.write(f"**{pii_type.title()}s:** {', '.join(items)}")
        
        st.subheader("🔒 Masked Text:")
        st.code(masked)

        # Encryption Section
        st.subheader("🔐 Encrypt Masked Text (AES-GCM)")

        use_existing_key = st.checkbox("I have my own key")

        if use_existing_key:
            b64_key = st.text_input("🔑 Enter your Base64-encoded key")
        else:
            b64_key = generate_key()
            st.text_input("🔑 Your generated key (save this!)", b64_key)

        if b64_key:
            nonce, ciphertext = encrypt_text(masked, b64_key)
            st.success("✅ Text encrypted!")
            st.code(f"Nonce: {nonce}")
            st.code(f"Ciphertext: {ciphertext}")
        else:
            st.warning("⚠️ Please provide or generate a key to encrypt the text.")

    else:
        st.success("✅ No PII detected.")

# --- Decryption Section ---
st.markdown("### 🔓 Decryption")

with st.expander("Decrypt Encrypted Text", expanded=True):
    st.markdown("Paste the values below to decrypt your previously encrypted content.")

    # Initialize state variables if not present
    for key in ["decrypt_key", "decrypt_nonce", "decrypt_cipher", "decrypted_result"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    # Input fields bound to session state
    st.text_input("AES Key (Base64)", key="decrypt_key")
    st.text_input("Nonce (Base64)", key="decrypt_nonce")
    st.text_area("Ciphertext (Base64)", key="decrypt_cipher", height=150)

    if st.button("🔓 Decrypt Text"):
        key = st.session_state["decrypt_key"]
        nonce = st.session_state["decrypt_nonce"]
        cipher = st.session_state["decrypt_cipher"]

        if key and nonce and cipher:
            try:
                result = decrypt_text(nonce, cipher, key)
                st.session_state["decrypted_result"] = result
                st.success("Decryption successful!")
            except Exception as e:
                st.error(f"Decryption failed: {e}")
        else:
            st.warning("Please fill in all fields before decrypting.")

    if st.session_state["decrypted_result"]:
        st.text_area("🔍 Decrypted Output", st.session_state["decrypted_result"], height=200)
