import uuid
from langgraph.checkpoint.memory import MemorySaver
from workflow.orchestrator import OrchestratorFactory
from dotenv import load_dotenv

load_dotenv()

class TerminalColors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class TerminalApplication:
    def __init__(self, model_identifier: str = "openai:gpt-5.4-mini"):
        self.factory = OrchestratorFactory(model_identifier=model_identifier)
        self.agent = self.factory.build_workflow(checkpointer=MemorySaver())
        self.session_id = str(uuid.uuid4())
        self.execution_config = {"configurable": {"thread_id": self.session_id}}

    def execute_chat_loop(self):
        print(f"{TerminalColors.WARNING}{TerminalColors.BOLD}Session initialized. Thread ID: {self.session_id}{TerminalColors.ENDC}\n")
        
        while True:
            user_input = input(f"{TerminalColors.BLUE}{TerminalColors.BOLD}Customer: {TerminalColors.ENDC}")
            
            if user_input.lower() in ["exit", "quit"]:
                break
                
            try:
                result = self.agent.invoke(
                    {"messages": [("user", user_input)]},
                    config=self.execution_config
                )
                
                final_content = result["messages"][-1].content
                
                if isinstance(final_content, list):
                    final_response = " ".join([block["text"] for block in final_content if block.get("type") == "text"])
                else:
                    final_response = final_content
                    
                print(f"\n{TerminalColors.GREEN}{TerminalColors.BOLD}Agent:{TerminalColors.ENDC} {final_response}")
                print(f"{TerminalColors.WARNING}{'-'*60}{TerminalColors.ENDC}\n")
                
            except Exception as error:
                print(f"\n{TerminalColors.FAIL}{TerminalColors.BOLD}System Error:{TerminalColors.ENDC} {error}\n")

if __name__ == "__main__":
    app = TerminalApplication()
    app.execute_chat_loop()