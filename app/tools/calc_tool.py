class CalcTool:
    def __init__(self):
        pass

    def get_tool_schemas(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "calculate_emi",
                    "description": "Calculate the Equated Monthly Installment (EMI) for a real estate loan.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "principal": {
                                "type": "number",
                                "description": "The total loan amount (Principal) in INR."
                            },
                            "annual_interest_rate": {
                                "type": "number",
                                "description": "The annual interest rate (percentage). E.g., 8.5 for 8.5%."
                            },
                            "tenure_years": {
                                "type": "integer",
                                "description": "The loan tenure in years."
                            }
                        },
                        "required": ["principal", "annual_interest_rate", "tenure_years"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_roi",
                    "description": "Calculate the Return on Investment (ROI) and Rental Yield for a property.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "property_cost": {
                                "type": "number",
                                "description": "Total cost of the property in INR."
                            },
                            "monthly_rent": {
                                "type": "number",
                                "description": "Expected monthly rent in INR."
                            },
                            "annual_appreciation_rate": {
                                "type": "number",
                                "description": "Expected annual capital appreciation rate (percentage). E.g. 5 for 5%."
                            }
                        },
                        "required": ["property_cost", "monthly_rent", "annual_appreciation_rate"]
                    }
                }
            }
        ]

    def calculate_emi(self, principal, annual_interest_rate, tenure_years) -> dict:
        principal = float(principal)
        annual_interest_rate = float(annual_interest_rate)
        tenure_years = int(tenure_years)
        try:
            if principal <= 0 or annual_interest_rate <= 0 or tenure_years <= 0:
                return {"ok": False, "message": "All inputs must be greater than zero."}

            r = (annual_interest_rate / 12) / 100  # monthly interest rate
            n = tenure_years * 12                  # total number of months

            emi = principal * r * ((1 + r)**n) / (((1 + r)**n) - 1)
            total_payment = emi * n
            total_interest = total_payment - principal

            return {
                "ok": True,
                "emi": round(emi, 2),
                "total_interest": round(total_interest, 2),
                "total_payment": round(total_payment, 2)
            }
        except Exception as e:
            return {"ok": False, "message": f"Calculation failed: {str(e)}"}

    def calculate_roi(self, property_cost, monthly_rent, annual_appreciation_rate) -> dict:
        property_cost = float(property_cost)
        monthly_rent = float(monthly_rent)
        annual_appreciation_rate = float(annual_appreciation_rate)
        try:
            if property_cost <= 0:
                return {"ok": False, "message": "Property cost must be greater than zero."}

            annual_rent = monthly_rent * 12
            rental_yield = (annual_rent / property_cost) * 100
            total_roi = rental_yield + annual_appreciation_rate

            return {
                "ok": True,
                "annual_rent": round(annual_rent, 2),
                "rental_yield_percentage": round(rental_yield, 2),
                "capital_appreciation_percentage": round(annual_appreciation_rate, 2),
                "total_annual_roi_percentage": round(total_roi, 2)
            }
        except Exception as e:
            return {"ok": False, "message": f"Calculation failed: {str(e)}"}
