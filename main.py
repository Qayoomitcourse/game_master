# 📦 Imports
import os
from dotenv import load_dotenv 
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel  
from agents.run import RunConfig  

from game_tools import roll_dice, generate_event, roll_dice_tool, generate_event_tool

# 🌐 Load API Key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

# 🤖 Create OpenAI-compatible client for Gemini
client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 💬 Define the model used by all agents
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# ⚙️ Runner configuration
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True  # Disable OpenAI tracing (for debugging/logging)
)

# 🎭 Narrator Agent - guides the main story
narrator_agent = Agent(
    name="Narrator Agent",
    instructions="""
You are a fantasy game narrator. Tell the story, describe the scene, and prompt the player for choices.
If a fight begins, hand off to MonsterAgent. If loot or item appears, hand off to ItemAgent.
""",
    model=model,
    tools=[generate_event_tool]  # ✅ Fixed
)

# 🐉 Monster Agent
monster_agent = Agent(
    name="Monster Agent",
    instructions="""
You simulate fantasy combat with monsters. Use roll_dice() to determine hit success and damage.
Narrate the battle in turns. End the fight and return control to NarratorAgent when the monster is defeated.
""",
    model=model,
    tools=[roll_dice_tool]  # ✅ Fixed
)
# 🪙 Item Agent - handles items and rewards
item_agent = Agent(
    name="Item Agent",
    instructions="""
You manage inventory and rewards. When loot is found, describe it and ask the player if they want to keep or use it.
Return control to NarratorAgent when done.
""",
    model=model
)

# 🚀 Main Adventure Loop
def main():
    print("🎮 Welcome to the Fantasy Adventure Game!")
    player_name = input("What is your player's name? -> ").strip()


    intro = f"Begin the story with a player named {player_name} ."
    result1 = Runner.run_sync(narrator_agent, intro, run_config=config)
    print("\n📜 Story Begins:\n", result1.final_output)

    # random encounter
    print("\n🎲 Rolling for random encounter...\n")
    roll = roll_dice()

    # 👾 Monster Encounter
    if roll > 11:
        print("👾 A monster appears!")
        result2 = Runner.run_sync(monster_agent, f"A wild beast blocks {player_name}'s path!", run_config=config,  max_turns=30 )
        print("\n⚔️ Battle:\n", result2.final_output)

    # 🎁 Item Discovery
    elif 8 < roll <= 11:
        print("🎁 An item glows in the darkness...")
        result3 = Runner.run_sync(item_agent, f"{player_name} finds a magical chest in the corner.", run_config=config)
        print("\n💎 Loot:\n", result3.final_output)

    
    else:
        print("🌿 The path remains calm for now...")

    # 📚 Continue the story with a new generated event
    event = generate_event()
    result4 = Runner.run_sync(narrator_agent, f"After that, {player_name} continues and: {event}", run_config=config)
    print("\n📚 Continued Adventure:\n", result4.final_output)

# ▶️ Run the game
if __name__ == "__main__":
    main()
