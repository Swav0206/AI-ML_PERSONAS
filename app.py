import streamlit as st
import time
from router import route_post
from generator import generate_post
from defense import generate_reply
from data.personas import bots

# Must be the first Streamlit command
st.set_page_config(
    page_title="AI Cognitive Bot System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for glassmorphism and modern UI
st.markdown("""
<style>
    /* Dark theme background */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #58a6ff, #a371f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .sub-header {
        text-align: center;
        color: #8b949e;
        font-size: 1.1rem;
        margin-bottom: 40px;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Glassmorphism for containers and inputs */
    div[data-testid="stTextInput"] > div > div > input,
    div[data-testid="stTextArea"] > div > div > textarea,
    div[data-testid="stSelectbox"] > div > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 8px;
    }

    /* Buttons styling */
    div.stButton > button {
        background: linear-gradient(135deg, #1f6feb 0%, #3fb950 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 111, 235, 0.4);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Main Title
st.markdown("<div class='main-header'>🤖 AI Cognitive Bot System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Agentic workflow for social media routing, generation, and defense</div>", unsafe_allow_html=True)

# Layout using Tabs
tab1, tab2, tab3 = st.tabs(["📌 Phase 1: Route Post", "📝 Phase 2: Generate Post", "⚔️ Phase 3: Defense & Reply"])

with tab1:
    st.markdown("### Match a human post to the most relevant AI bot")
    post = st.text_area("Enter a post from a user to analyze:", height=100, placeholder="E.g., Crypto is taking over the world and AI will help scale it.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Route Post"):
            if not post.strip():
                st.warning("Please enter a post to route.")
            else:
                with st.spinner("Analyzing intent and routing..."):
                    time.sleep(1) # Fake delay for UX
                    result = route_post(post)
                
                if result:
                    st.success("Analysis Complete!")
                    st.markdown("#### Matched Bots & Confidence Scores")
                    cols = st.columns(len(result))
                    for idx, (bot_name, score) in enumerate(result):
                        cols[idx].metric(label=f"Bot {bot_name}", value=f"{score*100}%", delta="High Match" if score > 0.5 else "Low Match", delta_color="normal" if score > 0.5 else "off")
                else:
                    st.info("No bots confidently matched this post's intent.")

with tab2:
    st.markdown("### Generate a persona-driven social media post")
    
    # Store bot choice in session state to link tabs visually if needed, but simple is fine for now.
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        bot_choice = st.selectbox("Select Bot Persona", list(bots.keys()), index=0)
        st.info(f"**Current Persona:**\\n{bots[bot_choice]}")
        
    with col_b:
        topic_input = st.text_input("Enter a Topic or Context:", placeholder="E.g., The future of AI in finance")
        if st.button("✨ Generate Post"):
            if not topic_input.strip():
                st.warning("Please enter a topic to generate a post.")
            else:
                with st.spinner(f"Bot {bot_choice} is writing..."):
                    output = generate_post(bot_choice, bots[bot_choice], topic_input)
                
                st.markdown("#### Generated Post:")
                with st.chat_message("ai", avatar="🤖"):
                    st.write(output.get("post_content", ""))
                
                with st.expander("View Raw Output Metadata"):
                    st.json(output)

with tab3:
    st.markdown("### Test the bot's defensive capabilities against arguments")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        def_bot_choice = st.selectbox("Select Defending Bot", list(bots.keys()), key="def_bot")
        st.info(f"**Bot Persona:**\\n{bots[def_bot_choice]}")
        parent_post = st.text_area("Parent Post (Original Context)", height=80, placeholder="The original post that started the thread...")
        
    with col_right:
        comment_history = st.text_area("Comment History", height=80, placeholder="Previous replies in the thread...")
        human_reply = st.text_area("Human Reply (The Argument)", height=80, placeholder="You are wrong because...")

    if st.button("🛡️ Generate Defense Reply"):
        if not human_reply.strip() or not parent_post.strip():
            st.warning("Please provide at least the Parent Post and Human Reply.")
        else:
            with st.spinner("Analyzing argument and formulating defense..."):
                reply = generate_reply(
                    bots[def_bot_choice],
                    parent_post,
                    comment_history,
                    human_reply
                )
            
            st.markdown("#### Bot's Response:")
            with st.chat_message("human", avatar="👤"):
                st.write(f"**Human:** {human_reply}")
            with st.chat_message("ai", avatar="🤖"):
                st.write(f"**Bot {def_bot_choice}:** {reply}")