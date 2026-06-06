import streamlit as st
from datetime import datetime, timedelta
import qrcode
from io import BytesIO

st.set_page_config(page_title="XRP Legacy Yield Vault Builder", layout="centered")

st.title("🛡️ XRP Legacy Yield Vault Builder")
st.markdown("**Sovereign • Yield-Earning • Time-Locked XRP Legacy**")

# === INTRODUCTION ===
st.subheader("What You Are Building")
st.markdown("This tool creates a legacy vault system for XRP with continuous yield while locked, time-based releases, and a fail-safe.")

# === BUILD SECTION ===
st.subheader("1. Configure Your Legacy Vault")

addresses_input = st.text_area("Wallets You Control (one per line)", value="rYourTangemAddressHere")
addresses = [addr.strip() for addr in addresses_input.splitlines() if addr.strip()]

birthday_str = st.text_input("Beneficiary Birthday (YYYY-MM-DD)", value="2010-06-06")

generational_mode = st.checkbox("**Never Sell / Generational Legacy Mode** (Principal stays locked forever — only yield accessible)", value=False)

if generational_mode:
    st.warning("⚠️ NOT RECOMMENDED FOR MOST USERS — Principal never released.")
    tranches = [(1.0, 9999)]
else:
    use_single = st.checkbox("Use Single Release Date for All Funds", value=False)
    if use_single:
        years = st.number_input("Release all funds after how many years?", value=30, min_value=1, step=1)
        tranches = [(1.0, float(years))]
    else:
        st.subheader("Vesting / Redemption Schedule (Multiple Tranches)")
        tranches = []
        default_pcts = [0.5, 10.0, 10.0, 10.0, 20.0, 49.5]
        default_ages = [16, 18, 21, 30, 40, 50]
        for i in range(6):
            col_a, col_b = st.columns([1, 1])
            with col_a:
                pct = st.number_input(
                    f"Tranche {i+1} — Percentage (%)", 
                    value=default_pcts[i], 
                    min_value=0.0, 
                    max_value=100.0, 
                    step=0.1, 
                    key=f"pct_{i}"
                )
            with col_b:
                age = st.number_input(
                    f"Tranche {i+1} — Release at age +", 
                    value=default_ages[i], 
                    min_value=0, 
                    step=1, 
                    key=f"age_{i}"
                )
            tranches.append((float(pct) / 100.0, int(age)))

# Fail-Safe
st.subheader("Ultimate Fail-Safe Unlock")
fail_safe_years = st.number_input("All remaining funds unlock after (years from birthday)", value=100, min_value=50, step=1)

st.subheader("Adding Future Deposits")
st.markdown("You can add more XRP to the vault anytime. New deposits earn yield and follow the same rules.")

# === RISK ACKNOWLEDGMENT ===
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

def main():
    print("=== Release Schedule ===")
    for pct, years in TRANCHES:
        if years >= 9999:
            print("Generational Mode: Principal locked forever (only yield accessible)")
            continue
        unlock_date = BIRTHDAY + timedelta(days=365 * years)
        print(f"{{pct*100:.1f}}% unlocks on {{unlock_date.date()}}")
    print(f"\\n🔒 Fail-Safe: All funds unlock by {{(BIRTHDAY + timedelta(days=365*FAIL_SAFE_YEARS)).date()}}")

if __name__ == "__main__":
    main()
'''

    st.download_button("📥 Download Finalized Script", data=script_content, file_name="xrp_legacy_yield_vault.py", mime="text/plain")

# Donation
st.markdown("---")
st.subheader("💚 Support This Tool")
st.markdown("**Suggested Donation: 10 XRP**")
donation_address = addresses[0] if addresses else "rYourTangemAddressHere"
st.code(donation_address)

st.caption("Test on XRPL Testnet first. Not financial or legal advice.")
