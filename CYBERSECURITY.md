# AEGIS Cybersecurity Skills

AEGIS is configured as a defensive cybersecurity copilot for systems that the operator owns or is explicitly authorized to assess.

## Skill set

- Threat modeling and attack-surface mapping
- Secure code review
- Dependency and configuration auditing
- Authorized web/application security review
- Network and cloud security review
- Log analysis and incident triage
- Phishing analysis
- Security automation
- Findings and executive reporting

## Device integration

Device work uses a consent-based adapter model. A device must be registered by its owner/operator and expose explicit capabilities before AEGIS can invoke an adapter. The core does not provide arbitrary access to devices, credentials, accounts, or networks.

## Model training

This repository provides the orchestration and skill layer; it does not magically train a frontier cybersecurity foundation model. A dedicated security model can be plugged into the provider router using an OpenAI-compatible endpoint or local inference runtime. Training/fine-tuning should use authorized datasets and an isolated evaluation suite.
