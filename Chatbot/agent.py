import json
from langchain_together import ChatTogether
from langchain.agents import initialize_agent, Tool, AgentType
from Chatbot.sla_check import check_order_sla,get_orders_pending_sla_check
from Chatbot.delivery import get_order
from Chatbot.inventory import check_inventory, get_listings_after_date, get_all_listings
import re
import tiktoken  # For accurate tokenization
     
class SLAAgent:
    DEFAULT_MAX_TOKENS = 8000  # Fallback max token limit

    def __init__(self, model: str):
        """
        Initialize the SLA Agent with the specified Together AI model.
        """
        self.chat = ChatTogether(model=model)
        self.model_max_tokens = self.DEFAULT_MAX_TOKENS
        self.tools = self.initialize_tools()
        self.agent = initialize_agent(
            self.tools,
            self.chat,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )
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
    def initialize_tools(self):
        """
        Define tools for the agent with appropriate descriptions and error handling.
        """
        return [
            Tool(
                name="get_order",
                func=self.get_order_tool,
                description="Fetches order details using an order ID. Returns JSON data with the order details or an error message."
            ),
            Tool(
                name="check_order_sla",
                func=self.check_order_sla_tool,
                return_direct = True,
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
                description="Fetches all listings added after a specified date (YYYY-MM-DD). Do not check further if this returns null. Returns a JSON array or an error.",
                return_direct = True,
            ),
            Tool(
                name="get_all_listings",
                func=self.get_all_listings_tool,
                return_direct = True,
                description="Retrieves all available listings from the database in JSON format.",
            ),
            Tool(
                name="extract_listing_id",
                func=self.extract_listing_id_tool,
                description="Extracts the listing ID from a given question. Assumes the listing ID follows the format: c91d6409f3862e68f6a4a71c3e0d6ec9.",
            ),
            Tool(
                name="extract_order_id",
                func=self.extract_order_id_tool,
                description="Extracts the order ID from a given question. Assumes the order ID follows the format: 0rj8FZJE.",
                ),
            Tool(
                name="extract_quantity_and_days",
                func=self.extract_quantity_and_days_tool,
                description="Extracts the quantity and time frame from a question. Returns data with quantity, listing ID, and number of days.",
            ),
            Tool(
                name="check_shipping_capacity",
                func=self.check_shipping_capacity_tool,
                description="Checks if a specified quantity of items can be shipped within the given time frame, based on inventory and SLA.",
            ),
            Tool(
                name="get_pending_sla_check_tool",
                func=self.get_pending_sla_check_tool,
                description="Checks for orders that are pending SLA checks (status 'Received').",
                return_direct=True
            ),
            Tool(
                name="common_sla_violations",
                func=self.common_sla_violations_tool,
                description="Lists common SLA violations.",
                return_direct=True
        ),
            ]
    def common_sla_violations_tool(self,question:str) -> str:
        """
        Returns a list of common SLA violation reasons.
        """
        common_violations = [
            "Insufficient inventory levels",
            "Shipping delays due to weather conditions",
            "Inaccurate order fulfillment",
            "Late payment processing",
            "Inadequate communication with customers",
            "Order cancellations due to stock unavailability",
            "Returns due to damaged or defective products",
            "Delays in order processing and fulfillment",
            "Inability to meet peak demand periods"
        ]
        return self.safe_json({"data": common_violations})
    def extract_quantity_and_days_tool(self, question: str) -> dict:
        """
        Extracts the quantity and time frame from a question.
        Example input: "Can I ship 50 items of listing c91d6409f3862e68f6a4a71c3e0d6ec9 in the next 10 days?"
        """
        # Regular expression to match quantity and time frame
        match = re.search(r"ship\s?(\d+)\s?items.*listing\s?([a-zA-Z0-9\-]+).*next\s?(\d+)\s?days", question)
        if match:
            quantity = int(match.group(1))  # Extract quantity
            listing_id = match.group(2)     # Extract listing ID
            days = int(match.group(3))      # Extract number of days
            return {"data": {"quantity": quantity, "listing_id": listing_id, "days": days}}
        return {"data": "Unable to extract required information."}

    def check_shipping_capacity_tool(self, extracted_data: dict) -> dict:
        """
        Checks if the specified quantity of items can be shipped within the given time frame.
        The `extracted_data` is expected to contain quantity, listing ID, and days.
        """
        # Extract the data from the passed dictionary
        quantity = extracted_data.get("quantity")
        listing_id = extracted_data.get("listing_id")
        days = extracted_data.get("days")

        # Check inventory for the listing ID
        inventory_response = self.check_inventory_tool(listing_id)
        available_inventory = inventory_response.get("data", {}).get("available_quantity", 0)

        # Check SLA for delivery within the given days
        sla_response = self.check_order_sla_tool(listing_id, days)
        sla_status = sla_response.get("data", {}).get("sla_met", False)

        # Evaluate whether shipping is possible
        if available_inventory >= quantity and sla_status:
            return {"data": f"Yes, you can ship {quantity} items of listing {listing_id} in the next {days} days."}
        else:
            if available_inventory < quantity:
                return {"data": f"Insufficient inventory for listing {listing_id}. Only {available_inventory} items available."}
            elif not sla_status:
                return {"data": f"Cannot meet the SLA for shipping {quantity} items of listing {listing_id} in the next {days} days."}
            else:
                return {"data": "Unknown error checking shipping capacity."}
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

    def get_pending_sla_check_tool(self,input=None) -> str:
        try:
            # Fetch the list of orders pending SLA check
            pending_sla_orders = get_orders_pending_sla_check()
            
            if not pending_sla_orders:
                return self.safe_json({"message": "No orders are pending SLA checks."})
            
            # Format the response as needed (You can include any specific formatting or additional info)
            return self.safe_json({
                "message": f"You have {len(pending_sla_orders)} order(s) pending SLA check.",
                "orders": pending_sla_orders  # Include the list of orders
            })
        
        except Exception as e:
            self.log_error("get_pending_sla_check_tool", str(e))
            return self.safe_json({"error": "Failed to fetch pending SLA orders."})

    def extract_listing_id_tool(self, question: str) -> str:
        """
        Extract the listing ID from the question.
        Assumes the listing ID is in a format like "listing ID <id>" or similar.
        You can adjust the regular expression based on the expected format.
        """
        # Regular expression to match a listing ID pattern (customize this based on your format)
        match = re.search(r"listing\s?ID\s?([a-zA-Z0-9\-]+)", question)
        if match:
            return match.group(1)
        return ""

    def extract_order_id_tool(self, question: str) -> str:
        """
        Extract the order ID from the question.
        Assumes the order ID is in a format like "order ID <id>" or similar.
        You can adjust the regular expression based on the expected format.
        """
        # Regular expression to match an order ID pattern (customize this based on your format)
        match = re.search(r"order\s?ID\s?([a-zA-Z0-9\-]+)", question)
        if match:
            return match.group(1)
        return ""
    

    def ask_question(self, question: str) -> dict:
        """
        Pass a natural language question to the LangChain agent, ensuring token limits.
        The response will be returned in a dictionary with 'text', 'data', and 'category' fields. 
        Populate the 'data' and 'category' fields only if needed. 
        The 'text' field will contain the final answer in human-readable format. This alone should be sufficient to answer the question.
        The 'data' field will contain any relevant list or structured data based on the query context.
        """

        try:
            # Ensure the input does not exceed the maximum token limit
            # input_tokens = self.count_tokens(question)
            # max_tokens_for_question = self.model_max_tokens - 500  # Reserve tokens for system prompts/context

            # if input_tokens > max_tokens_for_question:
            #     print(f"Input exceeds max token limit. Truncating to {max_tokens_for_question} tokens.")
            #     question = self.truncate_text(question, max_tokens_for_question)

            # Reinitialize ChatTogether for each query to ensure no memory of previous conversation
            self.chat = ChatTogether()  # Assuming this initializes the necessary components for the assistant

            # Initialize tools for the agent
            tools = self.initialize_tools()

            # Initialize the agent with the tools and the ChatTogether model
            self.agent = initialize_agent(tools, self.chat, agent_type="zero-shot-react-description", verbose=True)

            # Run the question through the agent
            response = self.agent.run(question)
           
            prompt = "Please rewrite the following data in a human-readable way. I am giving you the question and the final answer I got from LLM. Remove any list or dictionaries here and just give me one line text. Extract the message field and remove the data field from here .Just give final clear answer. Don't add any message like Here is the summary or sometihng like this \n " +"question is"+question+ "\nresponse is" + response
            print("*************************")
            print(prompt)
            print("*************************")
            agent2= ChatTogether(model="meta-llama/Llama-3-70b-chat-hf")
            human_readable_format=agent2.invoke(prompt)
            print(human_readable_format.content)
            # Initialize variables for the response text and data
            response_text = ""
            data = []

            if isinstance(response, str):
                # Handle string responses (simple text response)
                response_text = response
                return {
                    "text": response_text,
                    "data": [],
                    "category": "Success",
                    "answer":human_readable_format.content
                }

            elif isinstance(response, dict):
                # Handle dictionary responses where you may need to extract specific fields
                response_text = response.get('text', 'No text provided')
                data = response.get('data', [])
                category = response.get('category', 'Success')

                # Ensure we return a well-formed response
                return {
                    "text": response_text,
                    "data": data,
                    "category": category
                }

            else:
                # Handle unexpected response types (e.g., lists, other formats)
                return {
                    "text": "Sorry, I couldn't understand your question.",
                    "data": [],
                    "category": "Error"
                }

        except Exception as e:
            # Log error if something goes wrong
            self.log_error("ask_question", str(e))

            # Return an error response if an exception occurs
            return {
                "text": "An error occurred while processing your question. Please try again later.",
                "data": [],
                "category": "Error"
            }


