import secrets
tippay_secret = secrets.token_hex(16)
print(f"TIPPAY_SECRET={tippay_secret}")