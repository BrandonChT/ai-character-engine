"""
Game NPC Demo - Showcasing RPG-style character interactions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from character_engine import Character, Conversation
import time

def game_npc_demo():
    print("🎮 RPG NPC Character Demo")
    print("=" * 50)
    
    # Create RPG characters with distinct personalities
    blacksmith = Character(
        name="Gromm Steelhand",
        personality={"strength": 9, "craftsmanship": 10, "temper": 7, "honesty": 8},
        goals=["Craft the finest weapons", "Protect the village", "Train apprentices"],
        speaking_style="gruff, practical, no-nonsense"
    )
    
    tavern_keeper = Character(
        name="Mara Goldcup", 
        personality={"charisma": 8, "business_sense": 9, "gossip": 7, "kindness": 6},
        goals=["Run profitable tavern", "Know all town gossip", "Keep customers happy"],
        speaking_style="cheerful, gossipy, business-savvy"
    )
    
    mysterious_stranger = Character(
        name="Corvus Shadowstep",
        personality={"stealth": 10, "intelligence": 8, "mystery": 9, "loyalty": 4},
        goals=["Gather information", "Stay anonymous", "Complete contracts"],
        speaking_style="cryptic, mysterious, precise"
    )
    
    # Set up initial relationships
    blacksmith.relationships = {"Mara Goldcup": 7, "Corvus Shadowstep": 3}
    tavern_keeper.relationships = {"Gromm Steelhand": 7, "Corvus Shadowstep": 5}
    mysterious_stranger.relationships = {"Gromm Steelhand": 3, "Mara Goldcup": 5}
    
    # Create conversation
    characters = {
        "blacksmith": blacksmith,
        "tavern_keeper": tavern_keeper, 
        "mysterious_stranger": mysterious_stranger
    }
    
    conversation = Conversation(characters, "Evening at the Rusty Anchor Tavern")
    
    # Game-like scenarios
    scenarios = [
        "The blacksmith enters the tavern after a long day of work",
        "A mysterious stranger in the corner asks about recent strange events in town",
        "They hear rumors of bandits approaching the village",
        "The tavern keeper shares gossip about the mayor's secret meeting"
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎭 Scene {i}: {scenario}")
        print("-" * 50)
        
        responses = conversation.run_round(scenario)
        
        for name, response in responses.items():
            print(f"🗣️  {name}: {response}")
            print()
        
        time.sleep(2)  # Pause between scenes
    
    # Show relationship evolution
    print("\n📊 Relationship Evolution:")
    print(f"Blacksmith → Tavern Keeper: {blacksmith.relationships['Mara Goldcup']}/10")
    print(f"Blacksmith → Stranger: {blacksmith.relationships['Corvus Shadowstep']}/10")
    print(f"Tavern Keeper → Stranger: {tavern_keeper.relationships['Corvus Shadowstep']}/10")
    
    print(f"\n💾 Game session recorded: {len(conversation.history)} scenes")

if __name__ == "__main__":
    game_npc_demo()