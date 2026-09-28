"""
Automated Unit Tests for AI Bio Generator
Tests metrics calculation, export formatting, prompt generation,
and the NLP synthesizer across all bio types and tones.
"""

import unittest
from utils import calculate_metrics, format_txt_download, SAMPLE_PROFILES
from bio_generator import BioGenerator, BIO_TYPES, TONES


class TestUtils(unittest.TestCase):
    def test_metrics_empty(self):
        res = calculate_metrics("")
        self.assertEqual(res["word_count"], 0)
        self.assertEqual(res["char_count"], 0)
        self.assertEqual(res["reading_time_sec"], 0)

    def test_metrics_populated(self):
        sample = "Alex is a software engineer with 5 years experience. He loves Python!"
        res = calculate_metrics(sample)
        self.assertEqual(res["word_count"], 12)
        self.assertGreater(res["char_count"], 50)
        self.assertGreater(res["sentence_count"], 0)
        self.assertGreater(res["reading_time_sec"], 0)

    def test_txt_download_formatting(self):
        profile = {
            "name": "Jane Doe",
            "role": "Data Scientist",
            "skills": "Python, SQL",
            "experience": "3 years",
        }
        bio = "Jane Doe is a data scientist specializing in Python and SQL."
        txt = format_txt_download(profile, bio, "Short", "Professional")
        self.assertIn("Jane Doe", txt)
        self.assertIn("Data Scientist", txt)
        self.assertIn("Short", txt)
        self.assertIn("Professional", txt)
        self.assertIn(bio, txt)


class TestBioGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = BioGenerator(api_key="")
        self.profile = SAMPLE_PROFILES["Software Engineer"]

    def test_prompt_grounding_rules(self):
        prompt = self.generator.build_prompt(
            profile_data=self.profile,
            bio_type="LinkedIn",
            tone="Confident",
            pov="First Person (I / me)",
            include_emojis=True,
        )
        self.assertIn("CRITICAL GROUNDING AND ANTI-HALLUCINATION RULES", prompt)
        self.assertIn("STRICT TRUTHFULNESS", prompt)
        self.assertIn("Alex Rivera", prompt)
        self.assertIn("Senior Full-Stack Engineer", prompt)
        self.assertIn("LinkedIn", prompt)
        self.assertIn("Confident", prompt)

    def test_all_bio_types_and_tones(self):
        """Verify that every combination of Bio Type and Tone generates cleanly."""
        for b_type in BIO_TYPES.keys():
            for tone in TONES.keys():
                bio, is_fallback, msg = self.generator.generate_bio(
                    profile_data=self.profile,
                    bio_type=b_type,
                    tone=tone,
                    pov="First Person (I / me)",
                    include_emojis=False,
                )
                self.assertTrue(len(bio.strip()) > 20, f"Bio too short for {b_type} + {tone}")
                self.assertTrue("Alex Rivera" in bio or "I am" in bio or "I " in bio, f"Neither name nor pronoun found in {bio}")
                # Ensure no None / error in output
                self.assertIsNotNone(bio)

    def test_third_person_and_emojis(self):
        bio, _, _ = self.generator.generate_bio(
            profile_data=self.profile,
            bio_type="Short",
            tone="Friendly",
            pov="Third Person (He / She / They)",
            include_emojis=True,
        )
        self.assertIn("Alex Rivera", bio)
        self.assertTrue(len(bio) > 10)


if __name__ == "__main__":
    unittest.main()
