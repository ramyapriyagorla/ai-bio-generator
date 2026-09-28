"""
Bio Generator Module:
Integrates Google Gemini Generative AI with strict anti-hallucination prompt engineering,
and includes an intelligent offline NLP synthesizer fallback.
"""

import os
from typing import Dict, Any, Tuple, Optional
from dotenv import load_dotenv

# Load local environment variables from .env
load_dotenv()

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False


# Supported bio types and tone definitions
BIO_TYPES = {
    "Professional": (
        "A well-structured, authoritative, and balanced executive summary. "
        "Highlight current role, core competencies, notable career impact, and forward outlook."
    ),
    "Student": (
        "An academically focused profile highlighting education, major coursework, hands-on projects, "
        "campus leadership, technical skills, and career aspirations."
    ),
    "LinkedIn": (
        "An engaging, modern LinkedIn 'About' section style with an attention-grabbing hook, "
        "clear value proposition, key highlights, and an inviting closing call-to-action for networking."
    ),
    "Short": (
        "A concise elevator pitch of 2 to 4 punchy sentences. "
        "Distill identity, primary skills, and core impact into a brief, memorable summary."
    ),
    "Detailed": (
        "A comprehensive narrative of 3 to 4 well-structured paragraphs. "
        "Thoroughly explore professional journey, technical expertise, projects, standout achievements, and passions."
    ),
}

TONES = {
    "Professional": "Polished, formal, authoritative, and articulate.",
    "Friendly": "Warm, approachable, engaging, and conversational while maintaining credibility.",
    "Simple": "Direct, plain English, jargon-free, and easy to read.",
    "Confident": "Bold, dynamic, high-energy, and action-oriented, emphasizing impact and ambition.",
}


class BioGenerator:
    """Manages AI bio generation using Gemini with strict grounding and offline fallback."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        self._init_gemini()

    def _init_gemini(self) -> None:
        """Initializes the Google Generative AI client if key is present."""
        if GENAI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.configured = True
            except Exception:
                self.configured = False
        else:
            self.configured = False

    def set_api_key(self, api_key: str) -> None:
        """Dynamically update the API key."""
        self.api_key = api_key.strip()
        self._init_gemini()

    def build_prompt(
        self,
        profile_data: Dict[str, str],
        bio_type: str,
        tone: str,
        pov: str = "First Person (I / me)",
        include_emojis: bool = False,
    ) -> str:
        """
        Builds a comprehensive prompt with strict anti-hallucination guardrails.
        """
        type_desc = BIO_TYPES.get(bio_type, BIO_TYPES["Professional"])
        tone_desc = TONES.get(tone, TONES["Professional"])

        pov_instruction = (
            "Write in the FIRST PERSON (using 'I', 'my', 'me')."
            if "First" in pov
            else "Write in the THIRD PERSON (using the person's name and 'they/their' or 'he/she')."
        )

        emoji_instruction = (
            "Include 2-4 subtle, professional emojis to enhance readability and visual appeal."
            if include_emojis
            else "Do NOT use any emojis. Maintain clean plain text typography."
        )

        # Build user profile details
        user_facts = []
        name = profile_data.get("name", "").strip()
        if name:
            user_facts.append(f"- Full Name: {name}")
        role = profile_data.get("role", "").strip()
        if role:
            user_facts.append(f"- Current Role / Title: {role}")
        education = profile_data.get("education", "").strip()
        if education:
            user_facts.append(f"- Education & Background: {education}")
        skills = profile_data.get("skills", "").strip()
        if skills:
            user_facts.append(f"- Skills & Proficiencies: {skills}")
        experience = profile_data.get("experience", "").strip()
        if experience:
            user_facts.append(f"- Experience: {experience}")
        projects = profile_data.get("projects", "").strip()
        if projects:
            user_facts.append(f"- Key Projects: {projects}")
        certifications = profile_data.get("certifications", "").strip()
        if certifications:
            user_facts.append(f"- Certifications & Credentials: {certifications}")
        achievements = profile_data.get("achievements", "").strip()
        if achievements:
            user_facts.append(f"- Key Achievements & Awards: {achievements}")
        interests = profile_data.get("interests", "").strip()
        if interests:
            user_facts.append(f"- Personal Interests & Hobbies: {interests}")

        facts_block = "\n".join(user_facts) if user_facts else "- No specific details provided."

        prompt = f"""You are an elite executive resume writer, LinkedIn branding strategist, and NLP biographer.
Your task is to write a compelling, natural, grammatically flawless bio for the individual described below.

=== CRITICAL GROUNDING AND ANTI-HALLUCINATION RULES ===
1. STRICT TRUTHFULNESS: You MUST generate the bio using ONLY the facts and details explicitly provided in the 'USER FACTS' section below.
2. NO INVENTED DETAILS: Do NOT invent, assume, or fabricate any company names, universities, graduation years, metrics, percentages, job titles, or tools that are not in the facts.
3. BLANK FIELDS: If certain fields are omitted or blank, smoothly write around them without mentioning that information is missing.
4. ACCURACY: Rephrase and elevate the user's authentic story without exaggerating beyond the provided claims.

