
import streamlit as st
import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = st.secrets.get("HUGGINGFACE_API_TOKEN") or os.getenv("HF_TOKEN")

# Initialize session state
if "explanation" not in st.session_state:
    st.session_state.explanation = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "styles" not in st.session_state:
    st.session_state.styles = []
if "analogy" not in st.session_state:
    st.session_state.analogy = ""

def reset_session():
    st.session_state.explanation = None
    st.session_state.topic = ""
    st.session_state.styles = []
    st.session_state.analogy = ""

# GPT-OSS query function
def query_gpt_oss(prompt):
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {
        "model": "openai/gpt-oss-20b:together",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}\nFull response: {response.text}"

# Unified explanation generator
def generate_blended_explanation(styles, topic, custom_analogy=None, simplify=False, format_choice="Narrative", tone="Conversational"):
    style_list = ', '.join(styles)
    style_guidance = get_style_guidance(styles)

    if simplify:
        if format_choice == "Bullet Points":
            prompt = f"""
You are ArthaVittya, a financial learning assistant. Explain the concept "{topic}" in a short, beginner-friendly way using bullet points.

Instructions:
- Limit to 5 bullet points max
- Each point should be 1–2 short sentences
- Use simple language and everyday examples
- Avoid technical terms or economic jargon
- Focus on what it is, why it matters, and one relatable example
- Adapt the bullet points to match these learning styles: {style_guidance}

If the user provided a custom analogy, include it: "{custom_analogy}"
Speak in a {tone.lower()} tone.
"""
        else:  # Narrative format
            prompt = f"""
You are ArthaVittya, a financial learning assistant. Explain the concept "{topic}" in a short, beginner-friendly way using 1–2 short paragraphs.

Instructions:
- Keep total length under 150 words
- Use simple words and clear examples
- Avoid technical terms or deep analysis
- Speak like you're explaining it to a curious teenager
- Adapt the explanation to match these learning styles: {style_guidance}

If the user provided a custom analogy, include it: "{custom_analogy}"
Speak in a {tone.lower()} tone.
"""
    else:
            prompt = f"""
You are a financial learning assistant. Your goal is to explain the finance "{topic}" in a way that blends the user's selected learning styles: {style_list}.
Focus on clarity, relevance, and real-world financial applications. Use metaphors, structure, and sensory techniques that suit the selected styles.
Do not just list facts. Instead, create a flowing, immersive explanation that feels like a teacher guiding a curious learner. Use storytelling, relatable metaphors, and sensory language where appropriate.
Create a unified explanation that is easy to read and visually structured. Do not separate by style or label sections like “Visual Learner Tip.” Instead, break the explanation into required size, titled blocks that reflect the blended learning approach.
Speak like a thoughtful teacher explaining this to a curious learner. Be patient, expressive, and detailed. Avoid summarizing instead expand with care.
Blend techniques naturally. Don’t label them. Instead, let the explanation feel like a multisensory experience where visuals, logic, rhythm, and movement flow together.
Ensure numbers and formatting are clean and readable. Avoid merging words or symbols.
Each section should be at least 3–5 paragraphs long even more if needed. Expand with examples, analogies, and layered reasoning. Do not summarize instead elaborate.
Ensure all numbers, punctuation, and formatting are clean and readable. Avoid merging words or symbols. Use proper spacing and line breaks.

Use, titled sections only if helpful for the particular topic or concept, such as:
**1. What It Is**  
Begin with a clear, engaging introduction. Assume the learner is hearing this concept for the first time. Use relatable language and analogies to spark curiosity.

**2. How It Works**  
Dive deep into the mechanics. Use sensory metaphors (for visual/kinesthetic learners), rhythmic phrasing (for auditory learners), and logical flow (for analytical learners). Break down the concept step-by-step, and explain why each part matters.

**3. Real-World Example**  
Paint a vivid scenario that shows the concept in action. Use a story, situation, or simulation that the learner can visualize or relate to. Make it feel tangible.

**4. Real-World Case study or a cool fact

**5. Takeaway**  
End with a memorable insight or summary that reinforces understanding. Use repetition, metaphor, or a punchy phrase that sticks.

Blend techniques from all selected styles naturally. Use imagery, rhythm, tactile cues, structure, and reasoning — but keep each block concise and engaging.

If the user provided a custom analogy, weave it throughout: "{custom_analogy}".

Speak in a {tone.lower()} tone that suits the learner’s preference.

Avoid long paragraphs whenever required. Use short sections with bolded titles to guide the reader.
Avoid generic phrasing. Speak like a mentor who adapts to the learner’s needs. Make the explanation feel alive, layered, and easy to absorb.

"""
    return query_gpt_oss(prompt)


