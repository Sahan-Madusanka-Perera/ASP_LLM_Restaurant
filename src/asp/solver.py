import os
import clingo
from typing import List, Dict, Tuple, Optional
from src.asp.utils import parse_model

PROGRAMS_DIR = os.path.join(os.path.dirname(__file__), "programs")

class ASPSolverError(Exception):
    pass

class ASPSolver:
    def __init__(self, program_files: List[str] = ["menu.lp", "constraints.lp", "ordering.lp"]):
        self.program_files = program_files

    def solve(self, user_facts: str) -> Tuple[bool, Optional[List[Dict]], Optional[str]]:
        """
        Solves the ASP program combining static knowledge base with user generated facts.
        Returns: (success_bool, parsed_model_or_none, error_message_or_none)
        """
        ctl = clingo.Control(["0"]) # 0 means compute all models
        
        # Load static files
        for file in self.program_files:
            file_path = os.path.join(PROGRAMS_DIR, file)
            if not os.path.exists(file_path):
                return False, None, f"Program file not found: {file_path}"
            ctl.load(file_path)

        # Inject user generated facts
        try:
            ctl.add("base", [], user_facts)
        except RuntimeError as e:
            return False, None, f"Syntax error in generated ASP: {str(e)}"

        # Grounding
        try:
            ctl.ground([("base", [])])
        except RuntimeError as e:
            return False, None, f"Grounding error: {str(e)}"

        models = []
        
        # Solving
        def on_model(m):
            models.append(parse_model(m))

        solve_handle = ctl.solve(on_model=on_model)
        
        # Check result
        if solve_handle.unsatisfiable:
            # Phase 2 solver-in-the-loop will use this
            return False, None, "The request violated hard constraints (UNSAT)."
            
        if not models:
            return False, None, "No models could be found."

        # If there are multiple models, it's ambiguous. 
        # For Phase 1, we just take the first one. Phase 3 tackles ambiguity.
        return True, models[0], None
