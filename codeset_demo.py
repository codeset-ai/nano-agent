from nano.agent import Agent

# Step 1. Instantiate the nano agent
print("\nInitializing nano agent...")
agent = Agent(
    model="openai/gpt-4.1",
    remote=True,
    verbose=True,
    token_limit=64000,
    tool_limit=100,
)

# Step 2. Run the agent on the remote environment
sample_id = "traccar-traccar-95fdfd770130"
task = """
Some of the tests in this project are failing. Your task is to fix the source code such that all tests pass.
If needed, add the following Java SDK to the PATH: '/opt/hostedtoolcache/Java_Zulu_jdk/11.0.21-9/x64/bin'.
"""

print(f"Running agent on sample_id={sample_id}...")
agent.run(
    task=task,
    sample_id=sample_id,
)
