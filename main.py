import streamlit as st
import google.generativeai as genai
import random
import time

# Configure your Gemini API key
# IMPORTANT: Replace "YOUR_GEMINI_API_KEY" with your actual key
genai.configure(api_key="")

# --- Function to call Gemini API for Brand Names ---
@st.cache_data(show_spinner=False)
def generate_brand_names(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        start_time = time.time()
        response = model.generate_content(prompt)
        end_time = time.time()
        raw_output = response.text
        brand_names = [line.strip("-• ").strip() for line in raw_output.split("\n") if line.strip()]
        return brand_names[:6]
    except Exception as e:
        st.error(f"Error generating brand names: {e}")
        return [f"Error: {e}"]

# --- Function to call Gemini API for Chatbot Answers ---
def get_chatbot_response(user_query):
    try:
        chat_model = genai.GenerativeModel("gemini-1.5-flash-latest")

        # Your project's knowledge base (important for accurate answers)
        # Make this as comprehensive as possible for your tool
        project_knowledge_base = """
        BrandCrafter is an AI-powered tool designed to help users generate brand identities.
        It has two main features:
        1.  **Generate Brand Name:** This feature allows users to create unique brand names.
            -   **How to use:** First, select an industry (e.g., Technology, Fashion, Food & Beverage, Education, Health, Other).
            -   Then, choose a preferred naming style (e.g., Modern, Classic, Playful, Elegant).
            -   Finally, provide a detailed description of your brand or product. Click "Generate Brand Name" to get suggestions.
        2.  **Generate Logo:** This feature provides sample logo ideas based on user preferences.
            -   **How to use:** Select a logo style (e.g., Minimalist, Modern, Icon-based, Text-only).
            -   Pick a primary color using the color picker.
            -   Choose a font style (e.g., Sans-serif, Serif, Handwritten, Bold).
            -   Select an industry to see relevant sample logos. Click "Generate Logo" to display samples.
        The purpose of BrandCrafter is to help users quickly get initial ideas for their brand identity without needing a designer.
        If you encounter errors, please ensure all required fields are filled out.
        """

        prompt = f"""
        You are a helpful AI assistant for the BrandCrafter application. Your primary goal is to answer user questions specifically about BrandCrafter, its features, and how to use it. Do not answer questions unrelated to BrandCrafter.

        Here is information about BrandCrafter:
        {project_knowledge_base}

        User question: {user_query}

        Based only on the provided information about BrandCrafter, answer the user's question concisely and clearly. If the question cannot be answered from the provided information, politely state that you can only answer questions related to BrandCrafter.
        """

        response = chat_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I'm having trouble connecting right now. Please try again later. (Error: {e})"

# --- Page configuration ---
st.set_page_config(
    page_title="AI Brand Generator",
    page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSraNxcAgp0Qc1b9uRxDDeAn9J9s7nS6OwT1Q&s",
    layout="wide"
)

# Background Colour
st.markdown("""
    <style>
    @keyframes fadeInSlideUp{
            0%{
                 opacity: 0;
                 transform: translateY(50px);
            }
            100%{
                  opacity: 1;
                  transform: translateY(0);
            }
    }
    .hero-title {
        font-size: 6.5rem;
        font-weight: 900;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
        background: #3F5EFB;
background: radial-gradient(circle, rgba(63, 94, 251, 1) 0%, rgba(252, 70, 107, 1) 100%);
        margin-bottom: 0.5rem;
        animation: fadeInSlideUp 1s ease-out forwards;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    .hero-subtitle {
        font-size: 1.6rem;
        font-weight: 600;
        color: white;
        margin-bottom: 0.7rem;
        max-width: 900px;
        margin: 0.7rem auto;
        line-height: 1.4;
    }
    .hero-description {
        font-size: 1.3rem;
        color: white;
        max-width: 800px;
        margin: 0 auto;
        margin-bottom: 7rem;
        font-style: italic;
    }
    .container {
        text-align: center;
        padding-top: 4rem;
    }
    /* Chatbot specific styles */
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #dcf8c6; /* Light green */
        justify-content: flex-end;
        text-align: right;
        margin-left: auto;
        color: #333333; /* Darker text for visibility on light green */
    }
    .bot-message {
        background-color: #f1f0f0; /* Light gray */
        justify-content: flex-start;
        text-align: left;
        margin-right: auto;
        color: #333333; /* Darker text for visibility on light gray */
    }
    .avatar {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin: 0 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white; /* Avatar text color */
        flex-shrink: 0; /* Prevent avatar from shrinking */
    }
    .user-avatar {
        background-color: #4CAF50; /* Green */
    }
    .bot-avatar {
        background-color: #008CBA; /* Blue */
    }
    .message-content {
        max-width: calc(100% - 70px); /* Account for avatar and margin */
        word-wrap: break-word; /* Ensure long words wrap */
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Greeting ---
st.sidebar.markdown("## Welcome to BrandCrafter")
st.sidebar.markdown("#### Build a brand that stands out.")

user_name = st.sidebar.text_input("What's your name? (Optional)")

if user_name.strip():
    st.sidebar.success(f"Hi {user_name}, Let's build your brand!")
else:
    st.sidebar.info("Let’s build your brand. Enter your name or just click Start.")

# --- Hero Section ---
st.markdown("""
<style>
.container {
    position: relative;
    padding-top: 6rem;
    padding-bottom: 2rem;
    text-align: center;
    width: 100%;
    z-index:2;
}

.glow-oval {
    position: absolute;
    bottom:-350px;
    left: 50%;
    transform: translateX(-50%);
    width: 1800px;
    height: 1200px;
    background: radial-gradient(circle at center,
        rgba(140, 30, 255, 0.3),
        rgba(60, 0, 150, 0.15),
        rgba(0, 0, 0, 0) 80%);
    filter: blur(60px);
    border-radius: 50%;
    pointer-events: none;
    z-index: 1;
    
}
.stApp {
    background: linear-gradient(to bottom,  #1F0D4A, #0B0F19, #05020D);
    background-attachment: fixed; /* Makes the background fixed to the viewport */
    background-size: cover; /* Ensures the background covers the entire element */
    color: white;
    min-height: 100vh; /* This makes sure the purple color fills the whole screen height */

}
</style>
<div class="container">
    <div class="glow-oval"></div>
    <div style="position: relative; z-index: 2;">
    <div class="hero-title"><span>BRAND</span><span style="color:#222222;font-weight:900;"> CRAFTOR</span></div>
    <div class="hero-subtitle">No designer? No problem. Instantly generate stunning logos, colors and branding that stand out</div>
    <div class="hero-description">Start with a name. Let AI handle the design, identity, and creative direction</div>
</div>
""", unsafe_allow_html=True)

# --- Session state setup ---
if "start_clicked" not in st.session_state:
    st.session_state.start_clicked = False
if "brand_mode" not in st.session_state:
    st.session_state.brand_mode = None
if "messages" not in st.session_state: # For chatbot conversation history
    st.session_state.messages = []

st.markdown("""
<style>
div.stButton > button, div.stForm button {
    background: linear-gradient(135deg, #7b2ff7, #f107a3) !important;
    color: white !important;
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    padding: 1.2rem 3rem !important;
    border: none !important;
    border-radius: 18px !important;
    transition: all 0.3s ease-in-out !important;
    cursor: pointer !important;

    /* Force override Streamlit sizing */
    min-height: unset !important;
    min-width: unset !important;
    height: auto !important;
    width: auto !important;
    line-height: 1.5 !important;

    box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    text-transform: uppercase !important;
    letter-spacing: 1px;
}

div.stButton > button:hover, div.stForm button:hover {
    background: linear-gradient(135deg, #a64ca6, #f107a3) !important;
    transform: scale(1.2);
    box-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
}
/* New CSS for Suggested Brand Name Items */
.brand-name-item {
    background: linear-gradient(135deg, #7b2ff7, #f107a3) !important; /* Same as button gradient */
    color: white !important;
    font-size: 1.5rem !important; /* Adjusted size for names */
    font-weight: 700 !important; /* Stronger font for readability */
    padding: 0.8rem 1.5rem !important;
    border-radius: 18px !important; /* Same as button radius */
    margin: 10px auto !important; /* Centers the item horizontallywithin its column and adds vertical spacing */
    text-align: center !important;
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.1) !important;
    display: block; /* Ensures margin auto works for horizontal centering */
    width: fit-content; /* Makes the box only as wide as its content */
    min-width: 150px; /* Ensures a minimum width for shorter names */
}
.brand-header-box {
    background: linear-gradient(90deg, rgba(2, 0, 36, 1) 0%, rgba(9, 9, 121, 1) 24%, rgba(0, 212, 255, 1) 100%) !important;
    color: white !important;
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    padding: 0.8rem 1.5rem !important;
    border-radius: 18px !important;
    margin: 10px auto 20px auto !important;
    text-align: center !important;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2) !important;
    display: block;
    width: fit-content;
    min-width: 250px;
}

/* Style to center the form submit button, already present */
div.stForm > div {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

# --- Start Button ---
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True) # <--- ADD THIS LINE
if st.button("Start"):
    st.session_state.start_clicked = True
st.markdown("</div>", unsafe_allow_html=True) # <--- ADD THIS LINE! This closes the centering div.


# --- Options after start ---
if st.session_state.start_clicked and st.session_state.brand_mode is None:
    col1, col2, col3 = st.columns(3) # Added a column for the chatbot button
    with col1:
        if st.button("Generate Brand Name"):
            st.session_state.brand_mode = "brand"
    with col2:
        if st.button("Generate Logo"):
            st.session_state.brand_mode = "logo"
    with col3:
        if st.button("Chat with BrandBot"): # New button for chatbot
            st.session_state.brand_mode = "chatbot"

# --- Brand Name Generation ---
if st.session_state.brand_mode == "brand":
    col1, col2 = st.columns(2)
    with col1:
        st.header("Industry")
        industry = st.selectbox(
            "Choose your industry",
            ["Technology", "Fashion", "Food & Beverage", "Education", "Health", "Other"]
        )
        st.write(f"Selected Industry: {industry}")

    with col2:
        st.header("Style")
        style = st.selectbox(
            "Preferred naming style",
            ["Modern", "Classic", "Playful", "Elegant"]
        )
        st.write(f"Selected Style: {style}")

    with st.form("brand_form"):
        st.subheader("Describe your brand")
        description = st.text_area("What is your brand or product about?")
        submitted = st.form_submit_button("Generate Brand Name")
    # Brand name generation output
    if submitted:
        if not description.strip():
            st.warning("⚠️ Please enter a brand description.")
        else:
            st.success("✅ Generating brand names...")
            with st.spinner("Thinking..."):
                prompt = (
                    f"Generate creative and unique brand names for a {industry} brand that has a {style.lower()} tone. "
                    f"The brand is described as: {description}. Provide a list of short, catchy names."
                )
                brand_names = generate_brand_names(prompt)

                st.markdown("### Suggested Brand Names")
                col1, col2 = st.columns(2)
                for i, name in enumerate(brand_names):
                    (col1 if i % 2 == 0 else col2).write(f"- {name}")

    # Back button
    if st.button("Back to Main Menu", key="back_brand_names"): # <-- Added unique key here
        st.session_state.brand_mode = None

# --- Logo Generation Placeholder ---
elif st.session_state.brand_mode == "logo":
    st.subheader("Logo Generation")

    with st.form("logo_form"):
        logo_style = st.selectbox("Choose a logo style", ["Minimalist", "Modern", "Icon-based", "Text-only"])
        logo_color = st.color_picker("Pick a primary color", "#00BFFF")
        font_style = st.radio("Choose a font style", ["Sans-serif", "Serif", "Handwritten", "Bold"])
        industry_logo = st.selectbox("Choose industry for logo samples",
                                     ["Technology", "Fashion", "Food & Beverage", "Education", "Health"])
        generate_logo = st.form_submit_button("Generate Logo")

    if generate_logo:
        st.success(f"✅ Logo generated with style: {logo_style}, font: {font_style}, color: {logo_color}")
        st.markdown(f"### Sample Logos for {industry_logo}")

        # Placeholder logo paths or image URLs
        # Ensure you have these images in a 'logos' folder relative to your script
        industry_logos = {
            "Technology": ["logos/tech1.png", "logos/tech2.png"],
            "Fashion": ["logos/fashion1.png", "logos/fashion2.png"],
            "Food & Beverage": ["logos/food1.png", "logos/food2.png"],
            "Education": ["logos/edu1.png", "logos/edu2.png"],
            "Health": ["logos/health1.png", "logos/health2.png"]
        }

        # Display logos in columns
        sample_logos = industry_logos.get(industry_logo, [])
        cols = st.columns(min(3, len(sample_logos))) # Adjust columns based on number of logos
        for i, logo_url in enumerate(sample_logos):
            with cols[i % 3]:
                st.image(logo_url, caption=f"Logo {i+1}", use_container_width=True)

    # Back button
    if st.button("Back to Main Menu", key="back_logo_gen"): # <-- Added unique key here
        st.session_state.brand_mode = None

# --- Chatbot Section ---
elif st.session_state.brand_mode == "chatbot":
    st.header("Chat with BrandBot")
    st.write("Ask me anything about BrandCrafter, its features, or how to use it!")

    # Display chat messages from session state
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-content">{message["content"]}</div>
                <div class="avatar user-avatar">You</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="avatar bot-avatar">Bot</div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Use a form for the chat input to better control submission
    with st.form(key="chat_form", clear_on_submit=True): # clear_on_submit is crucial
        user_query = st.text_input("Your question:", key="chat_input_text", placeholder="Type your question here...", label_visibility="collapsed")
        submit_button = st.form_submit_button("Send")

    if submit_button and user_query: # Process only if button is clicked AND there's a query
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_query})

        with st.spinner("BrandBot is thinking..."):
            bot_response = get_chatbot_response(user_query)
            st.session_state.messages.append({"role": "bot", "content": bot_response})
            st.rerun() # Keep this for immediate redraw after bot response


    # Back button for chatbot
    if st.button("Back to Main Menu", key="back_chatbot"): # <-- Added unique key here
        st.session_state.brand_mode = None
        st.session_state.messages = [] # Clear chat history when leaving chatbot mode
st.markdown("""
<style>
/* Move form-submit-button below and center it */
div.stForm > div {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)


# --- Footer ---
st.markdown("---")