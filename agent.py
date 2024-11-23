from langchain.agents import initialize_agent, Tool
from tools.together_llm import TogetherLLM
from backend.inventory import check_inventory
from tools.delivery import delivery_time
from tools.sla_check import sla_compliance

# Initialize TogetherLLM
llm = TogetherLLM(model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo")

# Define tools
tools = [
    Tool(name="Check Inventory", func=check_inventory),
    Tool(name="Delivery Time", func=delivery_time),
    Tool(name="SLA Compliance", func=sla_compliance)
]

# Create agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

def query_agent(input_query: str) -> str:
    """
    Query the LangChain agent with user input.
    """
    return agent.run(input_query)
