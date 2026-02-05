import streamlit as st
import sys
import os

# Ensure project root is in path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from phase1.data_loader import load_zomato_dataset
from phase3.logic import filter_restaurants
from phase4.groq_service import get_ai_recommendations

# Set page configuration
st.set_page_config(
    page_title="Zomato AI Recommendation",
    page_icon="🍽️",
    layout="centered"
)

# Custom CSS for Zomato styling
st.markdown("""
    <style>
    /* Smooth Navigation & Fade-in Effect */
    .main {
        background: linear-gradient(135deg, #f4f7f6 0%, #e9ecef 100%);
        animation: fadeIn 1.2s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    h1 {
        color: #cb202d;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .stButton>button {
        background-color: #cb202d;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(203, 32, 45, 0.2);
    }

    .stButton>button:hover {
        background-color: #a31822;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(203, 32, 45, 0.3);
    }

    /* Recommendation Box Faded Styling */
    .recommendation-box {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #cb202d;
        color: #2d3436;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        animation: slideIn 0.6s ease-out;
    }

    @keyframes slideIn {
        from { opacity: 0; clip-path: inset(0 0 100% 0); }
        to { opacity: 1; clip-path: inset(0 0 0 0); }
    }
    </style>
    """, unsafe_allow_html=True)

# Load dataset once
@st.cache_resource
def load_data():
    return load_zomato_dataset()

# Main application
st.title("🍽️ Zomato AI Restaurant Recommendation")
st.markdown("Find the best dining spots in Bangalore using AI")

# Load dataset
with st.spinner("Loading Zomato dataset..."):
    df = load_data()

if df is None or df.empty:
    st.error("Failed to load dataset. Please check your connection.")
    st.stop()

st.success(f"Dataset loaded successfully! {len(df)} restaurants available.")

# Input form
st.subheader("Enter Your Preferences")
col1, col2 = st.columns(2)

with col1:
    location = st.text_input("Location", placeholder="e.g., Banashankari, Indiranagar")

with col2:
    budget = st.number_input("Budget per person (₹)", min_value=0, step=50, value=500)

# Recommendation button
if st.button("Get Recommendation", type="primary"):
    if not location:
        st.warning("Please enter a location.")
    else:
        with st.spinner("Consulting Zomato AI..."):
            # Filter restaurants
            filtered_df = filter_restaurants(df, location, budget)
            
            if filtered_df.empty:
                st.warning("No restaurants found matching your criteria. Try a broader location or increase your budget.")
            else:
                st.info(f"Found {len(filtered_df)} matching restaurants. Generating AI recommendation...")
                
                # Get AI recommendation
                recommendation = get_ai_recommendations(filtered_df, {"location": location, "budget": budget})
                
                # Display recommendation
                st.subheader("AI Recommendation")
                st.markdown(f"""
                <div class="recommendation-box">
                {recommendation}
                </div>
                """, unsafe_allow_html=True)
