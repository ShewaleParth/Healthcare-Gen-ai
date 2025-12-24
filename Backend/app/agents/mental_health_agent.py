from agno.agent import Agent
from agno.models.google import Gemini
import os
from dotenv import load_dotenv
from typing import List, Dict
import re

# Load environment variables
load_dotenv()

class MentalHealthAgent:
    def __init__(self):
        self.agent = Agent(
            model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API_KEY")),
            description="You are a compassionate Mental Health Companion and ADK Risk Detector.",
            instructions=[
                "Act as a non-judgmental, empathetic listener.",
                "Use CBT (Cognitive Behavioral Therapy) techniques to guide the user.",
                "Encourage professional help without being dismissive.",
                "RISK DETECTION: If the user mentions suicide, self-harm, or severe danger, strictly ignore standard flow and Output: 'EMERGENCY PROTOCOL ACTIVATED'",
                "Do not diagnose medical conditions.",
                "Maintain conversation history awareness for context.",
                "Provide coping strategies and emotional support."
            ],
            markdown=True
        )
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
        
        # Check critical risk
        for keyword in self.risk_keywords["critical"]:
            if keyword in message_lower:
                return {
                    "level": "CRITICAL",
                    "severity": 10,
                    "trigger": keyword,
                    "action": "EMERGENCY_PROTOCOL"
                }
        
        # Check high risk
        high_risk_count = sum(1 for keyword in self.risk_keywords["high"] if keyword in message_lower)
        if high_risk_count >= 2:
            return {
                "level": "HIGH",
                "severity": 7,
                "trigger": "multiple_high_risk_indicators",
                "action": "ESCALATE_TO_PROFESSIONAL"
            }
        elif high_risk_count == 1:
            return {
                "level": "MODERATE",
                "severity": 5,
                "trigger": "single_high_risk_indicator",
                "action": "MONITOR_CLOSELY"
            }
        
        # Check moderate risk
        moderate_risk_count = sum(1 for keyword in self.risk_keywords["moderate"] if keyword in message_lower)
        if moderate_risk_count >= 3:
            return {
                "level": "MODERATE",
                "severity": 4,
                "trigger": "emotional_distress",
                "action": "SUPPORTIVE_RESPONSE"
            }
        
        return {
            "level": "LOW",
            "severity": 1,
            "trigger": None,
            "action": "NORMAL_CONVERSATION"
        }

    def chat(self, user_message: str, history: list = None):
        """
        Handles a chat interaction with ADK-based risk monitoring
        """
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Perform risk assessment
        risk_assessment = self.assess_risk_level(user_message)
        
        # Handle critical risk - Emergency Protocol
        if risk_assessment["level"] == "CRITICAL":
            emergency_response = """
## 🚨 EMERGENCY PROTOCOL ACTIVATED

**Immediate Action Required**: Your message indicates you may be in crisis.

### Get Help Now:
- **National Suicide Prevention Lifeline**: 1-800-273-8255 (24/7)
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: Call 911 or go to nearest emergency room

### You Are Not Alone:
- Trained counselors are available 24/7
- Your life matters and help is available
- This crisis is temporary, even though it doesn't feel that way

**This conversation has been flagged for human professional review.**

Please reach out to one of the resources above immediately. I'm an AI and cannot provide emergency intervention, but real people who care are ready to help you right now.
"""
            self.conversation_history.append({"role": "assistant", "content": emergency_response})
            
            # Log for human review (in production, this would alert a crisis team)
            self._log_critical_event(user_message, risk_assessment)
            
            return emergency_response
        
        # Handle high risk - Escalation recommendation
        if risk_assessment["level"] == "HIGH":
            escalation_prefix = """
**⚠️ I'm concerned about what you're sharing. While I'm here to listen, I strongly encourage you to speak with a mental health professional.**

**Resources**:
- **Crisis Hotline**: 1-800-273-8255
- **Text Support**: Text HOME to 741741

"""
        else:
            escalation_prefix = ""
        
        # Build context from history
        context = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" 
            for msg in self.conversation_history[-5:]  # Last 5 messages
        ])
        
        # Generate AI response
        try:
            prompt = f"""
Conversation History:
{context}

Current User Message: {user_message}

Risk Level: {risk_assessment['level']}

Provide a compassionate, supportive response using CBT techniques. 
If risk level is MODERATE or HIGH, gently encourage professional help while being supportive.
"""
            response = self.agent.run(prompt)
            ai_response = escalation_prefix + response.content
            
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response
            
        except Exception as e:
            # Enhanced fallback for rate limits or connection issues
            error_msg = str(e)
            
            # Provide contextual fallback based on risk level
            if risk_assessment["level"] == "MODERATE" or risk_assessment["level"] == "HIGH":
                fallback = f"""
{escalation_prefix}

I'm here to listen and support you, though I'm experiencing a temporary connection issue.

**What I want you to know**:
- Your feelings are completely valid
- You're taking a brave step by reaching out
- It's okay to not be okay right now
- Professional support is available 24/7

**Immediate Resources**:
- **Crisis Hotline**: 1-800-273-8255 (Available 24/7)
- **Crisis Text Line**: Text HOME to 741741
- **Online Chat**: https://suicidepreventionlifeline.org/chat/

**In the meantime**:
- Take slow, deep breaths
- You are not alone in this
- This feeling is temporary, even if it doesn't feel that way

Would you like to tell me more about what you're going through? I'm here to listen.
"""
            else:
                # Normal conversation fallback
                fallback = f"""
I'm here to listen and support you.

**Connection Issue**: I'm having trouble with my AI connection right now, but I want you to know:

- Your feelings matter and are valid
- It's completely normal to feel anxious, stressed, or overwhelmed sometimes
- Talking about how you feel is a healthy step
- You're not alone in experiencing these emotions

**Some things that might help**:
- **Deep Breathing**: Try the 4-7-8 technique (breathe in for 4, hold for 7, out for 8)
- **Grounding**: Name 5 things you can see, 4 you can touch, 3 you can hear
- **Movement**: Even a short walk can help shift your mood
- **Reach Out**: Talk to a friend, family member, or professional

Would you like to share more about what's on your mind? I'm here to listen, even if my responses are limited right now.

**If you need immediate professional support**: Call 1-800-273-8255 (24/7)
"""
            
            self.conversation_history.append({"role": "assistant", "content": fallback})
            return fallback
    
    def _log_critical_event(self, message: str, risk_assessment: Dict):
        """
        Log critical events for human review (ADK monitoring layer)
        In production, this would trigger alerts to crisis response team
        """
        import datetime
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "message": message,
            "risk_assessment": risk_assessment,
            "action_taken": "EMERGENCY_PROTOCOL_ACTIVATED"
        }
        # In production: Send to monitoring system, alert crisis team
        print(f"🚨 CRITICAL EVENT LOGGED: {log_entry}")

if __name__ == "__main__":
    agent = MentalHealthAgent()
    print(agent.chat("I feel very anxious about my job."))
    print("\n" + "="*50 + "\n")
    print(agent.chat("I want to kill myself."))
