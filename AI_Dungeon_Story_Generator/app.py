import streamlit as st
import random
from datetime import datetime

# Set page config
st.set_page_config(page_title="AI Dungeon", layout="wide")
st.title("🎭 AI Dungeon: Interactive Story Generator")

# Genre templates with story starters
genres = {
    "Fantasy": {
        "starters": [
            "In a land of magic and mystery, a young adventurer stumbles upon",
            "Deep in the enchanted forest, there lies a hidden",
            "The dragon's lair trembles as a mysterious figure approaches",
            "In the kingdom of Eldoria, an ancient prophecy awakens when"
        ],
        "continuations": [
            "a glowing artifact that pulses with ancient power",
            "a map leading to the lost city of gold",
            "an old mentor who reveals the truth about their past",
            "an unexpected ally with magical abilities",
            "a cursed treasure that grants wishes",
            "a portal to another realm"
        ]
    },
    "Mystery": {
        "starters": [
            "A detective arrives at the crime scene where",
            "In the shadows of the city, a private investigator discovers",
            "An old letter arrives with a cryptic message:",
            "The truth behind the disappearance becomes clear when"
        ],
        "continuations": [
            "nothing is as it seems",
            "the witness tells an impossible story",
            "evidence points to someone unexpected",
            "a hidden connection emerges",
            "the perpetrator has been right there all along",
            "secrets from the past resurface"
        ]
    },
    "Sci-Fi": {
        "starters": [
            "In the year 2847, a space explorer encounters",
            "On a distant planet, scientists discover evidence of",
            "A rogue AI awakens with one mission:",
            "The colony ship detects an anomaly in"
        ],
        "continuations": [
            "an alien intelligence unlike anything known",
            "technology far beyond their understanding",
            "a temporal distortion",
            "an extinct civilization's warning",
            "a source of unlimited energy",
            "a signal from the past"
        ]
    },
    "Horror": {
        "starters": [
            "Something moves in the darkness, and",
            "The old mansion holds a terrible secret:",
            "Reality begins to crack when",
            "In the abandoned hospital, footsteps echo as"
        ],
        "continuations": [
            "it's not what it appears to be",
            "the horror is closer than expected",
            "the boundaries between worlds grow thin",
            "survival becomes impossible",
            "madness spreads like a plague",
            "a curse awakens"
        ]
    },
    "Adventure": {
        "starters": [
            "The expedition embarks on a quest to find",
            "Against impossible odds, a team of adventurers seeks",
            "A treasure map leads to",
            "On the horizon, the lost civilization beckons with"
        ],
        "continuations": [
            "the greatest treasure ever known",
            "their ultimate destiny",
            "dangers they never imagined",
            "allies from unexpected places",
            "a challenge that will change everything",
            "the answer to an ancient riddle"
        ]
    }
}

# Sidebar controls
st.sidebar.header("📖 Story Controls")
selected_genre = st.sidebar.selectbox("Choose Genre:", list(genres.keys()), key="genre")

# Initialize session state for story history
if "story" not in st.session_state:
    st.session_state.story = ""
if "history" not in st.session_state:
    st.session_state.history = []

# Main story area
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader(f"📝 Your {selected_genre} Story")
    
    # Display current story
    story_display = st.empty()
    if st.session_state.story:
        story_display.write(st.session_state.story)
    else:
        story_display.info("Start your story by clicking a button below!")

# Control buttons
st.subheader("🎮 Story Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🚀 Start New Story"):
        starter = random.choice(genres[selected_genre]["starters"])
        st.session_state.story = starter
        st.session_state.history = [starter]
        st.rerun()

with col2:
    if st.button("📖 Continue Story"):
        if st.session_state.story:
            continuation = random.choice(genres[selected_genre]["continuations"])
            st.session_state.story += " " + continuation
            st.session_state.history.append(continuation)
            st.rerun()
        else:
            st.warning("Start a story first!")

with col3:
    if st.button("🔄 Random Twist"):
        if st.session_state.story:
            twists = [
                " Suddenly, something unexpected happens...",
                " But then, reality shifts...",
                " At that moment, everything changes...",
                " However, a new threat emerges...",
                " Just when all seems lost...",
                " The truth is revealed...",
                " An ancient force awakens...",
                " A mysterious figure appears..."
            ]
            twist = random.choice(twists)
            st.session_state.story += twist
            st.session_state.history.append(twist)
            st.rerun()
        else:
            st.warning("Start a story first!")

with col4:
    if st.button("🗑️ Clear Story"):
        st.session_state.story = ""
        st.session_state.history = []
        st.rerun()

# Custom continuation input
st.subheader("✍️ Write Your Own Continuation")
user_input = st.text_input("Add your own text to the story:")

if st.button("Add My Text"):
    if user_input.strip() and st.session_state.story:
        st.session_state.story += " " + user_input.strip()
        st.session_state.history.append(user_input.strip())
        st.rerun()
    elif not st.session_state.story:
        st.warning("Start a story first!")

# Sidebar: Story management
with st.sidebar:
    st.divider()
    st.header("💾 Story Management")
    
    # Save story
    if st.session_state.story:
        story_filename = f"story_{selected_genre}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download Story"):
                st.download_button(
                    label="Download TXT",
                    data=st.session_state.story,
                    file_name=story_filename,
                    mime="text/plain"
                )
        
        with col2:
            if st.button("📋 Copy to Clipboard"):
                st.success("Story copied! (Use Ctrl+V to paste)")
    
    st.divider()
    st.header("📊 Story Stats")
    if st.session_state.story:
        word_count = len(st.session_state.story.split())
        char_count = len(st.session_state.story)
        st.metric("Words", word_count)
        st.metric("Characters", char_count)
        st.metric("Continuations", len(st.session_state.history) - 1)

# Story history/log
with st.sidebar:
    if st.session_state.history:
        st.divider()
        st.header("📜 Build Log")
        for i, part in enumerate(st.session_state.history):
            truncated = part[:50] + "..." if len(part) > 50 else part
            st.caption(f"**Step {i+1}:** {truncated}")

# Footer
st.divider()
st.markdown("""
**Tips for Better Stories:**
- 🎲 Use "Random Twist" to get unexpected turns
- ✍️ Write your own continuations for custom plots
- 🎭 Try different genres for variety
- 📥 Download your completed stories
- 🔄 Mix automatic and manual storytelling
""")