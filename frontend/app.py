import streamlit as st 
import requests 

# Setting th e Page Configuration 

st.set_page_config(page_title = "AI Loan Officer", layout = "centered")
st.title(" AI Loan Officer")
st.caption("Human-in-the-Loop Loan Decision System")

# API Configuration 

API_URL = "https://active-sentinel.onrender.com/"

# User Input Section (SideBar)

st.sidebar.header("Applicant Details")

income = st.sidebar.number_input(
    "Applicant Income",
    min_value=500,
    max_value=50000,
    value=5000
)

loan_amount = st.sidebar.number_input(
    "Loan Amount",
    min_value=50,
    max_value=1000,
    value=150
)

credit_history = st.sidebar.selectbox(
    "Credit History",
    options=[0, 1],
    format_func=lambda x: "Good (1)" if x == 1 else "Bad (0)"
)

# Prediction Button (API Call)

if st.button("🔍 Assess Loan Risk"):
    payload = {
        "Income": income,
        "LoanAmount": loan_amount,
        "CreditHistory": credit_history
    }

    try:
        response = requests.post(f"{API_URL}/predict", json=payload)
        response.raise_for_status()
        result = response.json()

        prediction = result.get("prediction")
        probability = result.get("probability")

        if prediction is None or probability is None:
            st.error("Invalid response from prediction API.")
        else:
            if prediction == 1:
                st.success("✅ Loan Approved")
            else:
                st.error("❌ Loan Rejected")

            st.metric("Approval Probability", f"{probability:.2f}")

            st.session_state["last_payload"] = payload
            st.session_state["last_prediction"] = prediction

    except Exception as e:
        st.error(f"API Error: {e}")



# Human Feedback Section 

if "last_payload" in st.session_state and "last_prediction" in st.session_state:
    st.markdown("---")
    st.subheader("🧠 Human Feedback")
    st.write("Is this decision correct?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Yes, Correct"):
            feedback_payload = {
                **st.session_state["last_payload"],
                "prediction": st.session_state["last_prediction"],
                "actual": st.session_state["last_prediction"]
            }

            requests.post(f"{API_URL}/feedback", json=feedback_payload)
            st.success("Feedback recorded!")

    with col2:
        if st.button("❌ No, Incorrect"):
            actual = 1 if st.session_state["last_prediction"] == 0 else 0

            feedback_payload = {
                **st.session_state["last_payload"],
                "prediction": st.session_state["last_prediction"],
                "actual": actual
            }

            requests.post(f"{API_URL}/feedback", json=feedback_payload)
            st.warning("Correction logged. System updated.")


# Live System monitoring (Admin View) 

st.markdown("---")
if st.checkbox("📊 Show System Health"):
    try:
        stats_response = requests.get(f"{API_URL}/stats")
        stats_response.raise_for_status()
        stats = stats_response.json()
        st.json(stats)
    except Exception as e:
        st.error(f"Could not fetch system stats: {e}")
