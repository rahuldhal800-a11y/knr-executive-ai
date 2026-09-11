"""Authorized defensive cybersecurity skill registry for AEGIS.

The skills are deliberately designed for assets the operator owns or is
explicitly authorized to test. They provide planning, passive analysis,
configuration review, secure coding, incident triage, and report generation.
They do not implement unauthorized access, credential theft, persistence,
or destructive exploitation.
"""
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class CyberSkill:
    name: str
    description: str
    category: str
    requires_authorization: bool = True


CYBER_SKILLS: List[CyberSkill] = [
    CyberSkill("threat_modeling", "Build STRIDE-style threat models and attack-surface maps." , "defense"),
    CyberSkill("secure_code_review", "Review application code for common security defects and propose fixes.", "application_security"),
    CyberSkill("dependency_audit", "Identify vulnerable or outdated dependencies and remediation paths.", "application_security"),
    CyberSkill("web_security_review", "Assess an authorized web application against OWASP-style controls.", "web_security"),
    CyberSkill("network_defense_review", "Review firewall, segmentation, exposed services, and defensive configuration.", "network"),
    CyberSkill("cloud_security_review", "Review IAM, storage, network, secrets, logging, and least-privilege configuration.", "cloud"),
    CyberSkill("incident_triage", "Classify alerts, preserve evidence, establish timelines, and recommend containment.", "incident_response"),
    CyberSkill("log_analysis", "Correlate logs and identify suspicious authentication, access, and execution patterns.", "blue_team"),
    CyberSkill("phishing_analysis", "Analyze suspicious messages, links, headers, and attachments defensively.", "blue_team"),
    CyberSkill("security_reporting", "Produce prioritized findings, evidence, severity, remediation, and executive summaries.", "governance"),
    CyberSkill("security_automation", "Create repeatable defensive checks and authorized security workflows.", "automation"),
]


def list_skills() -> List[Dict[str, str]]:
    return [s.__dict__.copy() for s in CYBER_SKILLS]


def get_skill(name: str) -> CyberSkill:
    for skill in CYBER_SKILLS:
        if skill.name == name:
            return skill
    raise KeyError(f"Unknown cybersecurity skill: {name}")
