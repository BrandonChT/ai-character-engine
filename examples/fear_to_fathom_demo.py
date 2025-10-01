import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from character_engine import Character, Conversation
import time

def fear_to_fathom_demo():
    print("🎮 FEAR TO FATHOM NPC DEMO")
    print("=" * 50)
    
    # Create Fear to Fatham style characters - using only valid parameters
    elias = Character(
        name="Elias - The Caretaker",
        personality="mysterious, protective, traumatized, knowledgeable. Old caretaker who's seen too many disappearances. Knows about ritual sites and lost his brother to the entity.",
        goals="Protect newcomers, hide the terrible truth",
        speaking_style="cryptic, wary, drops ominous hints, speaks slowly"
    )
    
    maya = Character(
        name="Maya - The Survivor", 
        personality="paranoid, fearful, desperate, observant. College student trapped in the woods. Terrified of moving shadows and whispering voices.",
        goals="Warn others, find a way out alive, document the truth",
        speaking_style="breathless, urgent, jumps at shadows, emotional"
    )
    
    print("📝 Created Characters:")
    print(f"• {elias.name}")
    print(f"  Personality: {elias.personality}")
    print(f"• {maya.name}")
    print(f"  Personality: {maya.personality}")
    print("\n")
    
    # Create conversation
    characters = {"elias": elias, "maya": maya}
    conversation = Conversation(characters, "Deep woods at night - distant screams echo")
    
    # Demo dialogues
    scenarios = [
        "I saw something moving in the old cabin...",
        "There are strange symbols carved in the trees nearby",
        "I found a camera with footage of your brother, Elias"
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"🎭 SCENARIO {i}: Player says: '{scenario}'")
        print("-" * 40)
        
        try:
            responses = conversation.run_round(scenario)
            
            for char_name, response in responses.items():
                print(f"{char_name.upper()}: {response}")
                # Remove relationship tracking if it doesn't exist
                # print(f"   [Relationship: {conversation.get_relationship(char_name, 'player')}/10]")
            print("\n")
            
        except Exception as e:
            print(f"⚠️  Response error: {e}")
            print("Trying fallback...")
            # Fallback to individual character responses
            for char_name, character in characters.items():
                try:
                    response = character.respond(scenario)
                    print(f"{char_name.upper()}: {response}")
                except:
                    print(f"{char_name.upper()}: *remains silent*")
            print("\n")
        
        time.sleep(2)  # Pause between scenarios
    
    print("=" * 50)
    print("✨ Demo completed!")

if __name__ == "__main__":
    fear_to_fathom_demo()
