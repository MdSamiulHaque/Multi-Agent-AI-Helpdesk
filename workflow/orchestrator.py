from dotenv import load_dotenv
load_dotenv()

from deepagents import CompiledSubAgent, create_deep_agent
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from tools.auth_tool import authenticate_user_by_email_and_dob
from tools.order_tools import get_order_status, cancel_order, process_refund
from tools.policy_tools import check_refund_eligibility
from tools.rag_tools import retrieve_manual_info

class OrchestratorFactory:
    def __init__(self, model_identifier: str = "openai:gpt-5.4-mini"):
        self.model_identifier = model_identifier

    def build_workflow(self, checkpointer=None):
        order_ops_graph = create_agent(
            model=self.model_identifier,
            tools=[get_order_status, cancel_order, process_refund, check_refund_eligibility],
            system_prompt="You are an order operations subagent. You manage refunds and cancellations. You must execute check_refund_eligibility before executing cancel_order or process_refund. Escalate to human if eligibility fails."
        )

        order_ops_subagent = CompiledSubAgent(
            name="order-ops",
            description="Specialized agent for managing order status, cancellations, and refunds",
            runnable=order_ops_graph,
        )

        product_specialist_graph = create_agent(
            model=self.model_identifier,
            tools=[retrieve_manual_info],
            system_prompt="You are a product specialist subagent. You provide product troubleshooting and usage instructions. You must use retrieve_manual_info to extract context from product manuals. Answer strictly using the retrieved text."
        )

        product_specialist_subagent = CompiledSubAgent(
            name="product-specialist",
            description="Specialized agent for product troubleshooting and reading manuals",
            runnable=product_specialist_graph,
        )

        general_support_graph = create_agent(
            model=self.model_identifier,
            tools=[],
            system_prompt="You are a general support subagent. You assist with account FAQs, general navigation, and offer a 10% discount code for generic customer dissatisfaction."
        )

        general_support_subagent = CompiledSubAgent(
            name="general-support",
            description="Specialized agent for general account FAQs and discount codes",
            runnable=general_support_graph,
        )

        subagents = [order_ops_subagent, product_specialist_subagent, general_support_subagent]


        orchestrator_agent = create_deep_agent(
            model=self.model_identifier,
            tools=[authenticate_user_by_email_and_dob],
            system_prompt="You are a customer support orchestrator. Authenticate the user first before handing task to order ops subagent. Delegate tasks to the appropriate subagent based on the customer request.",
            subagents=subagents,
            checkpointer=checkpointer,
        )

        return orchestrator_agent


agent = OrchestratorFactory().build_workflow()