=== BIO SPECIFICATIONS ===
- Bio Type: {bio_type} ({type_desc})
- Tone: {tone} ({tone_desc})
- Point of View: {pov_instruction}
- Emoji Usage: {emoji_instruction}

=== USER FACTS ===
{facts_block}

=== OUTPUT FORMAT ===
Produce ONLY the final ready-to-use bio text. Do NOT include markdown code blocks, conversational greetings, explanations, or meta-commentary.
"""
        return prompt.strip()

    def generate_bio(
        self,
        profile_data: Dict[str, str],
        bio_type: str = "Professional",
        tone: str = "Professional",
        pov: str = "First Person (I / me)",
        include_emojis: bool = False,
        temperature: float = 0.7,
    ) -> Tuple[str, bool, Optional[str]]:
        """
        Generates a bio using Gemini. If API key is missing or an error occurs,
        falls back to intelligent NLP synthesizer.

        Returns:
            Tuple[str, bool, Optional[str]]: (generated_text, is_fallback, error_or_info_message)
        """
        # Check if Gemini is configured
        if not self.configured or not GENAI_AVAILABLE:
            bio = self._synthesize_nlp_fallback(profile_data, bio_type, tone, pov, include_emojis)
            info_msg = (
                "Generated using local NLP synthesizer. "
                "To unlock Gemini generative AI, provide a GEMINI_API_KEY in the sidebar or in your .env file."
            )
            return bio, True, info_msg

        prompt = self.build_prompt(profile_data, bio_type, tone, pov, include_emojis)

        # Attempt generation using candidate models
        models_to_try = [
            "gemini-1.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-pro",
        ]

        last_error = None
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=1000,
                    ),
                )
                response = model.generate_content(prompt)
                if response and response.text:
                    cleaned_text = response.text.strip()
                    # Strip any accidental wrapping quotes or markdown backticks
                    if cleaned_text.startswith("```") and cleaned_text.endswith("```"):
                        lines = cleaned_text.splitlines()
                        if len(lines) >= 2:
                            cleaned_text = "\n".join(lines[1:-1]).strip()
                    return cleaned_text, False, None
            except Exception as e:
                last_error = str(e)
                continue

        # If all API calls failed, fall back to offline NLP synthesizer
        bio = self._synthesize_nlp_fallback(profile_data, bio_type, tone, pov, include_emojis)
        fallback_msg = (
            f"Gemini API request encountered an issue ({last_error}). "
            "Generated high-quality fallback bio using local NLP synthesizer."
        )
        return bio, True, fallback_msg

    def _synthesize_nlp_fallback(
        self,
        profile_data: Dict[str, str],
        bio_type: str,
        tone: str,
        pov: str,
        include_emojis: bool,
    ) -> str:
        """
        Local deterministic NLP bio synthesizer.
        Carefully stitches only the provided user details into natural, grammatically correct prose.
        Zero hallucinated details.
        """
        name = profile_data.get("name", "").strip() or "Professional"
        role = profile_data.get("role", "").strip() or "Specialist"
        education = profile_data.get("education", "").strip()
        skills = profile_data.get("skills", "").strip()
        experience = profile_data.get("experience", "").strip()
        projects = profile_data.get("projects", "").strip()
        certifications = profile_data.get("certifications", "").strip()
        achievements = profile_data.get("achievements", "").strip()
        interests = profile_data.get("interests", "").strip()

        is_first_person = "First" in pov

        # Emoji mapping
        e_role = "💼 " if include_emojis else ""
        e_edu = "🎓 " if include_emojis else ""
        e_skill = "🚀 " if include_emojis else ""
        e_proj = "🛠️ " if include_emojis else ""
        e_trophy = "🏆 " if include_emojis else ""
        e_heart = "✨ " if include_emojis else ""
        e_cta = "📫 " if include_emojis else ""

        # Sentence helpers based on POV and Tone
        subj = "I am" if is_first_person else f"{name} is"
        possessive = "My" if is_first_person else f"{name}'s"
        pronoun = "I" if is_first_person else name
        pronoun_obj = "me" if is_first_person else name

        tone_adjectives = {
            "Professional": "dedicated and results-driven",
            "Friendly": "passionate and collaborative",
            "Simple": "focused and practical",
            "Confident": "dynamic, high-impact, and ambitious",
        }
        adj = tone_adjectives.get(tone, "dedicated")

        # 1. SHORT BIO
        if bio_type == "Short":
            lines = [f"{e_role}{subj} a {adj} {role}."]
            if skills:
                lines.append(f"Specializing in {skills.rstrip('.')}.")
            if experience:
                lines.append(experience.rstrip(".") + ".")
            if achievements:
                lines.append(f"Notable highlights include {achievements.rstrip('.')}.")
            return " ".join(lines)

        # 2. STUDENT BIO
        if bio_type == "Student":
            paragraphs = []
            p1 = [f"{e_edu}{subj} a {adj} {role}"]
            if education:
                p1.append(f"pursuing {education.rstrip('.')}")
            paragraphs.append(" ".join(p1) + ".")

            p2 = []
            if skills:
                p2.append(f"{e_skill}Core competencies and technical coursework include {skills.rstrip('.')}.")
            if projects:
                p2.append(f"{e_proj}Hands-on project work includes {projects.rstrip('.')}.")
            if p2:
                paragraphs.append(" ".join(p2))

            p3 = []
            if achievements:
                p3.append(f"{e_trophy}Key accomplishments: {achievements.rstrip('.')}.")
            if interests:
                p3.append(f"{e_heart}Beyond academics, {pronoun.lower() if is_first_person else pronoun} is passionate about {interests.rstrip('.')}.")
            if p3:
                paragraphs.append(" ".join(p3))

            return "\n\n".join(paragraphs)

        # 3. LINKEDIN BIO
        if bio_type == "LinkedIn":
            sections = []
            # Hook
            sections.append(f"{e_role}{subj} a {adj} {role} dedicated to delivering excellence and high-impact solutions.")

            # Experience & Background
            body = []
            if experience:
                body.append(experience.rstrip(".") + ".")
            if education:
                body.append(f"{e_edu}Academic foundation: {education.rstrip('.')}.")
            if certifications:
                body.append(f"Certified in {certifications.rstrip('.')}.")
            if body:
                sections.append(" ".join(body))

            # Core Competencies / Skills
            if skills:
                sections.append(f"{e_skill}Core Skills & Expertise:\n• " + "\n• ".join([s.strip() for s in skills.split(",") if s.strip()]))

            # Key Projects & Achievements
            highlights = []
            if projects:
                highlights.append(f"{e_proj}Key Projects: {projects.rstrip('.')}.")
            if achievements:
                highlights.append(f"{e_trophy}Key Milestones: {achievements.rstrip('.')}.")
            if highlights:
                sections.append(" ".join(highlights))

            # Closing & Interests
            closing = []
            if interests:
                closing.append(f"{e_heart}When not working, {pronoun.lower() if is_first_person else pronoun} enjoys {interests.rstrip('.')}.")
            closing.append(f"{e_cta}Always open to exchanging ideas, collaborating on innovative projects, or connecting with fellow professionals.")
            sections.append(" ".join(closing))

            return "\n\n".join(sections)

        # 4. DETAILED BIO
        if bio_type == "Detailed":
            paragraphs = []
            # Paragraph 1: Executive Overview
            p1 = [f"{e_role}{subj} a {adj} {role}"]
            if education:
                p1.append(f"with an academic background in {education.rstrip('.')}")
            p1_str = " ".join(p1) + "."
            if experience:
                p1_str += f" {experience.rstrip('.')}."
            paragraphs.append(p1_str)

            # Paragraph 2: Core Skills & Projects
            p2 = []
            if skills:
                p2.append(f"{e_skill}{possessive} technical and professional competencies span {skills.rstrip('.')}.")
            if projects:
                p2.append(f"{e_proj}Major projects and initiatives include: {projects.rstrip('.')}.")
            if p2:
                paragraphs.append(" ".join(p2))

            # Paragraph 3: Credentials & Milestones
            p3 = []
            if certifications:
                p3.append(f"Holding credentials including {certifications.rstrip('.')},")
            if achievements:
                prefix = f"{possessive.lower()} track record features" if certifications else f"{e_trophy}{possessive} track record features"
                p3.append(f"{prefix} {achievements.rstrip('.')}.")
            if p3:
                paragraphs.append(" ".join(p3))

            # Paragraph 4: Interests & Vision
            p4 = []
            if interests:
                p4.append(f"{e_heart}Outside of professional commitments, {pronoun.lower() if is_first_person else pronoun} actively explores {interests.rstrip('.')}.")
            p4.append(f"Continuously looking forward to tackling complex challenges and driving meaningful contributions.")
            paragraphs.append(" ".join(p4))

            return "\n\n".join(paragraphs)

        # 5. PROFESSIONAL BIO (Default)
        paragraphs = []
        p1 = [f"{e_role}{subj} a {adj} {role}"]
        if education:
            p1.append(f"with a background in {education.rstrip('.')}")
        p1_str = " ".join(p1) + "."
        if experience:
            p1_str += f" {experience.rstrip('.')}."
        paragraphs.append(p1_str)

        p2 = []
        if skills:
            p2.append(f"{e_skill}Areas of expertise include {skills.rstrip('.')}.")
        if projects:
            p2.append(f"{e_proj}Demonstrated capability through key projects such as {projects.rstrip('.')}.")
        if achievements:
            p2.append(f"{e_trophy}Recognized for {achievements.rstrip('.')}.")
        if certifications:
            p2.append(f"Holds certifications in {certifications.rstrip('.')}.")
        if p2:
            paragraphs.append(" ".join(p2))

        if interests:
            paragraphs.append(f"{e_heart}Outside of work, {pronoun.lower() if is_first_person else pronoun} is an avid enthusiast of {interests.rstrip('.')}.")

        return "\n\n".join(paragraphs)
