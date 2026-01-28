
import streamlit as st

st.set_page_config(page_title="Credit FOIR Tool", layout="centered")
st.title("🏦 Credit Appraisal Tool")

# ---------------- FUNCTIONS ----------------

def calculate_emi(p, r, y):
    r = r / (12 * 100)
    n = y * 12
    if r == 0:
        return p / n
    return p * r * (1+r)**n / ((1+r)**n - 1)

def interest_only(p, r):
    return p * (r / (12*100))

def annualize(val, freq):
    if freq == "Monthly":
        return val * 12
    if freq == "Quarterly":
        return val * 4
    return val

# ---------------- SESSION ----------------

if "loans" not in st.session_state:
    st.session_state.loans = []

if "incomes" not in st.session_state:
    st.session_state.incomes = []

# ---------------- INCOME ----------------

st.header("💰 Income Details")

income_heads = ["Salary Income","Rental Income","Agri Income","Other"]

if "income_type" not in st.session_state:
    st.session_state.income_type = income_heads[0]
if "income_amount" not in st.session_state:
    st.session_state.income_amount = 0.0
if "income_freq" not in st.session_state:
    st.session_state.income_freq = "Monthly"
if "custom_income" not in st.session_state:
    st.session_state.custom_income = ""

income_type = st.selectbox("Select Type of Income", income_heads, key="income_type")

if income_type == "Other":
    custom_income = st.text_input("Enter Income Head", key="custom_income")
else:
    custom_income = ""

income_amount = st.number_input("Income Amount", min_value=0.0, step=1000.0, key="income_amount")
income_freq = st.selectbox("Credit Type", ["Monthly","Quarterly","Yearly"], key="income_freq")

if st.button("➕ Add Income"):
    name = custom_income if income_type=="Other" else income_type
    annual = annualize(income_amount, income_freq)

    st.session_state.incomes.append({
        "Type": name,
        "Credit": income_freq,
        "Amount": income_amount,
        "Annual": round(annual,2)
    })

    # Reset fields
    st.session_state.income_amount = 0.0
    st.session_state.custom_income = ""

# ---------------- INCOME TABLE ----------------

total_income = 0

if st.session_state.incomes:
    st.subheader("Income List")

    h1,h2,h3,h4,h5 = st.columns([1,3,2,2,1])
    h1.write("S.No")
    h2.write("Type of Income")
    h3.write("Credit Type")
    h4.write("Annual Income")
    h5.write("")

    for i, inc in enumerate(st.session_state.incomes):
        c1,c2,c3,c4,c5 = st.columns([1,3,2,2,1])
        c1.write(i+1)
        c2.write(inc["Type"])
        c3.write(inc["Credit"])
        c4.write(f"₹{inc['Annual']:,.0f}")
        total_income += inc["Annual"]
        if c5.button("❌", key=f"inc{i}"):
            st.session_state.incomes.pop(i)
            st.experimental_rerun()

st.write(f"### Total Annual Income: ₹{total_income:,.2f}")

st.divider()

# ---------------- LOANS ----------------

st.header("🏦 Loan Details")

loan_types = ["Term Loan","CC","OD","DOD"]

if "loan_type" not in st.session_state:
    st.session_state.loan_type = loan_types[0]
if "loan_amt" not in st.session_state:
    st.session_state.loan_amt = 0.0
if "loan_rate" not in st.session_state:
    st.session_state.loan_rate = 0.0
if "loan_tenure" not in st.session_state:
    st.session_state.loan_tenure = 1.0
if "loan_freq" not in st.session_state:
    st.session_state.loan_freq = "Monthly"

loan_type = st.selectbox("Loan Type", loan_types, key="loan_type")
loan_amt = st.number_input("Loan Amount", min_value=0.0, step=10000.0, key="loan_amt")
loan_rate = st.number_input("Interest %", min_value=0.0, step=0.1, key="loan_rate")
loan_freq = st.selectbox("Obligation Credit Type", ["Monthly","Quarterly","Yearly"], key="loan_freq")

if loan_type == "Term Loan":
    loan_tenure = st.number_input("Tenure (Years)", min_value=0.1, step=0.5, key="loan_tenure")
else:
    loan_tenure = None

if st.button("➕ Add Loan"):

    if loan_type == "Term Loan":
        base = calculate_emi(loan_amt, loan_rate, loan_tenure)
    else:
        base = interest_only(loan_amt, loan_rate)

    annual = annualize(base, loan_freq)

    st.session_state.loans.append({
        "Type": loan_type,
        "Interest": loan_rate,
        "Tenure": loan_tenure if loan_tenure else "-",
        "Credit": loan_freq,
        "Obligation": round(base,2),
        "Annual": round(annual,2)
    })

    # Reset fields
    st.session_state.loan_amt = 0.0
    st.session_state.loan_rate = 0.0

# ---------------- LOAN TABLE ----------------

total_obligation = 0

if st.session_state.loans:
    st.subheader("Loan List")

    h1,h2,h3,h4,h5,h6,h7 = st.columns([1,2,1,1,1,2,1])
    h1.write("S.No")
    h2.write("Loan Type")
    h3.write("Interest")
    h4.write("Tenure")
    h5.write("Credit")
    h6.write("Obligation")
    h7.write("")

    for i, l in enumerate(st.session_state.loans):
        c1,c2,c3,c4,c5,c6,c7 = st.columns([1,2,1,1,1,2,1])
        c1.write(i+1)
        c2.write(l["Type"])
        c3.write(l["Interest"])
        c4.write(l["Tenure"])
        c5.write(l["Credit"])
        c6.write(f"₹{l['Annual']:,.0f}")
        total_obligation += l["Annual"]
        if c7.button("❌", key=f"loan{i}"):
            st.session_state.loans.pop(i)
            st.experimental_rerun()

st.write(f"### Total Annual Obligation: ₹{total_obligation:,.2f}")

# ---------------- RESULT ----------------

st.divider()
st.header("✅ RESULT")

if total_income > 0:
    foir = (total_obligation / total_income) * 100
    st.write(f"### FOIR : {foir:.2f}%")
else:
    st.write("Please add income")

# ---------------- RESET ----------------

if st.button("Reset All"):
    st.session_state.incomes=[]
    st.session_state.loans=[]
    st.experimental_rerun()
