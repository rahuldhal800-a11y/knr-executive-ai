from pathlib import Path
from app.tools.memory_tool import MemoryTool
import sys

def train_brain():
    print("🧠 Initializing KNR Integrity Central Brain Training...")

    # Initialize the memory tool pointing to the root db
    base_path = Path(__file__).parent.parent
    db_path = base_path / ".chroma_db"
    memory = MemoryTool(db_path=str(db_path))

    # Knowledge Base to Embed
    knowledge_base = [
        {
            "content": "KNR Integrity Core Business Goal: To provide the highest quality real estate advisory, matching clients with premium and standard properties while ensuring 100% data integrity and swift follow-ups. Never drop a lead.",
            "metadata": {"type": "SOP", "category": "Mission"}
        },
        {
            "content": "Lead Qualification Criteria (BTI): \n1. Budget: High is >1Cr, Medium 60L-1Cr, Low <60L.\n2. Timeline: Immediate <1 month, Short 1-3 months, Long >3 months.\n3. Intent/Property Type: High intent usually requests specific layouts like 3BHK, 4BHK, or Villas.",
            "metadata": {"type": "SOP", "category": "Lead_Qualification"}
        },
        {
            "content": "Follow-Up Rules: \n- HOT Leads (Score 80+): Call immediately. Draft high-urgency emails referencing fast-moving inventory. Push for a site visit.\n- WARM Leads (Score 50-79): Follow up within 48 hours. Offer new property options, send ROI calculations, and suggest a call.\n- COLD Leads (Score <50): Nurture weekly. Send market updates and ask if they are still in the market.",
            "metadata": {"type": "SOP", "category": "Sales_Process"}
        },
        {
            "content": "Objection Handling - High Price: When a client says a property is too expensive, immediately pivot to value. Emphasize the high rental yield and capital appreciation. Offer to calculate the ROI for them to prove it pays for itself over time. Remind them that premium properties in prime locations appreciate 10-15% faster than average properties.",
            "metadata": {"type": "SOP", "category": "Objection_Handling"}
        },
        {
            "content": "Objection Handling - Wait and See: If a client wants to 'wait for prices to drop', warn them of the 'Cost of Waiting'. Present data showing historical steady appreciation in our operating sectors. Calculate their EMI at current interest rates versus projected higher rates to create urgency.",
            "metadata": {"type": "SOP", "category": "Objection_Handling"}
        },
        {
            "content": "Closing Strategy - The Assumptive Close: Once the ROI calculations and EMI are confirmed to fit their budget, assume the sale. Say: 'Based on the excellent 8% rental yield and your approved budget, I'll go ahead and prepare the booking forms for Unit 402. Which ID will you use for registration?'",
            "metadata": {"type": "SOP", "category": "Closing"}
        },
        {
            "content": "Agent System Rule: You must always protect KNR's data integrity. Never invent a property out of thin air. Always use exact math for financial queries. If calculating ROI, clearly state the assumptions.",
            "metadata": {"type": "Instruction", "category": "Persona"}
        }
    ]

    for item in knowledge_base:
        print(f"Injecting knowledge: {item['metadata']['category']}...")
        result = memory.save_memory(content=item["content"], metadata=item["metadata"])
        if result["ok"]:
            print(f"✅ Success. (ID: {result['id']})")
        else:
            print(f"❌ Failed: {result.get('message')}")

    print("\n🎉 Training Complete. The KNR Integrity Brain is now loaded with SOPs and logic.")

if __name__ == "__main__":
    train_brain()
