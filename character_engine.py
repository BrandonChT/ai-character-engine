"""
AI Character Engine - Complete Standalone Library
Consistent, personality-driven AI characters for games and applications
"""

import requests
import json
import time
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

class Character:
    """A consistent AI character with personality, memory, and relationships"""
    
    def __init__(self, 
                 name: str, 
                 personality: Dict[str, Any],
                 goals: List[str], 
                 speaking_style: str,
                 relationships: Optional[Dict[str, int]] = None,
                 ollama_url: str = "http://localhost:11434/api/generate"):
        
        self.name = name
        self.personality = personality
        self.goals = goals
        self.speaking_style = speaking_style
        self.relationships = relationships or {}
        self.ollama_url = ollama_url
        self.conversation_history = []
        
    def _validate_and_clean_response(self, text: str) -> str:
        """Enhanced validation with context consistency fixes"""
        if not text or len(text.strip()) < 10:
            return f"{self.name} remains silent, deep in thought."
        
        # Remove common garbage patterns
        garbage_patterns = [
            r'###.*?###', r'Instruction:.*', r'System:.*', 
            r'{"role".*?}', r'<\|.*?\|>', r'```.*?```'
        ]
        
        for pattern in garbage_patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL)
        
        # Check for obvious garbage
        if any(keyword in text.lower() for keyword in ['instruction', 'system:', '###', 'assistant']):
            return f"{self.name} carefully considers the situation."
        
        # Better sentence completion detection
        sentences = re.split(r'[.!?]', text)
        if sentences and not sentences[-1].strip().endswith(('.', '!', '?')):
            # Remove incomplete last sentence
            text = '.'.join(sentences[:-1]) + '.' if len(sentences) > 1 else text
        
        # Ensure proper word boundaries
        words = text.split()
        if len(words) > 300:  # More reasonable limit
            # Find a good stopping point
            for i in range(min(250, len(words)), len(words)):
                if words[i].endswith(('.', '!', '?')):
                    text = ' '.join(words[:i+1])
                    break
            else:
                text = ' '.join(words[:250]) + "..."
        
        return text.strip()
    
    def _analyze_conversation_tone(self, message: str) -> str:
        """Simple tone analysis for relationship updates"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['agree', 'support', 'trust', 'together', 'help']):
            return "cooperative"
        if any(word in message_lower for word in ['no', 'wrong', 'dangerous', 'stupid', 'against']):
            return "confrontational"
        if any(word in message_lower for word in ['believe', 'understand', 'appreciate', 'respect']):
            return "trust_building"
        
        return "neutral"
    
    def think(self, situation: str, context: Dict[str, Any] = None, max_retries: int = 2) -> str:
        """Generate a response based on character personality and situation"""
        context = context or {}
        
        # Build relationship context
        rel_context = ""
        if context.get('other_characters'):
            other_chars = context['other_characters']
            rel_scores = [f"{name}:{self.relationships.get(name, 5)}" 
                         for name in other_chars if name != self.name]
            if rel_scores:
                rel_context = f"\nRelationships: {', '.join(rel_scores)}"
        
        # Build the thinking prompt
        thinking_prompt = f"""You are {self.name}. Respond naturally in 150-300 words.

PERSONALITY: {self.speaking_style}
GOAL: {', '.join(self.goals)}
PERSONALITY_TRAITS: {json.dumps(self.personality)}{rel_context}

SITUATION: {situation}
CONTEXT: {json.dumps(context) if context else 'None'}

IMPORTANT: 
- Keep responses concise and complete
- End sentences properly (., !, ?)
- Avoid cutting off mid-thought
- Speak naturally in character

Respond as {self.name}:"""
        
        payload = {
            "model": "phi3",
            "prompt": thinking_prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "num_predict": 250,
                "seed": hash(self.name + situation) % 10000
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(self.ollama_url, json=payload, timeout=45)
                
                if response.status_code == 200:
                    result = response.json().get('response', '').strip()
                    validated = self._validate_and_clean_response(result)
                    
                    if len(validated.split()) >= 15:
                        # Store in conversation history
                        self.conversation_history.append({
                            "timestamp": datetime.now().isoformat(),
                            "situation": situation,
                            "response": validated
                        })
                        return validated
                    else:
                        time.sleep(1)
                        continue
                        
                else:
                    print(f"⚠️ API Error {response.status_code} for {self.name}")
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Timeout for {self.name}, attempt {attempt + 1}")
            except Exception as e:
                print(f"❌ Error for {self.name}: {str(e)}")
            
            time.sleep(2)
        
        # Fallback response
        fallbacks = {
            "direct": "We need to focus on practical solutions.",
            "compassionate": "There must be a peaceful way through this.",
            "calculating": "I'm assessing our options carefully."
        }
        
        # Choose fallback based on speaking style
        if "compassion" in self.speaking_style.lower():
            return fallbacks["compassionate"]
        elif "calculating" in self.speaking_style.lower():
            return fallbacks["calculating"]
        else:
            return fallbacks["direct"]
    
    def update_relationship(self, other_character: str, change: int):
        """Update relationship score with another character"""
        current = self.relationships.get(other_character, 5)
        self.relationships[other_character] = max(1, min(10, current + change))
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        return self.conversation_history[-limit:]

class Conversation:
    """Manages multi-character conversations with memory"""
    
    def __init__(self, characters: Dict[str, Character], scenario: str):
        self.characters = characters
        self.scenario = scenario
        self.history = []
        
    def run_round(self, situation: str) -> Dict[str, str]:
        """Run one round of conversation between all characters"""
        responses = {}
        
        for name, character in self.characters.items():
            other_characters = [n for n in self.characters.keys() if n != name]
            context = {
                'other_characters': other_characters,
                'scenario': self.scenario,
                'round_number': len(self.history) + 1
            }
            
            response = character.think(situation, context)
            responses[name] = response
            
            # Update relationships based on conversation tone
            tone = character._analyze_conversation_tone(response)
            for other_name in other_characters:
                if tone == "cooperative":
                    character.update_relationship(other_name, 1)
                elif tone == "confrontational":
                    character.update_relationship(other_name, -1)
        
        # Store round in history
        self.history.append({
            "round": len(self.history) + 1,
            "situation": situation,
            "responses": responses,
            "timestamp": datetime.now().isoformat()
        })
        
        return responses
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the entire conversation"""
        return f"Conversation with {len(self.characters)} characters over {len(self.history)} rounds"

# Version info
__version__ = "1.0.0" 
__author__ = "Abhinaw Singh"
__license__ = "MIT"