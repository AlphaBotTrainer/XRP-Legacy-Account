import streamlit as st
from datetime import datetime, timedelta
import qrcode
from io import BytesIO

st.set_page_config(page_title="XRP Legacy Yield Vault Builder", layout="centered")

st.title("🛡️ XRP Legacy Yield Vault Builder")
st.markdown("**Sovereign • Yield-Earning • Time-Locked XRP Legacy**")

# === BUILD SECTION ===
st.subheader("1. Configure Your Legacy Vault")

addresses_input = st.text_area("Wallets You want to Vault (one per line)", value="rYourTangemAddressHere")
addresses = [addr.strip() for addr in addresses_input.splitlines() if addr.strip()]

total_xrp = st.number_input("Total XRP Being Managed", value=2000.0, min_value=0.0, step=1.0)

birthday = st.date_input("Beneficiary Birthday", value=datetime(2010, 6, 6).date(), format="MM/DD/YYYY")
st.caption("Release dates are calculated from the birth date above.")

generational_mode = st.checkbox("**Never Sell / Generational Legacy Mode** (Principal stays locked forever — only yield accessible)", value=False)

est_price = st.number_input("Estimated XRP Value (USD)", value=5.0, min_value=0.0, step=0.1)

# Redemption Schedule
st.subheader("Redemption Schedule")

if "redemptions" not in st.session_state:
    st.session_state.redemptions = [(16, 0.5), (18, 10.0), (21, 10.0), (30, 10.0), (40, 20.0), (50, 49.5)]

if st.button("➕ Add Redemption Level"):
    st.session_state.redemptions.append((30, 10.0))
    st.rerun()

for i in range(len(st.session_state.redemptions)):
    col_a, col_b, col_c, col_d, col_e = st.columns([1.5, 2, 2, 2.5, 1])
    with col_a:
        age = st.number_input(f"Age +", value=st.session_state.redemptions[i][0], min_value=0, step=1, key=f"age_{i}")
    with col_b:
        pct = st.number_input(f"Percentage (%)", value=st.session_state.redemptions[i][1], min_value=0.0, max_value=100.0, step=0.1, key=f"pct_{i}")
    with col_c:
        xrp_amount = total_xrp * (pct / 100.0)
        st.metric("XRP Released", f"{xrp_amount:.2f}")
    with col_d:
        usd_value = xrp_amount * est_price
        st.metric("Est. USD Value", f"${usd_value:,.2f}")
    with col_e:
        if st.button("🗑️", key=f"del_{i}"):
            st.session_state.redemptions.pop(i)
            st.rerun()
    st.session_state.redemptions[i] = (int(age), float(pct))

redemptions = st.session_state.redemptions

# Fail-Safe
st.subheader("Ultimate Fail-Safe Unlock")
fail_safe_years = st.number_input("All remaining funds unlock after (years from birthday)", value=100, min_value=50, step=1)

# === SUPPORT / DONATION SECTION (Moved here as requested) ===
st.subheader("💚 Support This Tool")
donation_amount = st.number_input("Suggested Donation Amount (XRP)", value=10.0, min_value=0.0, step=1.0)
YOUR_XRP_ADDRESS = "rYourRealTangemAddressHere"   # ← REPLACE WITH YOUR ACTUAL ADDRESS

st.code(YOUR_XRP_ADDRESS)

col1, col2 = st.columns(2)
with col1:
    if st.button("📋 Copy Address"):
        st.success("✅ Address copied!")
with col2:
    if st.button("💸 Prepare Donation Transaction"):
        st.info(f"**Ready-to-sign {donation_amount} XRP Donation**\\n\\nDestination: {YOUR_XRP_ADDRESS}\\nAmount: {donation_amount} XRP")

qr = qrcode.make(YOUR_XRP_ADDRESS)
buf = BytesIO()
qr.save(buf, format="PNG")
st.image(buf.getvalue(), caption="Scan to Donate XRP (any amount)")

st.subheader("Adding Future Deposits")
st.markdown("You can add more XRP to the vault anytime. New deposits earn yield and follow the same rules.")

# === RISK ACKNOWLEDGMENT & FINALIZE ===
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

BIRTHDAY = datetime({birthday.year}, {birthday.month}, {birthday.day})
REDEMPTIONS = {redemptions}
FAIL_SAFE_YEARS = {fail_safe_years}
TOTAL_XRP = {total_xrp}

def main():
    print("=== Redemption Schedule ===")
    for age, pct in REDEMPTIONS:
        if age >= 9999:
            print("Generational Mode: Principal locked forever (only yield accessible)")
            continue
        unlock_date = BIRTHDAY + timedelta(days=365 * age)
        xrp_amount = TOTAL_XRP * (pct / 100.0)
        print(f"Age +{age} → {pct:.1f}% | {xrp_amount:.2f} XRP")
    print(f"\\n🔒 Fail-Safe: All remaining funds unlock by {{(BIRTHDAY + timedelta(days=365*FAIL_SAFE_YEARS)).date()}}")

if __name__ == "__main__":
    main()
'''

    st.download_button("📥 Download Finalized Script", data=script_content, file_name="xrp_legacy_yield_vault.py", mime="text/plain")

st.caption("Test everything on XRPL Testnet first. Not financial or legal advice.")
