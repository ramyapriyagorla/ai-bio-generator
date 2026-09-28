"""
AI Bio Generator - Streamlit Web Application
Powered by Python, Streamlit, NLP, and Generative AI (Google Gemini).
"""

import os
import streamlit as st
from dotenv import load_dotenv

from bio_generator import BioGenerator, BIO_TYPES, TONES
from utils import calculate_metrics, format_txt_download, SAMPLE_PROFILES

# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="AI Bio Generator | Professional Profile Creator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern, polished, attractive UI
st.markdown(
    """
    <style>
    /* Main container and font styles */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        max-width: 1280px;
    }
    
    /* Header gradient hero */
    .hero-card {
        background: linear-gradient(135deg, #1E1E2F 0%, #2D2B55 50%, #4B3869 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(90deg, #FFFFFF, #A5B4FC, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #D1D5DB;
        margin-top: 6px;
        margin-bottom: 0px;
    }
    
    /* Card wrapper */
    .content-box {
        background-color: var(--background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Result card */
    .bio-result-card {
        background: rgba(99, 102, 241, 0.04);
        border: 1.5px solid rgba(99, 102, 241, 0.25);
        border-radius: 14px;
        padding: 24px;
        font-size: 1.05rem;
        line-height: 1.7;
        margin-top: 12px;
        margin-bottom: 16px;
        color: inherit;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-type {
        background-color: rgba(99, 102, 241, 0.15);
        color: #6366F1;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    .badge-tone {
        background-color: rgba(168, 85, 247, 0.15);
        color: #A855F7;
        border: 1px solid rgba(168, 85, 247, 0.3);
    }
    .badge-ai {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    /* Streamlit button enhancements */
    div.stButton > button:first-child {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_session_state():
    """Initializes Streamlit session states for inputs and generated results."""
    defaults = {
        "name": "",
        "role": "",
        "education": "",
        "skills": "",
        "experience": "",
        "projects": "",
        "certifications": "",
        "achievements": "",
        "interests": "",
        "bio_type": "Professional",
        "tone": "Professional",
        "pov": "First Person (I / me)",
        "include_emojis": False,
        "generated_bio": "",
        "is_fallback": False,
        "status_message": None,
        "generation_count": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


def load_preset(preset_name: str):
    """Loads a pre-defined sample profile into session state."""
    if preset_name in SAMPLE_PROFILES:
        data = SAMPLE_PROFILES[preset_name]
        for key in [
            "name",
            "role",
            "education",
            "skills",
            "experience",
            "projects",
            "certifications",
            "achievements",
            "interests",
            "bio_type",
            "tone",
        ]:
            if key in data:
                st.session_state[key] = data[key]
        st.session_state.generated_bio = ""
        st.session_state.status_message = None


def clear_inputs():
    """Resets all input fields and the generated bio."""
    for key in [
        "name",
        "role",
        "education",
        "skills",
        "experience",
        "projects",
        "certifications",
        "achievements",
        "interests",
    ]:
        st.session_state[key] = ""
    st.session_state.generated_bio = ""
    st.session_state.status_message = None


# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("### ⚙️ Settings & Configuration")

    # API Key Configuration
    env_api_key = os.getenv("GEMINI_API_KEY", "").strip()
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=env_api_key,
        type="password",
        help="Reads from .env by default. Enter a key to override or test.",
        placeholder="AIzaSy...",
    )
    active_api_key = api_key_input.strip() or env_api_key

    if active_api_key:
        st.success("🟢 API Key Active (Gemini Generative AI)", icon="✅")
    else:
        st.info("ℹ️ No API key detected. Running in **NLP Fallback Mode**. Enter a key or add to `.env` to unlock Gemini.")

    st.markdown("---")

    # Sample Preset Loader
    st.markdown("### ⚡ Quick-Fill Presets")
    st.caption("Try sample profiles with 1-click:")
    cols_preset = st.columns(len(SAMPLE_PROFILES))
    for idx, preset_name in enumerate(SAMPLE_PROFILES.keys()):
        if st.button(preset_name, key=f"btn_preset_{idx}", use_container_width=True):
            load_preset(preset_name)
            st.rerun()

    st.markdown("---")

    # App Info & Guidelines
    st.markdown("### 🛡️ Grounding Guarantee")
    st.markdown(
        """
        - **Zero Hallucinations**: Strict prompt guardrails ensure the AI uses **only** your provided facts.
        - **Grammatically Correct**: Natural, professional prose tuned to your selected tone.
        - **Privacy First**: Keys are kept strictly local in `.env` and never saved or transmitted externally.
        """
    )
    st.markdown("---")
    st.caption("Built with Python, Streamlit, and Google Gemini.")


# --- MAIN HEADER HERO ---
st.markdown(
    """
    <div class="hero-card">
        <h1 class="hero-title">✨ AI Bio Generator</h1>
        <p class="hero-subtitle">
            Craft tailored, natural, and grammatically flawless bios using Generative AI and NLP — grounded strictly in your real facts.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --- MAIN LAYOUT (2 Columns) ---
col_form, col_output = st.columns([1.05, 1.1], gap="large")

# ==========================================
# LEFT COLUMN: INPUT FORM
# ==========================================
with col_form:
    st.markdown("### 📝 Profile Information")
    st.caption("Fill in your background details. Only provided information will be used.")

    # Name and Role
    c1, c2 = st.columns(2)
    with c1:
        name_val = st.text_input(
            "Full Name *",
            value=st.session_state.name,
            placeholder="e.g. Alex Rivera",
            key="name_input",
            help="Your full professional name.",
        )
        st.session_state.name = name_val
    with c2:
        role_val = st.text_input(
            "Target / Current Role *",
            value=st.session_state.role,
            placeholder="e.g. Senior Full-Stack Engineer",
            key="role_input",
            help="Your profession, target job title, or specialization.",
        )
        st.session_state.role = role_val

    # Education
    edu_val = st.text_area(
        "Education & Academic Background",
        value=st.session_state.education,
        placeholder="e.g. B.S. in Computer Science from University of Washington, 2023",
        height=70,
        key="edu_input",
    )
    st.session_state.education = edu_val

    # Skills
    skills_val = st.text_area(
        "Skills & Proficiencies",
        value=st.session_state.skills,
        placeholder="e.g. Python, React, AWS, Docker, FastAPI, PostgreSQL, Machine Learning",
        height=70,
        key="skills_input",
        help="List key technical, creative, or soft skills (comma-separated).",
    )
    st.session_state.skills = skills_val

    # Experience
    exp_val = st.text_area(
        "Experience Highlights",
        value=st.session_state.experience,
        placeholder="e.g. 5+ years building scalable SaaS web platforms and cloud microservices.",
        height=80,
        key="exp_input",
    )
    st.session_state.experience = exp_val

    # Projects
    proj_val = st.text_area(
        "Key Projects",
        value=st.session_state.projects,
        placeholder="e.g. Built an open-source real-time event streaming pipeline processing 100k events/sec.",
        height=75,
        key="proj_input",
    )
    st.session_state.projects = proj_val

    # Certifications & Achievements in 2 columns
    c3, c4 = st.columns(2)
    with c3:
        cert_val = st.text_area(
            "Certifications & Credentials",
            value=st.session_state.certifications,
            placeholder="e.g. AWS Certified Solutions Architect",
            height=70,
            key="cert_input",
        )
        st.session_state.certifications = cert_val
    with c4:
        achieve_val = st.text_area(
            "Key Achievements & Awards",
            value=st.session_state.achievements,
            placeholder="e.g. Reduced API latency by 45%; 1st place in 2025 Hackathon",
            height=70,
            key="achieve_input",
        )
        st.session_state.achievements = achieve_val

    # Interests
    interest_val = st.text_input(
        "Personal Interests / Hobbies",
        value=st.session_state.interests,
        placeholder="e.g. Marathon running, chess, open-source AI, violin",
        key="interest_input",
        help="Adds a relatable, human touch to friendly and detailed bios.",
    )
    st.session_state.interests = interest_val

    st.markdown("### 🎨 Bio Customization")
    c5, c6 = st.columns(2)
    with c5:
        bio_type_options = list(BIO_TYPES.keys())
        current_type_idx = (
            bio_type_options.index(st.session_state.bio_type)
            if st.session_state.bio_type in bio_type_options
            else 0
        )
        bio_type_val = st.selectbox(
            "Bio Type",
            options=bio_type_options,
            index=current_type_idx,
            help="Select the format and length of the bio.",
            key="bio_type_select",
        )
        st.session_state.bio_type = bio_type_val

    with c6:
        tone_options = list(TONES.keys())
        current_tone_idx = (
            tone_options.index(st.session_state.tone)
            if st.session_state.tone in tone_options
            else 0
        )
        tone_val = st.selectbox(
            "Tone",
            options=tone_options,
            index=current_tone_idx,
            help="Select the voice and emotional impression.",
            key="tone_select",
        )
        st.session_state.tone = tone_val

    # Advanced styling options (Point of view & Emojis)
    with st.expander("🛠️ Advanced Options (Perspective & Emojis)", expanded=False):
        c7, c8 = st.columns(2)
        with c7:
            pov_val = st.radio(
                "Perspective",
                options=["First Person (I / me)", "Third Person (He / She / They)"],
                index=0 if "First" in st.session_state.pov else 1,
                horizontal=True,
            )
            st.session_state.pov = pov_val
        with c8:
            emoji_val = st.checkbox(
                "Include professional emojis",
                value=st.session_state.include_emojis,
                help="Adds subtle, high-relevance emojis.",
            )
            st.session_state.include_emojis = emoji_val

    # Action Buttons Row: Generate, Clear
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns([2, 1])

    with btn_col1:
        generate_clicked = st.button(
            "🚀 Generate Bio",
            type="primary",
            use_container_width=True,
        )

    with btn_col2:
        clear_clicked = st.button(
            "🗑️ Clear Inputs",
            use_container_width=True,
        )
        if clear_clicked:
            clear_inputs()
            st.rerun()


# ==========================================
# GENERATION LOGIC HANDLER
# ==========================================
generator = BioGenerator(api_key=active_api_key)

profile_data = {
    "name": st.session_state.name,
    "role": st.session_state.role,
    "education": st.session_state.education,
    "skills": st.session_state.skills,
    "experience": st.session_state.experience,
    "projects": st.session_state.projects,
    "certifications": st.session_state.certifications,
    "achievements": st.session_state.achievements,
    "interests": st.session_state.interests,
}


def perform_generation(temp: float = 0.7):
    """Executes the bio generation with loading spinner and error handling."""
    if not profile_data["name"] and not profile_data["role"]:
        st.error("⚠️ Please provide at least your **Name** or **Current Role** to generate a bio.")
        return

    with st.spinner("🤖 Synthesizing your personalized bio using AI..."):
        try:
            bio_text, is_fallback, status_msg = generator.generate_bio(
                profile_data=profile_data,
                bio_type=st.session_state.bio_type,
                tone=st.session_state.tone,
                pov=st.session_state.pov,
                include_emojis=st.session_state.include_emojis,
                temperature=temp,
            )
            st.session_state.generated_bio = bio_text
            st.session_state.is_fallback = is_fallback
            st.session_state.status_message = status_msg
            st.session_state.generation_count += 1
        except Exception as exc:
            st.error(f"❌ An unexpected error occurred: {exc}")


if generate_clicked:
    perform_generation(temp=0.7)
    st.rerun()


# ==========================================
# RIGHT COLUMN: GENERATED BIO & ACTIONS
# ==========================================
with col_output:
    st.markdown("### 📄 Generated Bio")
    st.caption("Real-time preview with NLP text analysis and export tools.")

    if st.session_state.generated_bio:
        # Display badges for active configuration
        st.markdown(
            f"""
            <div>
                <span class="badge badge-type">Type: {st.session_state.bio_type}</span>
                <span class="badge badge-tone">Tone: {st.session_state.tone}</span>
                <span class="badge badge-ai">{'Local NLP' if st.session_state.is_fallback else 'Gemini AI'}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.status_message:
            st.info(st.session_state.status_message, icon="💡")

        # Bio Display Box
        st.markdown(
            f"""
            <div class="bio-result-card">
                {st.session_state.generated_bio.replace(chr(10), '<br>')}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # NLP Metrics Display
        metrics = calculate_metrics(st.session_state.generated_bio)
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("Words", metrics["word_count"])
        with m_col2:
            st.metric("Characters", metrics["char_count"])
        with m_col3:
            st.metric("Sentences", metrics["sentence_count"])
        with m_col4:
            st.metric("Reading Time", f"~{metrics['reading_time_sec']}s")

        st.markdown("---")

        # Action Buttons: Regenerate, Copy, Download
        act_col1, act_col2 = st.columns(2)

        with act_col1:
            if st.button("🔄 Regenerate Bio", use_container_width=True):
                # Use slightly higher temperature for creative variation
                perform_generation(temp=0.88)
                st.rerun()

        with act_col2:
            export_content = format_txt_download(
                profile_data=profile_data,
                bio=st.session_state.generated_bio,
                bio_type=st.session_state.bio_type,
                tone=st.session_state.tone,
            )
            safe_name = (
                st.session_state.name.lower().replace(" ", "_")
                if st.session_state.name
                else "profile"
            )
            file_name = f"bio_{safe_name}_{st.session_state.bio_type.lower()}.txt"

            st.download_button(
                label="📥 Download as TXT",
                data=export_content,
                file_name=file_name,
                mime="text/plain",
                use_container_width=True,
            )

        # Easy Copy Section
        with st.expander("📋 Copy to Clipboard", expanded=True):
            st.caption("Click the copy icon on the top-right of the code snippet below:")
            st.code(st.session_state.generated_bio, language="markdown")

    else:
        # Placeholder empty state
        st.markdown(
            """
            <div style="border: 2px dashed rgba(128, 128, 128, 0.3); border-radius: 14px; padding: 48px 24px; text-align: center; margin-top: 16px;">
                <div style="font-size: 3rem; margin-bottom: 12px;">✍️</div>
                <h4 style="margin: 0; color: #9CA3AF;">Your bio will appear here</h4>
                <p style="color: #6B7280; font-size: 0.95rem; margin-top: 8px;">
                    Fill in your details on the left, or pick one of the <b>Quick-Fill Presets</b> in the sidebar, then click <b>Generate Bio</b>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
