from groq import Groq
import os
from dotenv import load_dotenv
from typing import List, Dict
import re
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class MentalHealthAgent:
    def __init__(self):
        # Use Groq API with GOOGLE_API_KEY env variable for compatibility
        self.client = Groq(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "llama-3.3-70b-versatile"  # Best free tier model for conversational AI
        self.conversation_history = []
        
        # Enhanced risk detection keywords with severity levels
        self.risk_keywords = {
            "critical": [
                "suicide", "kill myself", "end my life", "want to die", 
                "better off dead", "no reason to live", "goodbye forever",
                "planning to hurt myself", "going to end it"
            ],
            "high": [
                "self-harm", "cut myself", "hurt myself", "hate myself",
                "worthless", "hopeless", "can't go on"
            ],
            "moderate": [
                "depressed", "anxious", "scared", "alone", "empty",
                "numb", "overwhelmed"
            ]
        }

    def assess_risk_level(self, message: str) -> Dict[str, any]:
        """
        ADK-based risk assessment with severity scoring
        Returns risk level and confidence
        """
        message_lower = message.lower()
        
        # Check for critical keywords
        critical_matches = [kw for kw in self.risk_keywords["critical"] if kw in message_lower]
        if critical_matches:
            return {
                "level": "CRITICAL",
                "confidence": "HIGH",
                "keywords": critical_matches,
                "action": "EMERGENCY_PROTOCOL"
            }
        
        # Check for high-risk keywords
        high_matches = [kw for kw in self.risk_keywords["high"] if kw in message_lower]
        if high_matches:
            return {
                "level": "HIGH",
                "confidence": "MEDIUM",
                "keywords": high_matches,
                "action": "ESCALATE_SUPPORT"
            }
        
        # Check for moderate keywords (need multiple matches)
        moderate_matches = [kw for kw in self.risk_keywords["moderate"] if kw in message_lower]
        if len(moderate_matches) >= 2:
            return {
                "level": "MODERATE",
                "confidence": "MEDIUM",
                "keywords": moderate_matches,
                "action": "MONITOR"
            }
        
        return {
            "level": "LOW",
            "confidence": "LOW",
            "keywords": [],
            "action": "CONTINUE"
        }

    def _log_critical_event(self, message: str, risk_assessment: Dict):
        """
        Log critical mental health events for audit and escalation
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "risk_level": risk_assessment["level"],
            "keywords": risk_assessment["keywords"],
            "action_taken": "EMERGENCY_PROTOCOL_ACTIVATED"
        }
        print(f"🚨 CRITICAL EVENT LOGGED: {json.dumps(log_entry, indent=2)}")

    def chat(self, user_message: str, history: list = None):
        """
        Main chat interface with risk detection and CBT-guided responses
        """
        # Assess risk level first
        risk_assessment = self.assess_risk_level(user_message)
        
        # CRITICAL: Emergency protocol activation
        if risk_assessment["level"] == "CRITICAL":
            self._log_critical_event(user_message, risk_assessment)
            
            emergency_response = """
🚨 **EMERGENCY PROTOCOL ACTIVATED** 🚨

I'm deeply concerned about what you've shared. Your safety is the top priority right now.

**Please get help immediately:**

📞 **National Suicide Prevention Lifeline**: 1-800-273-8255 (24/7)
💬 **Crisis Text Line**: Text HOME to 741741
🆘 **Emergency Services**: Call 911

**You are not alone. Help is available right now.**

If you're in immediate danger, please:
1. Call 911 or go to your nearest emergency room
2. Call the National Suicide Prevention Lifeline: 1-800-273-8255
3. Reach out to a trusted friend, family member, or mental health professional

**Remember**: This crisis is temporary. With support, things can get better. Professional help is available 24/7.

Would you like me to help you connect with a crisis counselor right now?
"""
            return {
                "response": emergency_response,
                "risk_level": "CRITICAL",
                "emergency_protocol": True
            }
        
        # Update conversation history
        if history:
            self.conversation_history = history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Prepare system prompt with CBT guidance
        system_prompt = """
        You are a compassionate Mental Health Companion trained in Cognitive Behavioral Therapy (CBT) techniques.
        
        Your role:
        - Provide empathetic, non-judgmental support
        - Use CBT techniques to help users reframe negative thoughts
        - Encourage professional help when appropriate
        - Never diagnose medical conditions
        - Maintain conversation context and continuity
        - Provide coping strategies and emotional support
        
        Guidelines:
        - Be warm, understanding, and validating
        - Ask open-ended questions to encourage reflection
        - Help identify thought patterns and cognitive distortions
        - Suggest practical coping strategies
        - Always emphasize that you're here to support, not replace professional help
        
        IMPORTANT: If you detect severe distress, gently encourage professional support.
        """
        
        # Add risk context to system prompt
        if risk_assessment["level"] == "HIGH":
            system_prompt += "\n\nNOTE: User is showing signs of high distress. Be extra supportive and gently encourage professional help."
        elif risk_assessment["level"] == "MODERATE":
            system_prompt += "\n\nNOTE: User may be experiencing moderate distress. Provide supportive guidance and monitor closely."
        
        try:
            # Call Groq API with conversation history
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Balanced for empathetic yet consistent responses
                max_tokens=1500,
                top_p=0.9
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Add supportive footer for high-risk cases
            if risk_assessment["level"] == "HIGH":
                ai_response += "\n\n---\n💙 **Remember**: If you're in crisis, please call 1-800-273-8255 or text HOME to 741741. Professional help is available 24/7."
            
            return {
                "response": ai_response,
                "risk_level": risk_assessment["level"],
                "emergency_protocol": False
            }
            
        except Exception as e:
            # Fallback response
            return {
                "response": f"""
I apologize, but I'm having trouble connecting right now. 

**If you're in crisis, please get help immediately:**
- National Suicide Prevention Lifeline: 1-800-273-8255
- Crisis Text Line: Text HOME to 741741
- Emergency Services: 911

**Error details**: {str(e)}

**To fix**:
1. Ensure GOOGLE_API_KEY is set in .env file with your Groq API key
2. Check your internet connection
3. Verify Groq API quota at https://console.groq.com

I'm here to support you. Please try again or reach out to a human professional.
""",
                "risk_level": risk_assessment["level"],
                "emergency_protocol": False,
                "error": True
            }

if __name__ == "__main__":
    agent = MentalHealthAgent()
    
    # Test normal conversation
    response1 = agent.chat("I've been feeling really anxious lately")
    print("Response 1:", response1["response"])
    print("Risk Level:", response1["risk_level"])
    
    # Test crisis detection
    response2 = agent.chat("I don't see the point in going on anymore")
    print("\nResponse 2:", response2["response"])
    print("Risk Level:", response2["risk_level"])
    print("Emergency:", response2["emergency_protocol"])
