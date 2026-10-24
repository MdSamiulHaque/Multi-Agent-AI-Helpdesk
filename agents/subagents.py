from langchain_openai import ChatOpenAI
from deepagents import create_deep_agent
from tools.order_tools import get_order_status, cancel_order, process_refund
from tools.policy_tools import check_refund_eligibility
from tools.rag_tools import retrieve_manual_info

class SubagentFactory:
    def __init__(self, model_name: str = "gpt-5.4-mini"):
        self.model = ChatOpenAI(model=model_name, temperature=0)

    def build_order_operations_agent(self):
        return create_deep_agent(
            model=self.model,
            tools=[
                get_order_status, 
                cancel_order, 
                process_refund, 
                check_refund_eligibility
            ],
            system_prompt="You are an order operations subagent. You manage refunds and cancellations. You must execute check_refund_eligibility before executing cancel_order or process_refund. Escalate to human if eligibility fails."
        )

    def build_product_specialist_agent(self):
        return create_deep_agent(
            model=self.model,
            tools=[retrieve_manual_info],
            system_prompt="You are a product specialist subagent. You provide product troubleshooting and usage instructions. You must use retrieve_manual_info to extract context from product manuals. Answer strictly using the retrieved text."
        )

    def build_general_support_agent(self):
        return create_deep_agent(
            model=self.model,
            tools=[], 
            system_prompt="You are a general support subagent. You assist with account FAQs, general navigation, and offer a 10% discount code for generic customer dissatisfaction."
        )