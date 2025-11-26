import asyncio
from src.graph import graph

async def main():
    print("--- Test 1: Research Request ---")
    inputs = {"messages": ["Please research the latest AI trends."]}
    async for event in graph.astream(inputs):
        for key, value in event.items():
            print(f"Node '{key}':")
            print(f"  State: {value}")
    
    print("\n--- Test 2: Coding Request ---")
    inputs = {"messages": ["Please write some python code."]}
    async for event in graph.astream(inputs):
        for key, value in event.items():
            print(f"Node '{key}':")
            print(f"  State: {value}")

    print("\n--- Test 3: General Request (Should Finish) ---")
    inputs = {"messages": ["Hello there!"]}
    async for event in graph.astream(inputs):
        for key, value in event.items():
            print(f"Node '{key}':")
            print(f"  State: {value}")

    print("\n--- Test 4: Long Context Request (Should Trim) ---")
    # Simulate a long conversation
    long_history = ["User: Message " + str(i) for i in range(50)]
    long_history.append("User: Please research quantum computing.")
    inputs = {"messages": long_history}
    
    # Note: We can't easily verify trimming in the output without logging, 
    # but running this without error confirms it handles the load.
    async for event in graph.astream(inputs):
        for key, value in event.items():
            print(f"Node '{key}':")
            print(f"  State: {value}")

if __name__ == "__main__":
    asyncio.run(main())
