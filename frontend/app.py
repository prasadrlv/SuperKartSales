
import os
import requests
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="SuperKart | Sales Prediction",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
# In Docker, set BACKEND_URL=http://backend:7860
# For local development, the default is localhost.
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:7860").rstrip("/")

# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(124,58,237,.10), transparent 30%),
            radial-gradient(circle at 90% 5%, rgba(14,165,233,.10), transparent 28%),
            #f8fafc;
    }

    stApp,
    .stApp p,
    .stApp li,
    .stApp label {
        color: #000000 !important;
    }

    [data-testid="stAppViewContainer"] {
        color: #111827;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hide default Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hero */
    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.6rem 2.8rem;
        border-radius: 24px;
        color: white;
        background: linear-gradient(135deg, #111827 0%, #312e81 48%, #2563eb 100%);
        box-shadow: 0 18px 50px rgba(30,41,59,.18);
        margin-bottom: 1.25rem;
    }

    .hero::after {
        content: "🛒";
        position: absolute;
        right: 4%;
        top: 12%;
        font-size: 7rem;
        opacity: .12;
        transform: rotate(-8deg);
    }

    .hero-kicker {
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: .14em;
        text-transform: uppercase;
        color: #c4b5fd;
        margin-bottom: .65rem;
    }

    .hero-title {
        font-size: clamp(2rem, 5vw, 3.25rem);
        line-height: 1.05;
        font-weight: 800;
        margin: 0 0 .8rem 0;
    }

    .hero-text {
        max-width: 720px;
        font-size: 1rem;
        line-height: 1.65;
        color: #dbeafe;
        margin: 0;
    }

    /* Cards */
    .info-card {
        background: rgba(255,255,255,.88);
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 1rem 1.1rem;
        height: 100%;
        box-shadow: 0 5px 20px rgba(15,23,42,.05);
    }

    .info-icon {
        font-size: 1.45rem;
        margin-bottom: .45rem;
    }

    .info-title {
        font-size: .9rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: .2rem;
    }

    .info-text {
        font-size: .78rem;
        color: #64748b;
    }

    .section-heading {
        font-size: 1.35rem;
        font-weight: 800;
        color: #111827;
        margin: 1.2rem 0 .25rem 0;
    }

    .section-caption {
        color: #64748b;
        font-size: .9rem;
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #718096;
        margin-bottom: 2rem;
    }

    .result-card {
        padding: 1.25rem;
        border-radius: 18px;
        border: 1px solid #ddd6fe;
        background: linear-gradient(135deg, #faf5ff, #eff6ff);
        margin-top: 1rem;
    }

    .result-label {
        color: #64748b;
        font-size: .82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .08em;
    }

    .result-value {
        color: #312e81;
        font-size: 2.25rem;
        font-weight: 800;
        margin-top: .2rem;
    }

    .api-pill {
        display: inline-block;
        padding: .28rem .65rem;
        border-radius: 999px;
        background: #eef2ff;
        color: #4338ca;
        font-size: .72rem;
        font-weight: 700;
        margin-top: .5rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        padding: 0 22px;
        background-color: #F3F4F6;
        border-radius: 10px 10px 0 0;
        color: #4B5563;
        font-size: 16px;
        font-weight: 600;
        border: none;
    }

    button[data-baseweb="tab"] {
        font-weight: 700;
        font-size: .95rem;
    }

    /* Primary buttons */
    .stButton > button[kind="primary"] {
        border-radius: 12px;
        font-weight: 700;
        min-height: 3rem;
        box-shadow: 0 8px 20px rgba(79,70,229,.18);
    }

    .stDownloadButton button {
        border-radius: 12px;
        font-weight: 700;
        min-height: 3rem;
        box-shadow: 0 8px 20px rgba(79,70,229,.18);
    }


    /* File uploader */
    [data-testid="stFileUploader"] {
        border-radius: 16px;
    }

    [data-testid="stFileUploaderFileName"] {
        color: #2563EB;
        font-size: 0.95rem;
        font-weight: 600;
        max-width: 280px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">AI-powered retail analytics</div>
        <div class="hero-title">SuperKart Sales Predictor</div>
        <p class="hero-text">
            Estimate product sales instantly or run predictions across an entire CSV in batchmode.
            Use the same trained model through a simple, modern prediction workspace.
        </p>
        <div class="api-pill">● API connected through Docker</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize state only once
if "show_settings" not in st.session_state:
    st.session_state.show_settings = False

if "server_endpoint" not in st.session_state:
    st.session_state.server_endpoint = ""

# Toggle function
def toggle_settings():
    st.session_state.show_settings = not st.session_state.show_settings

# Settings button
st.button(
    "⚙️",
    on_click=toggle_settings,
    type="secondary"
)

# Show this only after clicking Settings
if st.session_state.show_settings:
    BACKEND_URL = st.text_input(
        "Server endpoint",
        key="server_endpoint",
        value=BACKEND_URL,
        help="Enter the base URL for your server or API."
    )

# ---------------------------------------------------------
# Feature cards
# ---------------------------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">🎯</div>
            <div class="info-title">Single prediction</div>
            <div class="info-text">Enter one product and store profile to get an instant sales estimate.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">📊</div>
            <div class="info-title">Batch prediction</div>
            <div class="info-text">Upload a CSV and predict sales for multiple products in one request.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">⚡</div>
            <div class="info-title">Fast API workflow</div>
            <div class="info-text">Streamlit handles the UI while your Flask API handles model inference.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Prediction tabs
# ---------------------------------------------------------
single_tab, batch_tab = st.tabs(["🎯 Single Prediction", "📁 Batch Prediction"])

# =========================================================
# SINGLE PREDICTION
# =========================================================
with single_tab:
    st.markdown(
        '<div class="section-heading">Predict sales for one product</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-caption">Provide the product and store attributes below.</div>',
        unsafe_allow_html=True,
    )

    with st.form("single_prediction_form"):
        left, right = st.columns(2, gap="large")

        with left:
            st.markdown('<div class="section-title">📦 Product details</div>', unsafe_allow_html=True)

            Product_Weight = st.number_input(
                "Product Weight",
                min_value=0.0,
                value=12.66,
                step=0.01,
                help="Weight of the product.",
            )

            Product_Sugar_Content = st.selectbox(
                "Product Sugar Content",
                ["Low Sugar", "Regular", "No Sugar"],
            )

            Product_Allocated_Area = st.number_input(
                "Product Allocated Area",
                min_value=0.0,
                value=0.068,
                step=0.001,
                format="%.3f",
                help="Ratio of the product display area to total store display area.",
            )

            Product_MRP = st.number_input(
                "Product MRP",
                min_value=0.0,
                value=116.7,
                step=0.1,
                help="Maximum retail price.",
            )

            Product_Type_Category = st.selectbox(
                "Product Type Category",
                ["Perishables", "Non Perishables"],
            )

            Product_Id_char = st.selectbox(
                "Product ID Category",
                ["FD", "NC", "DR"],
            )

        with right:

            st.markdown('<div class="section-title">🏪 Store details</div>', unsafe_allow_html=True)
            Store_Size = st.selectbox(
                "Store Size",
                ["Small", "Medium", "High"],
            )

            Store_Location_City_Type = st.selectbox(
                "Store Location City Type",
                ["Tier 1", "Tier 2", "Tier 3"],
            )

            Store_Type = st.selectbox(
                "Store Type",
                [
                    "Supermarket Type1",
                    "Supermarket Type2",
                    "Departmental Store",
                    "Food Mart",
                ],
            )

            Store_Age_Years = st.number_input(
                "Store Age (Years)",
                min_value=0,
                value=17,
                step=1,
            )

            st.markdown(
                """
                <div class="info-card" style="margin-top:.7rem;">
                    <div class="info-icon">💡</div>
                    <div class="info-title">Prediction tip</div>
                    <div class="info-text">
                        Check the product MRP and store attributes before running the model.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "⚡ Run Sales Prediction",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if Product_Weight <= 0:
            st.warning("Please enter a valid Product Weight.")
        elif Product_MRP <= 0:
            st.warning("Please enter a valid Product MRP.")
        else:
            product_request_data = {
                "Product_Weight": Product_Weight,
                "Product_Sugar_Content": Product_Sugar_Content,
                "Product_Allocated_Area": Product_Allocated_Area,
                "Product_MRP": Product_MRP,
                "Store_Size": Store_Size,
                "Store_Location_City_Type": Store_Location_City_Type,
                "Store_Type": Store_Type,
                "Store_Age_Years": Store_Age_Years,
                "Product_Type_Category": Product_Type_Category,
                "Product_Id_char": Product_Id_char,
            }

            with st.spinner("Running sales prediction..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/v1/predict",
                        json=product_request_data,
                        headers={"Content-Type": "application/json"},
                        timeout=60,
                    )

                    if response.status_code == 200:
                        result = response.json()
                        predicted_sales = result.get("Sales", 0)

                        st.markdown(
                            f"""
                            <div class="result-card">
                                <div class="result-label">Predicted Sales</div>
                                <div class="result-value">{float(predicted_sales):,.2f}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        try:
                            error_detail = response.json().get("error", response.text)
                        except Exception:
                            error_detail = response.text

                        st.error(
                            f"Prediction API returned HTTP {response.status_code}: {error_detail}"
                        )

                except requests.exceptions.RequestException as e:
                    st.error(
                        f"Unable to connect to the prediction API at "
                        f"{BACKEND_URL}: {e}"
                    )

# =========================================================
# BATCH PREDICTION
# =========================================================
with batch_tab:
    st.markdown(
        '<div class="section-heading">Predict sales in bulk</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-caption">Upload a CSV containing the model input columns.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">📄</div>
            <div class="info-title">CSV batch prediction</div>
            <div class="info-text">
                Upload your product dataset, review the rows, then send it to the
                batch prediction API.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload the CSV used by your batch prediction endpoint.",
    )

    if uploaded_file is not None:
        try:
            preview_df = pd.read_csv(uploaded_file)

            with st.expander("👀 Preview uploaded data", expanded=True):
                st.dataframe(
                    preview_df.head(5),
                    use_container_width=True,
                    hide_index=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(
                "🚀 Run Batch Prediction",
                type="primary",
                use_container_width=True,
                key="batch_prediction_button",
            ):
                # Reset the file pointer because it was read for the preview.
                uploaded_file.seek(0)

                with st.spinner(
                    f"Running predictions for {len(preview_df):,} rows..."
                ):
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/v1/predictbatch",
                            files={
                                "file": (
                                    uploaded_file.name,
                                    uploaded_file,
                                    "text/csv",
                                )
                            },
                            timeout=120,
                        )

                        if response.status_code == 200:
                            predictions = response.json()

                            st.success("Batch predictions completed successfully!")
                           

                            sales = list(predictions.values())
                            if len(sales) == len(preview_df):
                                result_df = preview_df.copy()
                                result_df.insert(0, "Predicted_Sales", sales)
                                st.markdown("#### 📈 Prediction results")
                                st.dataframe(
                                    result_df,
                                    use_container_width=True,
                                    hide_index=True,
                                )

                                # CSV download
                                csv_data = result_df.to_csv(index=False).encode("utf-8")

                                st.download_button(
                                    "⬇️ Download predictions as CSV",
                                    data=csv_data,
                                    type="primary",
                                    file_name="superkart_predictions.csv",
                                    mime="text/csv",
                                    use_container_width=True,
                                )

                        else:
                            try:
                                error_detail = response.json().get(
                                    "error", response.text
                                )
                            except Exception:
                                error_detail = response.text

                            st.error(
                                f"Batch API returned HTTP "
                                f"{response.status_code}: {error_detail}"
                            )

                    except requests.exceptions.RequestException as e:
                        st.error(
                            f"Unable to connect to the batch prediction API at "
                            f"{BACKEND_URL}: {e}"
                        )
        except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")

    else:
        st.info("Upload a CSV file to preview the data and start batch prediction.")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(
    """
    <br>
    <div style="text-align:center;color:#94a3b8;font-size:.78rem;padding:1rem 0;">
        SuperKart Sales Prediction Platform · Flask API + Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
