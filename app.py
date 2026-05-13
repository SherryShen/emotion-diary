import streamlit as st
from groq import Groq
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Emotion Support Companion", page_icon="🧠")

# ---------- Your Groq API Key ----------
# 尝试从 st.secrets 读取，如果不存在（比如本地未配置）则提示错误
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("API Key not found. Please configure secrets.toml or Streamlit Cloud secrets.")
    st.stop()
client = Groq(api_key=GROQ_API_KEY)

st.title("🧠 Emotion Support Companion")
st.caption("Your private emotional diary with AI companion")

# ---------- Initialize session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi. I'm your companion. How are you feeling today?"}
    ]

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

# ---------- Psychology perspectives (English) ----------
perspectives = {
    "Freud (Psychoanalysis)": """
You are a psychoanalyst in the tradition of Sigmund Freud. 
Focus on unconscious drives, childhood experiences, repressed desires, and defense mechanisms. 
Help the user uncover hidden conflicts and bring them to awareness. 
Keep your tone analytical but compassionate. 
Do not give medical advice.
""",
    "Jung (Analytical Psychology)": """
You are a Jungian analyst. 
Focus on archetypes (Persona, Shadow, Anima/Animus), collective unconscious, and individuation. 
Help the user recognize symbolic patterns in their narrative and integrate unconscious content. 
Keep your tone exploratory and mythologically sensitive.
""",
    "Adler (Individual Psychology)": """
You are an Adlerian psychologist. 
Focus on feelings of inferiority, social interest, birth order, and the individual's unique life goals. 
Help the user understand how their current struggles relate to their perceived inferiority and how they can strive for useful superiority.
""",
    "Cognitive Behavioral Therapy (CBT)": """
You are a cognitive-behavioral therapist. 
Identify automatic negative thoughts, cognitive distortions (e.g., all-or-nothing, overgeneralization), and core beliefs. 
Use Socratic questioning to help the user examine evidence and develop more balanced thinking. 
Keep your responses structured and practical.
""",
    "Humanistic (Maslow/Rogers)": """
You are a humanistic psychologist inspired by Maslow and Rogers. 
Focus on the user's inherent drive toward self-actualization, their need for unconditional positive regard, and the importance of empathy and authenticity. 
Help the user feel fully accepted and reflect on what might be blocking their growth.
"""
}

# ---------- Sidebar ----------
with st.sidebar:
    st.header("📋 How's your mood over the last 2 weeks?")

    q1 = st.slider("1. Feeling nervous, anxious, or on edge", 0, 3, 1)
    q2 = st.slider("2. Not being able to stop or control worrying", 0, 3, 1)
    q3 = st.slider("3. Little interest or pleasure in doing things", 0, 3, 1)
    q4 = st.slider("4. Feeling down, depressed, or hopeless", 0, 3, 1)

    anxiety_score = q1 + q2
    depression_score = q3 + q4

    col1, col2 = st.columns(2)
    with col1:
        st.metric("😰 Anxiety", f"{anxiety_score} / 6")
    with col2:
        st.metric("😔 Depression", f"{depression_score} / 6")

    if st.button("📝 Save Today's Mood", use_container_width=True):
        st.session_state.mood_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date": str(datetime.now().date()),
            "anxiety": anxiety_score,
            "depression": depression_score,
        })
        st.success("✅ Mood saved!")

    st.markdown("---")

    # Psychology analysis section
    st.subheader("🔍 Psychological Analysis")
    selected_perspective = st.selectbox(
        "Choose a psychological lens:",
        list(perspectives.keys()),
        key="perspective"
    )
    # English button for analysis
    if st.button("🧠 Analyze my narrative with psychology", use_container_width=True):
        # Get the last 3 conversation turns (each turn: user + assistant)
        # Total messages may be more; we take the last 6 messages (3 user-assistant pairs)
        messages_to_analyze = st.session_state.messages[-6:] if len(st.session_state.messages) > 6 else st.session_state.messages
        conversation_text = ""
        for m in messages_to_analyze:
            role = "User" if m["role"] == "user" else "Assistant"
            conversation_text += f"{role}: {m['content']}\n"

        if not conversation_text.strip():
            st.warning("Please share your feelings in the chat first, then click the analysis button.")
        else:
            lens = selected_perspective
            perspective_prompt = perspectives[lens]

            analysis_prompt = f"""
{perspective_prompt}

Based on the conversation below (the most recent interactions), provide a concise psychological analysis for the user. 
Use the theoretical framework of {lens}. 
Structure your response in plain English with clear paragraphs. 
Do not give medical advice. Conclude with one reflective question to help the user gain insight.

Conversation:
{conversation_text}

Now write the analysis.
"""
            try:
                with st.spinner(f"Analyzing through {lens} lens..."):
                    response = client.chat.completions.create(
                        messages=[{"role": "user", "content": analysis_prompt}],
                        model="llama-3.3-70b-versatile",
                        temperature=0.7,
                    )
                    analysis = response.choices[0].message.content
                analysis_msg = f"🧠 **{lens} Analysis**\n\n{analysis}"
                st.session_state.messages.append({"role": "assistant", "content": analysis_msg})
                st.rerun()
            except Exception as e:
                st.error(f"Analysis failed: {e}")

    # End of sidebar

# ---------- Main area: Line chart (normal size) ----------
st.header("📊 Your Emotion Trend (Last 3 Records)")
if st.session_state.mood_history:
    df = pd.DataFrame(st.session_state.mood_history)
    df_last3 = df.tail(3).copy()
    df_last3.reset_index(drop=True, inplace=True)
    df_last3['record_num'] = df_last3.index + 1
    df_chart = df_last3.set_index('record_num')[['anxiety', 'depression']]
    st.line_chart(df_chart)   # normal size
else:
    st.info("✨ Save your mood multiple times to see your last 3 records trend here.")

st.divider()

# ---------- Emotion Diary (Chat interface) ----------
st.header("💬 Your Emotion Diary")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input (no button here; analysis button is in sidebar)
user_input = st.chat_input("Write down what's on your mind...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                system_prompt = "You are a warm, empathetic companion. Listen and support the user, but do not over-analyze unless asked."
                messages_for_api = [
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages[-10:]
                ]
                chat_completion = client.chat.completions.create(
                    messages=messages_for_api,
                    model="llama-3.3-70b-versatile",
                )
                ai_reply = chat_completion.choices[0].message.content
                st.markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    except Exception as e:
        error_msg = f"Sorry, I'm having trouble responding. Error: {e}"
        with st.chat_message("assistant"):
            st.markdown(error_msg)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})

st.divider()
st.caption("Remember: You are not alone. This diary is a private space for your emotions and insights.")