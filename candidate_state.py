required_fields = [
    "name", "email", "phone", "experience",
    "desired_position", "location", "tech_stack"
]

def init_candidate_info():
    info = {field: None for field in required_fields}
    info["responses"] = []
    info["proficiency_summary"] = None
    return info
