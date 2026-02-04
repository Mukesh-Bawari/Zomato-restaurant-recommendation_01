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
    .main {
        background-color: #f4f7f6;
    }
    h1 {
        color: #cb202d;
    }
    .stButton>button {
        background-color: #cb202d;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #a31822;
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
                <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border-left: 5px solid #cb202d; color: #333;">
                {recommendation}
                </div>
                """, unsafe_allow_html=True)
