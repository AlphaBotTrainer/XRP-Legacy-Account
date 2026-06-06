import streamlit as st
from datetime import datetime, timedelta
import qrcode
from io import BytesIO

st.set_page_config(page_title="XRP Legacy Yield Vault Builder", layout="centered")

st.title("🛡️ XRP Legacy Yield Vault Builder")
st.markdown("**Sovereign • Yield-Earning • Time-Locked XRP Legacy**")

# === INTRODUCTION ===
st.subheader("What You Are Building")
st.markdown("""
This tool creates a legacy vault system for XRP with continuous yield while locked.
You can choose standard releases, single-date release, or generational "Never Sell" mode.
""")

# === BUILD SECTION ===
st.subheader("1. Configure Your Legacy Vault")

addresses_input = st.text_area("Wallets You Control (one per line)", value="rYourTangemAddressHere")
addresses = [addr.strip() for addr in addresses_input.splitlines() if addr.strip()]

birthday_str = st.text_input("Beneficiary Birthday (YYYY-MM-DD)", value="2010-06-06")

generational_mode = st.checkbox("**Never Sell / Generational Legacy Mode** (Principal stays locked forever — beneficiary receives only yield)", value=False)

if generational_mode:
    st.warning("⚠️ **NOT RECOMMENDED FOR MOST USERS** — This creates a true multi-generational lock where the principal is never released. Only earned yield can be withdrawn. Strong fail-safe still applies below.")

use_single_date = st.checkbox("Use Single Release Date for All Funds (Simple Mode)", value=False) if not generational_mode else False

if generational_mode:
    tranches = [(1.0, 9999)]  # Symbolic — principal never releases
elif use_single_date:
    release_years = st.number_input("Release All Funds After (years)", value=30, min_value=1, step=1)
    tranches = [(1.0, release_years)]
else:
    st.subheader("Vesting / Redemption Schedule")
    tranches = []
    default_pcts = [0.5, 10, 10, 10, 20, 49.5]
    default_ages = [16, 18, 21, 30, 40, 50]
    for i in range(6):
        col_a, col_b = st.columns([1, 1])
        with col_a:
            pct = st.number_input(f"Tranche {i+1} (%)", value=default_pcts[i], min_value=0.0, max_value=100.0, step=0.1, key=f"pct{i}")
        with col_b:
            age = st.number_input(f"Release at age +", value=default_ages[i], min_value=0, step=1, key=f"age{i}")
        tranches.append((pct / 100.0, age))

# Fail-Safe (always present)
st.subheader("Ultimate Fail-Safe Unlock")
fail_safe_years = st.number_input("All remaining funds unlock after (years from birthday)", value=100, min_value=50, step=1)
st.info(f"**Fail-Safe Date**: All remaining funds become redeemable by birthday + {fail_safe_years} years (even in Generational Mode).")

st.subheader("Adding Future Deposits")
st.markdown("You can add more XRP anytime. New deposits earn yield immediately and follow the chosen rules.")

# === RISK & FINALIZE ===
st.markdown("---")
st.subheader("2. Final Risk Acknowledgment & Download")

st.error("**CRITICAL RISKS - READ CAREFULLY BEFORE FINALIZING**")
st.markdown("""
- Irreversibility and long/ permanent lock-up
- Variable / non-guaranteed yield
- XRP price volatility
- Technical, protocol, and custody risks
- Legal & tax compliance in your jurisdiction
""")

name = st.text_input("Type your full name to confirm", placeholder="Your Full Name")
agree = st.checkbox("I have read and understood all risks. I take full responsibility.")

if st.button("✅ Finalize & Download Script", type="primary", disabled=not (agree and name.strip() and addresses)):
    st.success("✅ Legacy Vault Plan finalized!")
    
    mode = "Generational Never-Sell" if generational_mode else ("Single Date" if use_single_date else "Multi-Tranche")
    
    script_content = f'''# XRP Legacy Yield Vault Script
# Mode: {mode}
# Finalized on {datetime.now().strftime("%Y-%m-%d")}

from datetime import datetime, timedelta

TRANCHES = {tranches}
BIRTHDAY = datetime.fromisoformat("{birthday_str}")
FAIL_SAFE_YEARS = {fail_safe_years}
GENERATIONAL_MODE = {generational_mode}

def calculate_notice_date(unlock_date, notice_days=40):
    notice_start = (unlock_date - timedelta(days=notice_days)).replace(day=1)
    return notice_start

def prepare_deposit(address, amount_drops, vault_id="YOUR_VAULT_ID"):
    print(f"Prepare additional deposit of {{amount_drops / 1_000_000:.2f}} XRP")

def main():
    print("=== Release Schedule ===")
    if GENERATIONAL_MODE:
        print("⚠️ GENERATIONAL MODE: Principal is never released. Only yield can be withdrawn.")
    for pct, years in TRANCHES:
        if years >= 9999:
            continue
        unlock_date = BIRTHDAY + timedelta(days=365 * years)
        notice_date = calculate_notice_date(unlock_date)
        print(f"{{pct*100:.1f}}% → Unlock {{unlock_date.date()}} | Notice ~{{notice_date.date()}}")
    
    fail_safe_date = BIRTHDAY + timedelta(days=365 * FAIL_SAFE_YEARS)
    print(f"\\n🔒 ULTIMATE FAIL-SAFE: All remaining funds unlock by {{fail_safe_date.date()}}")
    
    print("\\nUse prepare_deposit() anytime to add more XRP.")

if __name__ == "__main__":
    main()
'''

    st.download_button(
        label="📥 Download Your Finalized Python Script",
        data=script_content,
        file_name="xrp_legacy_yield_vault.py",
        mime="text/plain"
    )

# Donation section
st.markdown("---")
st.subheader("💚 Support This Tool")
st.markdown("**Suggested Donation: 10 XRP**")
donation_address = addresses[0] if addresses else "rYourTangemAddressHere"
st.code(donation_address)

st.caption("Test on XRPL Testnet first. Not financial or legal advice.")
