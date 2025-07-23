from nano.agent import Agent

# Step 1. Instantiate the nano agent
print("\nInitializing nano agent...")
agent = Agent(
    model="gemini/gemini-2.5-flash",
    remote=True,
    verbose=True,
    token_limit=64000,
    tool_limit=200,
)

# Step 2. Run the agent on the remote environment
dataset = "gitbug-java"
sample_id = "assertj-assertj-vavr-f4d7f276e87c"
task = """
Some of the tests in this project are failing. Your task is to fix the source code such that all tests pass.
"""

print(f"Running agent on sample_id={sample_id}...")
agent.run(
    task=task,
    sample_id=sample_id,
)
