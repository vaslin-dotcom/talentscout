required_fields = [
    "name", "email", "phone", "experience",
    "desired_position", "location", "tech_stack"
]

candidate_info = {field: None for field in required_fields}
candidate_info["responses"] = []
candidate_info["proficiency_summary"] = None
