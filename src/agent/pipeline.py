from src.llm.client import LLMClient
from src.llm.prompts import SYSTEM_PARSER_PROMPT, SYSTEM_GENERATOR_PROMPT, CRITIC_PROMPT
from src.asp.solver import ASPSolver
from src.asp.utils import format_atoms_as_text

class NeuroSymbolicPipeline:
    def __init__(self):
        self.llm = LLMClient()
        self.solver = ASPSolver()

    async def process_request(self, user_text: str) -> str:
        """
        Executes the LLM -> ASP -> LLM pipeline with Solver-in-the-Loop critic (Phase 2).
        """
        # 1. Semantic Parsing: NL to ASP
        generated_asp = await self.llm.generate(SYSTEM_PARSER_PROMPT, user_text)
        print(f"[DEBUG] Parsed ASP:\n{generated_asp}\n")

        # Critic Loop (Phase 2)
        max_retries = 2
        success = False
        parsed_model = None
        error_msg = None

        for attempt in range(max_retries + 1):
            # 2. Logic Solving (System 2)
            success, parsed_model, error_msg = self.solver.solve(generated_asp)
            
            if success:
                break
                
            print(f"[DEBUG] Solver Error (Attempt {attempt + 1}): {error_msg}")
            if attempt < max_retries:
                # 3. Solver-in-the-Loop feedback
                critic_user_prompt = CRITIC_PROMPT.format(
                    original_request=user_text,
                    faulty_asp=generated_asp,
                    error_message=error_msg
                )
                generated_asp = await self.llm.generate(SYSTEM_PARSER_PROMPT, critic_user_prompt)
                print(f"[DEBUG] Critic Revised ASP:\n{generated_asp}\n")

        # 4. Natural Language Generation
        if success:
            atoms_text = format_atoms_as_text(parsed_model)
            generator_prompt = f"User Request: {user_text}\n\nASP Solution:\n{atoms_text}"
        else:
            generator_prompt = f"User Request: {user_text}\n\nASP Solver Error:\n{error_msg}"

        final_response = await self.llm.generate(SYSTEM_GENERATOR_PROMPT, generator_prompt)
        return final_response
