"""
Simple Demo - AI Character Engine
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from character_engine import Character, Conversation

def main():
    print("🤖 AI Character Engine - Simple Demo")
    print("=" * 50)
    
    # Create some characters
    knight = Character(
        name="Sir Galadon",
        personality={"bravery": 9, "loyalty": 8, "wisdom": 6},
        goals=["Protect the kingdom", "Find the lost artifact"],
        speaking_style="formal, honorable, slightly poetic"
    )
    
    merchant = Character(
        name="Baron Von Trader",
        personality={"friendliness": 7, "greed": 8, "cunning": 6},
        goals=["Make profit", "Expand business", "Stay safe"],
        speaking_style="charming, persuasive, money-focused"
    )
    
    # Set up relationships
    knight.relationships["Baron Von Trader"] = 6  # Neutral-positive
    merchant.relationships["Sir Galadon"] = 5     # Neutral
    
    # Create a conversation
    characters = {"knight": knight, "merchant": merchant}
    conversation = Conversation(characters, "Medieval town marketplace")
    
    # Run some conversation rounds
    situations = [
        "The knight approaches the merchant's stall",
        "The merchant shows a rare magical artifact",
        "They hear rumors of dragons approaching the town"
    ]
    
    for i, situation in enumerate(situations, 1):
        print(f"\n🔄 Round {i}: {situation}")
        print("-" * 40)
        
        responses = conversation.run_round(situation)
        
        for name, response in responses.items():
            print(f"{name}: {response}")
        
        time.sleep(1)  # Pause between rounds
    
    # Show final relationships
    print(f"\n📊 Final Relationships:")
    print(f"Knight -> Merchant: {knight.relationships['Baron Von Trader']}/10")
    print(f"Merchant -> Knight: {merchant.relationships['Sir Galadon']}/10")
    
    print(f"\n💾 Conversation history: {len(conversation.history)} rounds recorded")

if __name__ == "__main__":
    import time
    main()