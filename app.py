import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(
    page_title="GovDPI | Civic Requirements Agent",
    page_icon="🏛️",
    layout="wide"
)

# Custom CSS to make it look different from your last project
st.markdown("""
<style>
    .stButton>button {
        background-color: #0F9D58; /* Google Green */
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0B8043;
    }
    .main-header {
        color: #1a73e8; /* Google Blue */
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🏛️ GovDPI: Autonomous Civic Requirements Agent</h1>", unsafe_allow_html=True)
st.caption("Track 01: AI for Digital Public Infrastructure & Governance | GDG Madurai Keeladi Edition")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Enter Gemini API Key:", type="password", placeholder="AIzaSy...")
    
    st.markdown("---")
    st.subheader("📜 Sample Civic Schemes")
    preset = st.selectbox(
        "Select a policy brief:",
        [
            "Custom Brief",
            "Rural Offline Ration (PDS) Sync",
            "Farmer Drought Relief (DBT)",
            "Women Artisan Micro-Grants via e-Sevai"
        ]
    )

sample_briefs = {
    "Rural Offline Ration (PDS) Sync": "Fair price shops (ration shops) in remote rural zones experience frequent network outages. We need an offline-first POS verification system. When connectivity drops, verify cardholders via biometric hash or offline OTP, queue rations disbursed in an encrypted local database, and securely sync transactions with the State Food & Civil Supplies cloud once network resumes without duplicate payouts.",
    "Farmer Drought Relief (DBT)": "Automate disaster relief disbursement when rainfall drops below normal. The system must correlate satellite vegetation and drought indices directly with state land records (Patta/Chitta). If crop damage exceeds 33%, disburse financial assistance directly to the farmer's Aadhaar-seeded bank account via PFMS/DBT, bypassing physical revenue officer inspection queues.",
    "Women Artisan Micro-Grants via e-Sevai": "A portal for women weavers and traditional artisans in rural clusters to receive state seed capital. Most applicants have basic feature phones or visit local e-Sevai centers. The system needs voice-assisted application intake in Tamil, DigiLocker pull for artisan community ID, and auto-verification of bank account seeding."
}

default_brief = sample_briefs.get(preset, "")

# Main Input
policy_brief = st.text_area(
    "Paste Unstructured Policy / Scheme Brief:",
    value=default_brief,
    height=200
)

# Generate Button
if st.button("⚡ Generate DPI Architecture Spec", type="primary"):
    if not api_key:
        st.error("⚠️ Please enter your Gemini API Key in the sidebar.")
    elif not policy_brief.strip():
        st.warning("⚠️ Please provide a policy brief.")
    else:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an elite Digital Public Infrastructure (DPI) Architect.
        Analyze this civic scheme brief:
        \"\"\"{policy_brief}\"\"\"

        Structure your output strictly into these 4 Markdown sections:
        ### 1. Citizen Journey & Last-Mile Delivery
        - **Target Beneficiary Profile**: Primary groups impacted.
        - **Access Channels**: Delivery endpoints.
        - **Inclusion Measures**: Design safeguards.

        ### 2. Digital Public Infrastructure (DPI) Integration Matrix
        - **Identity & KYC**: Verification mechanism.
        - **Document & Data Layer**: Registries utilized.
        - **Payment Rails**: Financial disbursement rails.

        ### 3. Engineering Acceptance Criteria (BDD / Gherkin)
        - Scenario A: Happy Path.
        - Scenario B: Edge Case (Network drop/Biometric fail).

        ### 4. Governance & Vulnerability Risk Audit
        - Data Privacy & DPDP compliance.
        - Exclusion risk warning.
        """
        
        with st.spinner("Analyzing public infrastructure rails and drafting specs..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.success("✅ DPI Specification Generated Successfully!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Execution Error: {e}")
