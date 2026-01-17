from typing import List
from .base_task import BaseTask

class SummarizeTask(BaseTask):
    """
    A task strategy for summarizing a large document using a Map-Reduce approach.
    This is essential for "global" tasks that require a holistic understanding
    of the entire document.
    """
    def execute(self, text_chunks: List[str], task_instruction: str) -> str:
        print(f"[INFO] ==> Step 3: 'Summarize' task detected. Executing Map-Reduce strategy.")
        
        # --- MAP PHASE ---
        # In this phase, we get an initial summary for each chunk of the document.
        initial_summaries = []
        total_chunks = len(text_chunks)
        map_prompt_template = (
            "You are part of a multi-step document processing pipeline. Your current task is to summarize the following text chunk.\n\n"
            "Create a concise and accurate summary of the key points and information contained in this text. This summary will be combined with others to generate a final summary of a much larger document.\n\n"
            "TEXT CHUNK:\n---\n{chunk}\n---"
        )

        for i, chunk in enumerate(text_chunks):
            print(f"[INFO]     - [Map] Processing chunk {i + 1} of {total_chunks}...")
            
            prompt = map_prompt_template.format(chunk=chunk)
            summary = self.llm_service.invoke_llm(prompt)
            initial_summaries.append(summary)

        # --- REDUCE PHASE ---
        # In this phase, we combine the initial summaries and create a final, cohesive summary.
        print("[INFO]     - [Reduce] Combining intermediate summaries for final processing...")
        combined_summaries = "\n\n".join(initial_summaries)
        
        reduce_prompt_template = (
            "You are an expert analyst. Your task is to fulfill the user's final request: '{task}'.\n\n"
            "The following text is a collection of summaries from different parts of a very large document. "
            "Your job is to synthesize these summaries into a single, final, and coherent output that accurately reflects the entire document and satisfies the user's request.\n\n"
            "COMBINED SUMMARIES:\n---\n{summaries}\n---"
        )
        
        final_prompt = reduce_prompt_template.format(task=task_instruction, summaries=combined_summaries)
        final_summary = self.llm_service.invoke_llm(final_prompt)
        
        return final_summary
