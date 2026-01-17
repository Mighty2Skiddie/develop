from typing import List
from .base_task import BaseTask

class RewriteTask(BaseTask):
    """
    A task strategy for rewriting or refining a document chunk by chunk.
    This is suitable for "local" tasks where context from the entire
    document is not needed for each step (e.g., translation, tone change).
    """
    def execute(self, text_chunks: List[str], task_instruction: str) -> str:
        print(f"[INFO] ==> Step 3: 'Rewrite' task detected. Executing Map strategy.")
        
        rewritten_chunks = []
        total_chunks = len(text_chunks)

        prompt_template = (
            "You are an expert editor. Your overall goal for the entire document is to '{task}'.\n\n"
            "Now, apply this goal to the following specific text chunk. Preserve the original meaning but modify the style, tone, or wording as requested. "
            "Output ONLY the rewritten text for this chunk.\n\n"
            "TEXT CHUNK:\n---\n{chunk}\n---"
        )

        for i, chunk in enumerate(text_chunks):
            print(f"[INFO]     - [Map] Processing chunk {i + 1} of {total_chunks}...")
            
            prompt = prompt_template.format(task=task_instruction, chunk=chunk)
            rewritten_chunk = self.llm_service.invoke_llm(prompt)
            rewritten_chunks.append(rewritten_chunk)

        # Join all the rewritten chunks to form the final document, separated by double newlines
        return "\n\n".join(rewritten_chunks)
