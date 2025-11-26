import os
import asyncio
from langsmith import Client
from langchain.smith import RunEvalConfig, run_on_dataset
from langchain_openai import ChatOpenAI
from src.graph import graph

# Define a simple dataset (in a real scenario, this would be uploaded to LangSmith)
example_inputs = [
    ("What is the capital of France?", "Paris"),
    ("Write a python function to add two numbers.", "def add(a, b): return a + b"),
]

async def run_eval():
    client = Client()
    
    # Check if keys are present
    if not os.environ.get("LANGCHAIN_API_KEY") or not os.environ.get("OPENAI_API_KEY"):
        print("Skipping evaluation: Missing API keys.")
        return

    # Define the evaluator
    eval_config = RunEvalConfig(
        evaluators=["qa"],
        llm=ChatOpenAI(model="gpt-4o")
    )

    # Create a dataset in LangSmith (if not exists)
    dataset_name = "Agent Prototype Eval"
    if not client.has_dataset(dataset_name=dataset_name):
        dataset = client.create_dataset(dataset_name=dataset_name)
        for q, a in example_inputs:
            client.create_example(inputs={"messages": [q]}, outputs={"answer": a}, dataset_id=dataset.id)

    # Run evaluation
    # Note: We need to wrap the graph to match the expected input/output format for run_on_dataset
    # This is a simplified example.
    print(f"Running evaluation on dataset: {dataset_name}")
    
    # For demonstration, we just print this message as full integration requires more setup
    # run_on_dataset(...) 

if __name__ == "__main__":
    asyncio.run(run_eval())
