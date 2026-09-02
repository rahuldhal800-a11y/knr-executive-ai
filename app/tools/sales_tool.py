class SalesTool:
    def __init__(self):
        pass

    def get_tool_schemas(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "score_lead",
                    "description": "Evaluate a real estate lead and assign a score based on KNR Integrity criteria (Budget, Timeline, Intent).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "budget_in_lakhs": {
                                "type": "number",
                                "description": "The client's budget in Lakhs (INR)."
                            },
                            "timeline_in_months": {
                                "type": "integer",
                                "description": "How soon the client wants to buy (in months)."
                            },
                            "property_type_interest": {
                                "type": "string",
                                "description": "Type of property they want (e.g., 2BHK, 3BHK, Villa)."
                            }
                        },
                        "required": ["budget_in_lakhs", "timeline_in_months"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "draft_follow_up",
                    "description": "Draft a professional follow-up message for a real estate client.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "client_name": {
                                "type": "string",
                                "description": "Name of the client."
                            },
                            "last_contact_date": {
                                "type": "string",
                                "description": "When we last spoke to them."
                            },
                            "context": {
                                "type": "string",
                                "description": "Context of the previous conversation or what they are looking for."
                            },
                            "urgency": {
                                "type": "string",
                                "enum": ["High", "Medium", "Low"],
                                "description": "The urgency level of this lead."
                            }
                        },
                        "required": ["client_name", "context", "urgency"]
                    }
                }
            }
        ]

    def score_lead(self, budget_in_lakhs: float, timeline_in_months: int, property_type_interest: str = "Unknown") -> dict:
        try:
            score = 0
            reasons = []

            # Budget evaluation
            if budget_in_lakhs >= 100:
                score += 40
                reasons.append("High budget (1Cr+).")
            elif budget_in_lakhs >= 60:
                score += 25
                reasons.append("Medium budget (60L - 1Cr).")
            else:
                score += 10
                reasons.append("Lower budget (<60L).")

            # Timeline evaluation
            if timeline_in_months <= 1:
                score += 40
                reasons.append("Immediate timeline (<1 month).")
            elif timeline_in_months <= 3:
                score += 25
                reasons.append("Short timeline (1-3 months).")
            else:
                score += 10
                reasons.append("Long timeline (>3 months).")

            # Bonus for high-intent property types
            if property_type_interest.upper() in ["3BHK", "4BHK", "VILLA"]:
                score += 20
                reasons.append(f"High value property interest ({property_type_interest}).")
            else:
                score += 10
                reasons.append(f"Standard property interest ({property_type_interest}).")

            # Determine category
            if score >= 80:
                category = "HOT"
            elif score >= 50:
                category = "WARM"
            else:
                category = "COLD"

            return {
                "ok": True,
                "score": score,
                "category": category,
                "reasons": reasons
            }
        except Exception as e:
            return {"ok": False, "message": f"Failed to score lead: {str(e)}"}

    def draft_follow_up(self, client_name: str, context: str, urgency: str, last_contact_date: str = "recently") -> dict:
        try:
            if urgency == "High":
                draft = f"Dear {client_name},\n\nI hope this email finds you well. Following up on our last conversation {last_contact_date} regarding {context}, I wanted to let you know that we have some highly sought-after inventory that matches your exact criteria. Properties in this segment are moving fast.\n\nWhen would be a good time for a quick 5-minute call today or tomorrow to discuss this?\n\nBest Regards,\nKNR Integrity CRM"
            elif urgency == "Medium":
                draft = f"Hi {client_name},\n\nI hope you're having a good week. We spoke {last_contact_date} about {context}. I've put together a few new property options that align perfectly with what you are looking for.\n\nLet me know if you'd like me to send them over, or if you have a few minutes for a call this week.\n\nBest,\nKNR Integrity CRM"
            else:
                draft = f"Hi {client_name},\n\nJust checking in with you! We last connected {last_contact_date} regarding {context}. Are you still in the market for a property? We have some interesting new developments in our portfolio.\n\nPlease let me know if you'd like to receive some market updates.\n\nBest,\nKNR Integrity CRM"

            return {"ok": True, "draft": draft}
        except Exception as e:
            return {"ok": False, "message": f"Failed to draft follow-up: {str(e)}"}
