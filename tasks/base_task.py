from abc import ABC, abstractmethod
from typing import List
from core.llm_services import LLMService

class BaseTask(ABC):
    """
    An abstract base class that defines the structure for all task strategies.
    This acts as a contract, ensuring any new task we create will have the
    necessary methods and properties to work with our system.
    """
    def __init__(self, llm_service: LLMService):
        """
        Initializes the task with a reference to the LLM communication service.
        """
        self.llm_service = llm_service

    @abstractmethod
    def execute(self, text_chunks: List[str], task_instruction: str) -> str:
        """
        The main method that every task must implement. This is where the
        core logic of the task (e.g., summarizing, rewriting) will go.

        Args:
            text_chunks: A list of text chunks from the document.
            task_instruction: The user's specific instruction for the task.

        Returns:
            A single string containing the final processed result.
        """
        pass
