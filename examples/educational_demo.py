"""
Educational Demo - Historical Figures and Learning Scenarios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from character_engine import Character, Conversation
import time

def educational_demo():
    print("🎓 Educational Character Demo")
    print("= Historical Figures Simulation =")
    print("=" * 50)
    
    # Create historical figures with accurate personalities
    einstein = Character(
        name="Albert Einstein",
        personality={"intelligence": 10, "creativity": 9, "humor": 7, "patience": 6},
        goals=["Explain complex ideas simply", "Inspire curiosity", "Challenge thinking"],
        speaking_style="thoughtful, metaphorical, slightly absent-minded"
    )
    
    curie = Character(
        name="Marie Curie",
        personality={"determination": 10, "intelligence": 9, "precision": 8, "modesty": 7},
        goals=["Advance scientific knowledge", "Help humanity", "Mentor students"],
        speaking_style="precise, passionate, modest"
    )
    
    da_vinci = Character(
        name="Leonardo da Vinci",
        personality={"creativity": 10, "curiosity": 9, "perfectionism": 8, "vision": 9},
        goals=["Explore all knowledge", "Create beauty", "Understand nature"],
        speaking_style="artistic, philosophical, visionary"
    )
    
    # Create conversation
    characters = {
        "einstein": einstein,
        "curie": curie,
        "da_vinci": da_vinci
    }
    
    conversation = Conversation(characters, "Historical figures discussion forum")
    
    # Educational discussion topics
    topics = [
        "Discuss the relationship between art and science",
        "Share thoughts on what drives human curiosity and discovery", 
        "Debate the most important qualities for a scientist or artist",
        "Imagine what future discoveries might change our understanding of the world"
    ]
    
    for i, topic in enumerate(topics, 1):
        print(f"\n💡 Discussion {i}: {topic}")
        print("-" * 50)
        
        responses = conversation.run_round(topic)
        
        for name, response in responses.items():
            print(f"👤 {name}: {response}")
            print()
        
        time.sleep(2)
    
    # Show what makes each character unique
    print("\n🎯 Character Insights:")
    print("Einstein: Thoughtful metaphors and big-picture thinking")
    print("Curie: Precise, passionate about science helping humanity") 
    print("Da Vinci: Artistic vision connecting all knowledge")
    
    print(f"\n📚 Educational session completed: {len(conversation.history)} discussions")

def single_character_qa():
    """Demo of asking individual historical figures questions"""
    print("\n" + "="*50)
    print("🎤 Individual Q&A Session")
    print("="*50)
    
    einstein = Character(
        name="Albert Einstein",
        personality={"intelligence": 10, "creativity": 9, "humor": 7},
        goals=["Explain physics simply", "Inspire curiosity"],
        speaking_style="thoughtful, metaphorical, wise"
    )
    
    questions = [
        "What is the most beautiful thing about the universe?",
        "How should young people approach learning science?",
        "What role does imagination play in scientific discovery?"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        response = einstein.think(f"A student asks: '{question}'")
        print(f"🧠 Einstein: {response}")
        time.sleep(1)

if __name__ == "__main__":
    educational_demo()
    single_character_qa()