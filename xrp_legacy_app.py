# === Redemption Schedule ===
st.subheader("Redemption Schedule")

total_xrp = st.number_input("Total XRP Being Managed", value=2000.0, min_value=0.0, step=1.0)
est_price = st.number_input("Estimated XRP Value (USD)", value=5.0, min_value=0.0, step=0.1)

if "redemptions" not in st.session_state:
    st.session_state.redemptions = [(16, 0.5), (18, 10.0), (21, 10.0), (30, 10.0), (40, 20.0), (50, 49.5)]

if st.button("➕ Add Redemption Level"):
    st.session_state.redemptions.append((30, 10.0))
    st.rerun()

# Header Row
header_cols = st.columns([1.5, 2, 2, 2.5, 1])
header_cols[0].write("**Age +**")
header_cols[1].write("**Percentage (%)**")
header_cols[2].write("**XRP Released**")
header_cols[3].write("**Est. USD Value**")
header_cols[4].write("**Action**")

for i in range(len(st.session_state.redemptions)):
    col_a, col_b, col_c, col_d, col_e = st.columns([1.5, 2, 2, 2.5, 1])
    with col_a:
        age = st.number_input(f"Age +", value=st.session_state.redemptions[i][0], min_value=0, step=1, key=f"age_{i}", label_visibility="collapsed")
    with col_b:
        pct = st.number_input(f"Percentage (%)", value=st.session_state.redemptions[i][1], min_value=0.0, max_value=100.0, step=0.1, key=f"pct_{i}", label_visibility="collapsed")
    with col_c:
        xrp_amount = total_xrp * (pct / 100.0)
        st.write(f"{xrp_amount:.2f} XRP")
    with col_d:
        usd_value = xrp_amount * est_price
        st.write(f"${usd_value:,.2f}")
    with col_e:
        if st.button("🗑️", key=f"del_{i}"):
            st.session_state.redemptions.pop(i)
            st.rerun()
    st.session_state.redemptions[i] = (int(age), float(pct))
