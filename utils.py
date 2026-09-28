"""
Utility functions for text processing, NLP metrics calculation,
export formatting, and sample presets for the AI Bio Generator.
"""

from datetime import datetime
from typing import Dict, Any, Tuple


def calculate_metrics(text: str) -> Dict[str, Any]:
    """
    Computes NLP and readability metrics for the generated bio.
    
    Returns:
        dict: word_count, char_count_with_spaces, char_count_no_spaces,
              estimated_reading_time_sec, sentence_count
    """
    if not text or not text.strip():
        return {
            "word_count": 0,
            "char_count": 0,
            "char_count_no_spaces": 0,
            "reading_time_sec": 0,
            "sentence_count": 0,
        }

    stripped = text.strip()
    words = stripped.split()
    word_count = len(words)
    char_count = len(stripped)
    char_count_no_spaces = len(stripped.replace(" ", "").replace("\n", ""))

    # Count sentences (period, exclamation, question mark)
    import re
    sentences = [s for s in re.split(r'[.!?]+', stripped) if s.strip()]
    sentence_count = len(sentences)

    # Average silent reading speed: ~200-250 words per minute (approx 3.5 words/sec)
    reading_time_sec = max(1, round(word_count / 3.5)) if word_count > 0 else 0

    return {
        "word_count": word_count,
        "char_count": char_count,
        "char_count_no_spaces": char_count_no_spaces,
        "reading_time_sec": reading_time_sec,
        "sentence_count": sentence_count,
    }


def format_txt_download(profile_data: Dict[str, str], bio: str, bio_type: str, tone: str) -> str:
    """
    Creates a clean, structured plain text file export for the user's bio.
    """
    metrics = calculate_metrics(bio)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    divider = "=" * 60
    subdivider = "-" * 60

    lines = [
        divider,
        "AI BIO GENERATOR - EXPORTED PROFILE BIO",
        divider,
        f"Generated At : {now_str}",
        f"Full Name    : {profile_data.get('name', 'N/A')}",
        f"Target Role  : {profile_data.get('role', 'N/A')}",
        f"Bio Type     : {bio_type}",
        f"Tone         : {tone}",
        f"Word Count   : {metrics['word_count']} words",
        f"Char Count   : {metrics['char_count']} characters",
        divider,
        "",
        "GENERATED BIO:",
        subdivider,
        bio.strip(),
        subdivider,
        "",
        "SOURCE INFORMATION PROVIDED:",
        f"Education     : {profile_data.get('education', 'N/A') or 'N/A'}",
        f"Skills        : {profile_data.get('skills', 'N/A') or 'N/A'}",
        f"Experience    : {profile_data.get('experience', 'N/A') or 'N/A'}",
        f"Projects      : {profile_data.get('projects', 'N/A') or 'N/A'}",
        f"Certifications: {profile_data.get('certifications', 'N/A') or 'N/A'}",
        f"Achievements  : {profile_data.get('achievements', 'N/A') or 'N/A'}",
        f"Interests     : {profile_data.get('interests', 'N/A') or 'N/A'}",
        "",
        divider,
        "Generated with AI Bio Generator (Powered by Gemini & Streamlit)",
        divider,
    ]

    return "\n".join(lines)


# Presets for fast testing and previewing
SAMPLE_PROFILES = {
    "Software Engineer": {
        "name": "Alex Rivera",
        "role": "Senior Full-Stack Engineer",
        "education": "B.S. in Computer Science from University of Washington",
        "skills": "Python, TypeScript, React, Node.js, FastAPI, PostgreSQL, Docker, AWS, GraphQL",
        "experience": "5+ years developing scalable SaaS web applications, microservices, and distributed cloud systems.",
        "projects": "Architected an open-source real-time event streaming pipeline processing 100k events/sec. Built a developer productivity dashboard used by 2,000+ engineers.",
        "certifications": "AWS Certified Solutions Architect – Associate",
        "achievements": "Reduced API p99 latency by 45% across core customer workflows; Speaker at PyCon 2024 regional meetup.",
        "interests": "Open-source development, mechanical keyboards, marathon running, hiking in the Pacific Northwest",
        "bio_type": "LinkedIn",
        "tone": "Confident",
    },
    "Computer Science Student": {
        "name": "Priya Sharma",
        "role": "Aspiring AI/ML Engineer & CS Undergraduate",
        "education": "B.Tech in Artificial Intelligence & Data Science, Expected Graduation 2026",
        "skills": "Python, PyTorch, Scikit-Learn, Pandas, NumPy, OpenCV, Git, SQL, Streamlit",
        "experience": "Undergraduate Research Assistant at University AI Lab; Summer Machine Learning Intern at TechNova Labs.",
        "projects": "Developed a computer vision system for real-time sign language recognition with 94% accuracy. Created an automated study notes summarizer using NLP.",
        "certifications": "DeepLearning.AI Deep Learning Specialization",
        "achievements": "1st place in University Hackathon 2025 (400+ participants); Published research paper on lightweight CNNs at student symposium.",
        "interests": "Generative AI research, competitive programming, playing classical violin, tech mentoring",
        "bio_type": "Student",
        "tone": "Friendly",
    },
    "Product Manager": {
        "name": "Marcus Chen",
        "role": "Lead Product Manager",
        "education": "MBA from UC Berkeley Haas School of Business; B.A. in Economics",
        "skills": "Product Strategy, Roadmap Planning, User Research, Agile/Scrum, Data Analytics, A/B Testing, Cross-Functional Leadership",
        "experience": "7 years leading cross-functional teams spanning engineering, UX design, and marketing to launch B2B enterprise software.",
        "projects": "Spearheaded the 0-to-1 launch of an enterprise collaboration workspace driving $12M ARR in Year 1.",
        "certifications": "Certified Scrum Product Owner (CSPO), Pragmatic Institute Certified (PMC-III)",
        "achievements": "Increased user retention by 28% through data-driven product onboarding revamp; Mentored 10+ junior APMs.",
        "interests": "Fintech trends, chess, specialty coffee brewing, urban cycling",
        "bio_type": "Professional",
        "tone": "Professional",
    },
}
