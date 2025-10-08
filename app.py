import streamlit as st
import google.generativeai as genai
import time
import json
from datetime import datetime

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# DARK THEME CSS STYLING - ATTRACTIVE & MODERN
# -------------------------------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Headers */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .sub-header {
        font-size: 1.6rem;
        color: #ffd700;
        margin-bottom: 1rem;
        font-weight: 700;
        padding: 10px;
        background: rgba(255, 215, 0, 0.1);
        border-radius: 10px;
        border-left: 4px solid #ffd700;
    }
    
    /* Response Boxes */
    .response-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border: 2px solid #4fc3f7;
        box-shadow: 0 8px 32px rgba(79, 195, 247, 0.3);
        color: #e3f2fd;
        font-size: 16px;
        line-height: 1.7;
        backdrop-filter: blur(10px);
    }
    
    .user-query-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 2px solid #ff9ff3;
        color: #fff;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    
    /* Info and Metric Boxes */
    .info-box {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 2px solid #55efc4;
        color: #fff;
        box-shadow: 0 6px 20px rgba(0, 184, 148, 0.4);
    }
    
    .metric-box {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        border: 2px solid #fd79a8;
        color: #fff;
        box-shadow: 0 6px 20px rgba(253, 121, 168, 0.4);
    }
    
    .parameter-box {
        background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border: 2px solid #a29bfe;
        color: #fff;
        box-shadow: 0 6px 20px rgba(162, 155, 254, 0.4);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #2d3436;
        border-radius: 25px;
        padding: 14px 32px;
        border: none;
        font-weight: 700;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4);
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(255, 154, 158, 0.6);
        background: linear-gradient(135deg, #fecfef 0%, #ff9a9e 100%);
    }
    
    .secondary-button {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%) !important;
        color: white !important;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2d3436 0%, #1e272e 100%);
        border-right: 3px solid #ffd700;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #dfe6e9;
        font-size: 0.9rem;
        padding: 25px;
        background: rgba(45, 52, 54, 0.8);
        border-radius: 15px;
        border: 1px solid #636e72;
        backdrop-filter: blur(10px);
    }
    
    /* Messages */
    .success-message {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        border: 2px solid #55efc4;
        color: #fff;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(0, 184, 148, 0.4);
    }
    
    .error-message {
        background: linear-gradient(135deg, #e17055 0%, #d63031 100%);
        border: 2px solid #fab1a0;
        color: #fff;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
    }
    
    .warning-message {
        background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        border: 2px solid #ffeaa7;
        color: #2d3436;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(253, 203, 110, 0.4);
    }
    
    /* Progress and loading */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        background: rgba(45, 52, 54, 0.8);
        color: #dfe6e9;
        border: 2px solid #636e72;
        border-radius: 10px;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(45, 52, 54, 0.8);
        color: #dfe6e9;
        border: 2px solid #636e72;
        border-radius: 10px;
    }
    
    /* Select boxes */
    .stSelectbox > div > div > div {
        background: rgba(45, 52, 54, 0.8);
        color: #dfe6e9;
        border: 2px solid #636e72;
        border-radius: 10px;
    }
    
    /* Sliders */
    .stSlider > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #2d3436 0%, #1e272e 100%) !important;
        color: #ffd700 !important;
        border: 2px solid #636e72 !important;
        border-radius: 10px !important;
    }
    
    /* Chat history items */
    .chat-history-item {
        background: linear-gradient(135deg, #2d3436 0%, #1e272e 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #636e72;
        color: #dfe6e9;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR CONFIGURATION
# -------------------------------
with st.sidebar:
    st.markdown("### ⚡ Configuration")
    st.markdown("---")
    
    api_key = st.text_input("🔑 Enter your Gemini API Key", type="password", 
                           help="Get your API key from Google AI Studio",
                           placeholder="Paste your API key here...")
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.markdown('<div class="success-message">✅ API Key Configured</div>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div class="error-message">❌ Error: {e}</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 🚀 Model Settings")
    
    model_option = st.selectbox(
        "Select AI Model",
        ["gemini-2.0-flash", "gemini-pro", "gemini-1.5-flash"],
        index=0,
        help="Choose the Gemini model version"
    )
    
    # Important Parameters
    st.markdown("### 🎛️ Key Parameters")
    
    col_temp, col_tokens = st.columns(2)
    
    with col_temp:
        temperature = st.slider(
            "🔥 Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Controls creativity: Lower = more focused, Higher = more creative"
        )
    
    with col_tokens:
        max_tokens = st.slider(
            "📏 Max Tokens",
            min_value=50,
            max_value=2000,
            value=800,
            step=50,
            help="Maximum length of the response"
        )
    
    st.markdown("---")
    st.markdown("### ⚡ Active Settings")
    
    # Display current parameters
    st.markdown(f"""
    <div class="parameter-box">
    <h4 style='color: #fff; margin: 0;'>Current Configuration</h4>
    <div style='margin-top: 10px;'>
    🚀 <strong>Model:</strong> {model_option}<br>
    🔥 <strong>Temperature:</strong> {temperature}<br>
    📏 <strong>Max Tokens:</strong> {max_tokens}<br>
    🔑 <strong>API Status:</strong> {'✅ Active' if api_key else '❌ Inactive'}
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🌟 About")
    st.markdown("""
    <div class="info-box">
    <strong>Gemini AI Assistant</strong><br><br>
    Experience the power of AI with beautiful, responsive design and intelligent conversations about technology, space, economy, and more!
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# MAIN CONTENT
# -------------------------------
st.markdown('<div class="main-header">🚀 Prompt Engineering using Gemini </div>', unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "last_response" not in st.session_state:
    st.session_state.last_response = None

# -------------------------------
# SIMPLIFIED FUNCTIONS
# -------------------------------
def simple_retriever(query):
    """Simple context retriever"""
    knowledge_base = {
        "technology": "India is rapidly advancing in AI, semiconductor manufacturing, 5G/6G technology, and digital infrastructure through initiatives like Digital India and Make in India.",
        "economy": "India aims to become a $5 trillion economy by 2025-26 with focus on manufacturing, infrastructure development, and export growth.",
        "environment": "India is committed to renewable energy with 500 GW capacity target by 2030 and net-zero emissions by 2070 through massive solar and wind energy projects.",
        "space": "ISRO is planning Gaganyaan manned mission, Venus orbiter Shukrayaan-1, and developing reusable launch vehicles to reduce space access costs.",
        "default": "India is pursuing comprehensive development across all sectors with focus on technology innovation, economic growth, environmental sustainability, and space exploration."
    }
    
    query_lower = query.lower()
    if any(word in query_lower for word in ['tech', 'digital', 'ai', 'software', 'computer']):
        return knowledge_base["technology"]
    elif any(word in query_lower for word in ['economy', 'gdp', 'business', 'market']):
        return knowledge_base["economy"]
    elif any(word in query_lower for word in ['environment', 'climate', 'energy', 'green']):
        return knowledge_base["environment"]
    elif any(word in query_lower for word in ['space', 'isro', 'rocket', 'mission']):
        return knowledge_base["space"]
    else:
        return knowledge_base["default"]

def generate_response(query, model_name, temperature, max_tokens):
    """Generate AI response with error handling"""
    try:
        if not api_key:
            return "❌ Please enter your Gemini API key in the sidebar to get started."
        
        genai.configure(api_key=api_key)
        retrieved_info = simple_retriever(query)
        
        prompt = f"""
        Context: {retrieved_info}
        
        Question: {query}
        
        Please provide a comprehensive, well-structured response with relevant details and examples:
        """
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": 0.95,
                "top_k": 40,
            }
        )
        
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            return "❌ The model couldn't generate a response. Please try again with a different question."
            
    except Exception as e:
        return f"❌ Error: {str(e)}"

# -------------------------------
# MAIN INTERFACE
# -------------------------------
if api_key:
    # Create two columns for main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="sub-header">💬 Ask Your Question</div>', unsafe_allow_html=True)
        
        # Query examples
        query_examples = [
            "Tell me about India's space exploration plans",
            "What are India's economic growth targets?",
            "Explain India's digital transformation initiatives", 
            "Describe India's environmental and climate goals",
            "What is India's plan for AI development?",
            "How is India developing its semiconductor industry?"
        ]
        
        example_choice = st.selectbox("🎯 Choose a sample question:", 
                                    ["Select an example..."] + query_examples)
        
        user_query = st.text_area(
            "✨ Or write your own question:",
            value=example_choice if example_choice != "Select an example..." else "",
            height=120,
            placeholder="Ask me anything about India's development in technology, economy, space, environment..."
        )
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])
        with col_btn1:
            generate_clicked = st.button("🚀 Generate Response", use_container_width=True, type="primary")
        with col_btn2:
            clear_clicked = st.button("🗑️ Clear History", use_container_width=True)
        
        if clear_clicked:
            st.session_state.messages = []
            st.session_state.query_count = 0
            st.session_state.last_response = None
            st.markdown('<div class="success-message">🗑️ Chat history cleared!</div>', unsafe_allow_html=True)
            st.rerun()
        
        # Handle response generation
        if generate_clicked:
            if not user_query.strip():
                st.markdown('<div class="warning-message">⚠️ Please enter a question first.</div>', unsafe_allow_html=True)
            else:
                # Create containers for response
                response_container = st.container()
                
                with st.spinner("🔮 Analyzing your question with AI magic..."):
                    # Progress animation
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    steps = [
                        "🌌 Initializing AI...",
                        "🔍 Analyzing question...", 
                        "📚 Gathering knowledge...",
                        "✨ Generating response...",
                        "🎉 Finalizing..."
                    ]
                    
                    for i, step in enumerate(steps):
                        progress = (i + 1) * 20
                        progress_bar.progress(progress)
                        status_text.text(f"{step} {progress}%")
                        time.sleep(0.3)
                    
                    # Generate response
                    start_time = time.time()
                    answer = generate_response(user_query, model_option, temperature, max_tokens)
                    response_time = time.time() - start_time
                    
                    # Store response
                    st.session_state.last_response = {
                        "query": user_query,
                        "answer": answer,
                        "response_time": response_time,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "model": model_option,
                        "temperature": temperature
                    }
                    
                    st.session_state.messages.append(st.session_state.last_response)
                    st.session_state.query_count += 1
                    
                    # Complete progress
                    progress_bar.progress(100)
                    status_text.text("✅ Response Ready!")
                    time.sleep(0.5)
                
                # Clear progress
                progress_bar.empty()
                status_text.empty()
                
                # Display response
                with response_container:
                    if st.session_state.last_response:
                        response_data = st.session_state.last_response
                        
                        # User query
                        st.markdown("### 👤 Your Question")
                        st.markdown(f'<div class="user-query-box">{response_data["query"]}</div>', unsafe_allow_html=True)
                        
                        # AI response
                        st.markdown("### 🤖 AI Response")
                        if response_data["answer"].startswith("❌"):
                            st.markdown(f'<div class="error-message">{response_data["answer"]}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="response-box">{response_data["answer"]}</div>', unsafe_allow_html=True)
                            st.markdown('<div class="success-message">✨ Response generated successfully!</div>', unsafe_allow_html=True)
                        
                        # Metrics
                        st.markdown("### 📊 Performance Metrics")
                        col1, col2, col3, col_4 = st.columns(4)
                        with col1:
                            st.markdown(f'<div class="metric-box"><h4>⚡ Speed</h4><h3>{response_data["response_time"]:.2f}s</h3></div>', unsafe_allow_html=True)
                        with col2:
                            st.markdown(f'<div class="metric-box"><h4>🤖 Model</h4><h3>{response_data["model"].split("-")[0]}</h3></div>', unsafe_allow_html=True)
                        with col3:
                            st.markdown(f'<div class="metric-box"><h4>🔥 Temp</h4><h3>{response_data["temperature"]}</h3></div>', unsafe_allow_html=True)
                        with col_4:
                            st.markdown(f'<div class="metric-box"><h4>📈 Total</h4><h3>{st.session_state.query_count}</h3></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="sub-header">📊 Dashboard</div>', unsafe_allow_html=True)
        
        # Statistics
        st.markdown("### 📈 Session Stats")
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.metric("🚀 Questions Asked", st.session_state.query_count)
        st.metric("🤖 Active Model", model_option)
        st.metric("🔥 Temperature", f"{temperature}")
        st.metric("📏 Max Tokens", max_tokens)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        st.markdown("""
        <div class="parameter-box">
        <strong>💡 Pro Tips:</strong><br><br>
        • Use specific questions for better answers<br>
        • Adjust temperature for creativity<br>
        • Try different sample questions<br>
        • Check response metrics for insights
        </div>
        """, unsafe_allow_html=True)
        
        # Recent Activity
        if st.session_state.messages:
            st.markdown("### 🔄 Recent Activity")
            for i, msg in enumerate(list(reversed(st.session_state.messages))[:3]):
                with st.expander(f"💬 {msg['query'][:40]}...", expanded=False):
                    st.markdown(f"**⏰ Time:** {msg['timestamp']}")
                    st.markdown(f"**🤖 Model:** {msg['model']}")
                    st.markdown(f"**⚡ Speed:** {msg['response_time']:.2f}s")
                    st.markdown("**📝 Response:**")
                    st.markdown(f"<div style='color: #b2bec3; font-size: 14px;'>{msg['answer'][:150]}...</div>", unsafe_allow_html=True)

else:
    # Welcome screen
    st.markdown("""
    <div style='text-align: center; padding: 50px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin: 20px 0; border: 3px solid #ffd700;'>
        <h1 style='color: #ffd700; margin-bottom: 20px; font-size: 3rem;'>🚀 Welcome to Gemini AI</h1>
        <p style='font-size: 1.4rem; color: #fff; margin-bottom: 30px;'>
            Your Gateway to Intelligent Conversations
        </p>
        <div style='font-size: 1.1rem; color: #dfe6e9;'>
            Enter your API key in the sidebar to unlock the power of AI
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 25px; border-radius: 15px; border: 2px solid #ff9ff3; text-align: center; height: 200px;'>
            <h3 style='color: #fff;'>🔮 Smart AI</h3>
            <p style='color: #fff;'>Powered by Google's Gemini for intelligent, contextual responses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #00b894 0%, #00a085 100%); padding: 25px; border-radius: 15px; border: 2px solid #55efc4; text-align: center; height: 200px;'>
            <h3 style='color: #fff;'>🎨 Beautiful UI</h3>
            <p style='color: #fff;'>Stunning dark theme with gradient colors and smooth animations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); padding: 25px; border-radius: 15px; border: 2px solid #81ecec; text-align: center; height: 200px;'>
            <h3 style='color: #fff;'>⚡ Fast & Responsive</h3>
            <p style='color: #fff;'>Lightning-fast responses with real-time progress tracking</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown(
    '<div class="footer">'
    '✨ Built with Tanmay using Streamlit + Google Gemini API | '
    f' | '
    '🚀 Experience the Future of AI'
    '</div>', 
    unsafe_allow_html=True
)