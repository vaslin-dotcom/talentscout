from candidate_state import candidate_info

def update_candidate_info(parsed_data):
    for key in candidate_info:
        if key in parsed_data and candidate_info[key] is None:
            candidate_info[key] = parsed_data[key]
