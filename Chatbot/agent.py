import json
from langchain_together import ChatTogether
from langchain.agents import initialize_agent, Tool, AgentType
from Chatbot.sla_check import check_order_sla
from Chatbot.delivery import get_order
from Chatbot.inventory import check_inventory, get_listings_after_date, get_all_listings
import tiktoken  # For accurate tokenization
class SLAAgent:
    DEFAULT_MAX_TOKENS = 8000  # Fallback max token limit

    def __init__(self, model: str):
        """
        Initialize the SLA Agent with the specified Together AI model.
        """
        self.chat = ChatTogether(model=model)
        self.model_max_tokens = self.get_model_token_limit(model) or self.DEFAULT_MAX_TOKENS
        self.tools = self.initialize_tools()
        self.agent = initialize_agent(
            self.tools,
            self.chat,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

    def initialize_tools(self):
        """
        Define tools for the agent with appropriate descriptions and error handling.
        """
        return [
            Tool(
                name="get_order",
                func=self.get_order_tool,
                description="Fetches order details using an order ID. Returns JSON data with the order details or an error message.",
            ),
            Tool(
                name="check_order_sla",
                func=self.check_order_sla_tool,
                description="Verifies the SLA status for an order. Requires valid JSON input of order details. Returns SLA results or errors.",
            ),
            Tool(
                name="check_inventory",
                func=self.check_inventory_tool,
                description="Checks inventory availability for a given listing ID. Returns inventory data in JSON format or errors.",
            ),
            Tool(
                name="get_listings_after_date",
                func=self.get_listings_after_date_tool,
                description="Fetches all listings added after a specified date (YYYY-MM-DD). Returns a JSON array or an error.",
            ),
            Tool(
                name="get_all_listings",
                func=self.get_all_listings_tool,
                description="Retrieves all available listings from the database in JSON format.",
            ),
        ]

    def get_model_token_limit(self, model: str) -> int:
        """
        Determine the token limit for a specific model.
        """
        model_limits = {
            "meta-llama/Llama-3-70b-chat-hf": 8192,
            "meta-llama/Llama-2-13b-chat-hf": 4096,
        }
        return model_limits.get(model, None)

    def count_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in the input text using tiktoken.
        """
        encoding = tiktoken.get_encoding("cl100k_base")  # Update with appropriate encoding for your model
        return len(encoding.encode(text))

    def truncate_text(self, text: str, max_tokens: int) -> str:
        """
        Truncate the input text to ensure it doesn't exceed the max token limit.
        """
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text)
        if len(tokens) > max_tokens:
            truncated_tokens = tokens[:max_tokens]
            return encoding.decode(truncated_tokens)
        return text

    def log_error(self, tool_name: str, error_message: str):
        """
        Log errors with the tool name for better debugging.
        """
        print(f"[ERROR] {tool_name}: {error_message}")

    def safe_json(self, data):
        """
        Convert data to a JSON string with error handling.
        """
        try:
            return json.dumps(data)
        except (TypeError, ValueError) as e:
            self.log_error("JSON Conversion", str(e))
            return json.dumps({"error": "Failed to convert data to JSON."})

    def get_order_tool(self, order_id: str) -> str:
        try:
            order = get_order(order_id)
            if not order:
                return self.safe_json({"error": f"Order with ID {order_id} not found."})
            return self.safe_json(order)
        except Exception as e:
            self.log_error("get_order", str(e))
            return self.safe_json({"error": "Failed to fetch order details."})

    def check_order_sla_tool(self, order_data: str) -> str:
        try:
            order_dict = json.loads(order_data)
            sla_status = check_order_sla(order_dict)
            return self.safe_json(sla_status)
        except (json.JSONDecodeError, Exception) as e:
            self.log_error("check_order_sla", str(e))
            return self.safe_json({"error": "Invalid input format or SLA check failure."})

    def check_inventory_tool(self, listing_id: str) -> str:
        try:
            inventory_status = check_inventory(listing_id)
            if not inventory_status:
                return self.safe_json({"error": f"No inventory details found for listing ID {listing_id}."})
            return self.safe_json(inventory_status)
        except Exception as e:
            self.log_error("check_inventory", str(e))
            return self.safe_json({"error": "Failed to check inventory."})

    def get_listings_after_date_tool(self, date: str) -> str:
        try:
            listings = get_listings_after_date(date)
            if not listings:
                return self.safe_json({"error": f"No listings found after {date}."})
            return self.safe_json(listings)
        except Exception as e:
            self.log_error("get_listings_after_date", str(e))
            return self.safe_json({"error": "Failed to fetch listings."})

    def get_all_listings_tool(self, query=None) -> str:
        try:
            listings = get_all_listings()
            if not listings:
                return self.safe_json({"error": "No listings found in the database."})
            return self.safe_json(listings)
        except Exception as e:
            self.log_error("get_all_listings", str(e))
            return self.safe_json({"error": "Failed to fetch all listings."})

    def categorize_response(self, response: str) -> str:
        """
        Categorizes the response based on specific keywords or structures.
        """
        if "order" in response.lower():
            return "Order Info"
        elif "inventory" in response.lower():
            return "Inventory Info"
        elif "listing" in response.lower():
            return "Listings Info"
        else:
            return "General Info"
    def ask_question(self, question: str) -> dict:
        """
        Pass a natural language question to the LangChain agent, ensuring token limits.
        The response will be returned in a dictionary with 'text', 'data', and 'category' fields. 
        The 'data' field will contain any relevant list based on the query context.
        """
        try:
            # Ensure the input does not exceed the maximum token limit
            input_tokens = self.count_tokens(question)
            max_tokens_for_question = self.model_max_tokens - 500  # Reserve tokens for system prompts/context

            if input_tokens > max_tokens_for_question:
                print(f"Input exceeds max token limit. Truncating to {max_tokens_for_question} tokens.")
                question = self.truncate_text(question, max_tokens_for_question)

            # Reinitialize ChatTogether for each query to ensure no memory of previous conversation
            self.chat = ChatTogether()  # Assuming this initializes the necessary components for the assistant

            # Run the question through the agent
            response = self.agent.run(question)

            # Clean the response by stripping unnecessary assistant context or waiting messages
            cleaned_response = response.split("\nassistant")[0].strip()

            # Identify relevant data based on the question (this could be dynamic based on specific queries)
            data = []
            if "inventory status" in question.lower():
                listing_id = self.extract_listing_id(question)
                inventory_data = self.get_inventory_data(listing_id)
                data = [{
                    "listing_id": listing_id,
                    "available_stock": inventory_data["stock"],
                    "product_name": inventory_data["name"],
                    "price": inventory_data["price"]
                }]
            elif "order status" in question.lower():
                order_id = self.extract_order_id(question)
                order_status = self.get_order_status(order_id)
                data = [{
                    "order_id": order_id,
                    "status": order_status["status"],
                    "expected_delivery": order_status["delivery_date"]
                }]

            # Categorize the response based on the content
            category = self.categorize_response(cleaned_response)

            # Structure the response as a dictionary
            response_dict = {
                "text": cleaned_response,
                "data": data,
                "category": category
            }

            return response_dict

        except Exception as e:
            self.log_error("ask_question", str(e))

            # Ensure the agent doesn't enter into an infinite loop or process errors excessively
            return {
                "text": "An error occurred while processing your question. Please try again later.",
                "data": [],
                "category": "Error"
            }

# model_name = "meta-llama/Llama-3-70b-chat-hf"  # Replace with your desired Together AI model

# # Function to create a new agent instance
# def create_new_agent(model: str) -> SLAAgent:
#     return SLAAgent(model=model)

# # Questions to Ask
# questions = [
#     "Show me all listings added after 2023-01-01.",
#     "Can you fetch all available listings from the database?",
#     "What is the inventory status for listing ID c91d6409f3862e68f6a4a71c3e0d6ec9?",
# ]
# questions=[
#     "Can you fetch all available listings from the database?",
#     "Show me all listings added after 2023-01-01.",
#     "What is the inventory status for listing ID c91d6409f3862e68f6a4a71c3e0d6ec9?",
   
# ]


# # Array to store questions and answers
# qa_array = []

# for question in questions:
#     print(f"Question: {question}")
    
#     # Create a fresh agent instance for each question
#     agent = create_new_agent(model_name)
    
#     # Get the response
#     response = agent.ask_question(question)
#     print(f"Response:\n{response}\n")
    
#     # Append question and response to the array
#     qa_array.append({
#         "question": question,
#         "response": response
#     })

# # Output the array
# print("Questions and Answers Array:")
# print(json.dumps(qa_array, indent=2))


