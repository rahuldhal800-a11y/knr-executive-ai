"""Unified skill registry used by the AEGIS planner."""
from app.cyber_skills import list_skills

DIGITAL_SKILLS = {
    "research": "Research, summarize, compare, and synthesize information.",
    "content": "Create and transform business content across supported formats.",
    "coding": "Plan, implement, test, review, and document software changes.",
    "files": "Organize, inspect, transform, and generate authorized files.",
    "automation": "Compose repeatable workflows from registered tools.",
    "cybersecurity": "Authorized defensive cybersecurity analysis and reporting.",
}


def all_skills():
    return {**DIGITAL_SKILLS, "cybersecurity_modules": list_skills()}
