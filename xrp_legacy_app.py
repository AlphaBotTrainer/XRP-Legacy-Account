import streamlit as st
from datetime import datetime, timedelta
import qrcode
from io import BytesIO

st.set_page_config(page_title="XRP Legacy Yield Vault Builder", layout="centered")

st.title("🛡️ XRP Legacy Yield Vault Builder")
st.markdown("**Sovereign • Yield-Earning • Time-Locked XRP Legacy**")

# === DONATION AMOUNT (at top) ===
st.subheader("Support This Tool")
donation_amount = st.number_input("Suggested Donation (XRP)", value=10.0, min_value=0.0, step=1.0)
YOUR_XRP_ADDRESS = "rYourRealTangemAddressHere"  # ← REPLACE WITH YOUR ACTUAL XRP ADDRESS

# === INTRODUCTION ===
st.subheader("What You Are Building")
st.markdown("This tool creates a legacy vault system with continuous yield while locked, flexible releases, and a fail-safe.")

# === BUILD SECTION ===
st.subheader("1. Configure Your Legacy Vault")

addresses_input = st.text_area("Wallets You Control (one per line)", value="rYourTangemAddressHere")
addresses = [addr.strip() for addr in addresses_input.splitlines() if addr.strip()]

birthday_str = st.text_input("Beneficiary Birthday (YYYY-MM-DD)", value="2010-06-06")

generational_mode = st.checkbox("**Never Sell / Generational Legacy Mode** (Principal locked forever — only yield accessible)", value=False)

# Dynamic Tranches
st.subheader("Vesting / Redemption Schedule")
if "tranches" not in st.session_state:
    st.session_state.tranches = [(0.5, 16), (10.0, 18), (10.0, 21), (10.0, 30), (20.0, 40), (49.5, 50)]

if st.button("➕ Add Tranche"):
    st.session_state.tranches.append((10.0, 30))

for i in range(len(st.session_state.tranches)):
    col_a, col_b, col_c = st.columns([2, 2, 1])
    with col_a:
        pct = st.number_input(f"Tranche {i+1} — %", value=st.session_state.tranches[i][0], min_value=0.0, max_value=100.0, step=0.1, key=f"pct_{i}")
    with col_b:
        age = st.number_input(f"Release at age +", value=st.session_state.tranches[i][1], min_value=0, step=1, key=f"age_{i}")
    with col_c:
        if st.button("🗑️", key=f"del_{i}"):
            st.session_state.tranches.pop(i)
            st.rerun()
    st.session_state.tranches[i] = (float(pct), int(age))

tranches = st.session_state.tranches

# Fail-Safe
st.subheader("Ultimate Fail-Safe Unlock")
fail_safe_years = st.number_input("All remaining funds unlock after (years from birthday)", value=100, min_value=50, step=1)

st.subheader("Adding Future Deposits")
st.markdown("You can add more XRP anytime using the `prepare_deposit()` function in the generated script.")

# === RISK & FINALIZE ===
st.markdown("---")
st.subheader("2. Final Risk Acknowledgment & Download")

st.error("**CRITICAL RISKS - READ CAREFULLY**")
st.markdown("""
- Irreversibility and long/permanent lock-up  
- Variable / non-guaranteed yield  
- XRP price volatility  
- Technical, protocol, and custody risks  
- Legal & tax compliance in your jurisdiction
""")

name = st.text_input("Type your full name to confirm", placeholder="Your Full Name")
agree = st.checkbox("I have read and understood all risks. I take full responsibility.")

if st.button("✅ Finalize & Download Script", type="primary", disabled=not (agree and name.strip() and addresses)):
    st.success("✅ Plan finalized!")
    
    script_content = f'''# XRP Legacy Yield Vault Script
# Finalized on {datetime.now().strftime("%Y-%m-%d")}

from datetime import datetime, timedelta

TRANCHES = {tranches}
BIRTHDAY = datetime.fromisoformat("{birthday_str}")
FAIL_SAFE_YEARS = {fail_safe_years}

def prepare_deposit(address, amount_drops, vault_id="YOUR_VAULT_ID"):
    print(f"Prepare deposit of {{amount_drops / 1_000_000:.2f}} XRP")

def main():
    print("=== Release Schedule ===")
    for pct, years in TRANCHES:
        if years >= 9999:
            print("Generational Mode: Principal locked forever")
            continue
        unlock_date = BIRTHDAY + timedelta(days=365 * years)
        print(f"{{pct:.1f}}% unlocks on {{unlock_date.date()}}")
    print(f"\\n🔒 Fail-Safe Unlock: {{(BIRTHDAY + timedelta(days=365*FAIL_SAFE_YEARS)).date()}}")
    
    print("\\n=== Suggested Donation ===")
    print(f"Send {donation_amount} XRP to {YOUR_XRP_ADDRESS}")
    print("Use your wallet to send this donation.")

if __name__ == "__main__":
    main()
'''

    st.download_button("📥 Download Finalized Script", data=script_content, file_name="xrp_legacy_yield_vault.py", mime="text/plain")

# Donation QR
st.markdown("---")
st.subheader("💚 Support This Tool")
st.code(YOUR_XRP_ADDRESS)
qr = qrcode.make(YOUR_XRP_ADDRESS)
buf = BytesIO()
qr.save(buf, format="PNG")
st.image(buf.getvalue(), caption="Scan to Donate")

st.caption("Test on XRPL Testnet first. Not financial or legal advice.")
