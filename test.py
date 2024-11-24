from Chatbot.agent import SLAAgent
model_name = "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo" 
from Chatbot.sla_check import get_orders_pending_sla_check
import json
# # Function to create a new agent instance
def create_new_agent(model: str) -> SLAAgent:
    return SLAAgent(model=model)

# Questions to Ask
questions = [
     "Do I have any orders pending SLA checks?",
    "Show me all listings added after 2023-01-01.",
    "Can I deliver 800 pieces of listing ID c91d6409f3862e68f6a4a71c3e0d6ec9 within 2 days",
    "What are the most common reasons for SLA violations?",
    "How many SLA violations were due to inventory issues?",
  
]

questions2 = [
    "Show me all listings added after 2023-01-01.",
    "What is the inventory status for listing ID c91d6409f3862e68f6a4a71c3e0d6ec9?",
      "Do I have any orders pending SLA checks?",
    "Can I deliver 800 pieces of listing ID c91d6409f3862e68f6a4a71c3e0d6ec9 within 2 days"
    "Show me all listings added after 2023-01-01.",
    "What is the inventory status for listing ID c91d6409f3862e68f6a4a71c3e0d6ec9?",
]

# Array to store questions and answers
qa_array = []

for question in questions:
    print(f"Question: {question}")
    
    # Create a fresh agent instance for each question
    agent = create_new_agent(model_name)
    
    # Get the response
    response = agent.ask_question(question)
    print(f"Response:\n{response}\n")
    
    # Append question and response to the array
    qa_array.append({
        "question": question,
        "response": response
    })

# Output the array
print("Questions and Answers Array:")
print(json.dumps(qa_array, indent=2))

# get_orders_pending_sla_check()