# Style tips generator
def generate_style_tips(styles, topic, analogy=None, simplify =False, format_choice="Narrative", tone="Conversational"):
    style_list = ', '.join(styles)
     
    
    if simplify:
        
       prompt = f"""
You are a personalized learning assistant. A user is about to learn about "{topic}" and has selected the following learning styles: {style_list}.

Your task is to generate , engaging tips that help the user absorb the finance or economics concepts explanation more effectively based on those styles.

Use a warm, encouraging tone. Speak directly to the learner. Make each tip feel like a personal suggestion from a mentor who understands their style.

Use clear, encouraging language. Include sensory cues, metaphors, or strategies that align with each style. If the user provided an analogy, incorporate it creatively: "{analogy}".
"""
    return query_gpt_oss(prompt)


# Style guidance
def get_style_guidance(styles):
    phrases = []

    if "Visual" in styles:
        phrases.append("vivid metaphors, spatial descriptions, and visual imagery")
    if "Auditory" in styles:
        phrases.append("rhythmic phrasing, repetition, and spoken-style narration")
    if "Kinesthetic" in styles:
        phrases.append("movement-based metaphors, tactile simulations, and action-oriented examples")
    if "Logical" in styles:
        phrases.append("step-by-step reasoning, cause-effect logic, and analytical flow")
    if "Reading/Writing" in styles:
        phrases.append("structured paragraphs, bullet points, and written summaries")

    if not phrases:
        return "Use a clear and engaging explanation style."

    # Combine phrases into a single sentence
    if len(phrases) == 1:
        return f"Use {phrases[0]} to match the learner’s style."
    else:
        last = phrases.pop()
        combined = ", ".join(phrases)
        return f"Blend {combined}, and {last} to match the learner’s selected styles."





# UI layout
st.title("ArthaVittya — Learn Finance & Economics Your Way")
st.markdown("**ArthaVittya** helps you master finance and economics through personalized explanations tailored to your learning style.")


with st.sidebar:
    st.header("Customize Your Learning")
    styles = st.multiselect("Choose your Financial learning styles:", 
        ["Visual", "Auditory", "Kinesthetic", "Reading/Writing", "Logical"])
    topic = st.text_input("Enter a finance or economics concept (e.g., inflation, compound interest)")
    custom_analogy = st.text_input("Add a custom analogy (optional):")
    
    generate = st.button("Generate Explanation")
    show_tips = st.button("Show Learning Tips")
    simplify = st.checkbox("Simplify This (Beginner-Friendly)")
    format_choice = st.radio(
    "Choose explanation format for simplify:",
    ["Narrative", "Bullet Points"]
)

    tone = st.selectbox("Choose explanation tone:", ["Conversational", "Academic"])


    if st.button("🔄 Reset"):
        reset_session()
        st.rerun()

# Generate explanation
if generate:
    if not topic:
        st.warning("Please enter a finance or economics topic to learn about.")
    else:
        explanation = generate_blended_explanation(styles, topic, custom_analogy, simplify, format_choice, tone)
        st.session_state.explanation = explanation
        st.session_state.topic = topic
        st.session_state.styles = styles
        st.session_state.analogy = custom_analogy

        if simplify and len(explanation.split()) > 180:
            st.warning("This explanation may be too long for simplified mode. Try rephrasing or switching to bullet points.") 

        st.subheader("📘 Personalized Explanation")
        st.write(explanation)

# Show learning tips independently
if show_tips:
    if not topic or not styles:
        st.warning("Please enter a topic and select at least one learning style to generate tips.")
    else:
        style_tips = generate_style_tips(styles, topic, custom_analogy)
        st.subheader("🧠 Learning Tips Based on Your Style")
        st.write(style_tips)

