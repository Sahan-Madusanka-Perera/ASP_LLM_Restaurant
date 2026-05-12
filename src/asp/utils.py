from typing import List, Dict, Any
import clingo

def parse_model(model: clingo.Model) -> List[Dict[str, Any]]:
    """
    Parses a Clingo model into a list of dictionaries.
    Example: order(pizza) -> {"name": "order", "args": ["pizza"]}
    """
    parsed_atoms = []
    for symbol in model.symbols(shown=True):
        atom_dict = {
            "name": symbol.name,
            "args": [str(arg) for arg in symbol.arguments]
        }
        parsed_atoms.append(atom_dict)
    return parsed_atoms

def format_atoms_as_text(parsed_atoms: List[Dict[str, Any]]) -> str:
    """
    Converts parsed atoms back to a readable string for the LLM.
    """
    lines = []
    for atom in parsed_atoms:
        args_str = ", ".join(atom["args"])
        if args_str:
            lines.append(f"{atom['name']}({args_str}).")
        else:
            lines.append(f"{atom['name']}.")
    return "\n".join(lines)
