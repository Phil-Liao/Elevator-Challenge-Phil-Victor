def individual_navigation(stopping_plan:dict, elevator_id:str, floor_assigned:int, current_floor:int) -> dict:
    """
    Keyword Arguments:
    stopping_plan: "stopping_plan" of updownbot.py
    elevator_id: elevator["id"]
    floor_assigned: request["floor"]
    current_floor: elevator["floor"]
    """
    stopping_plan[elevator_id]["stops"].append(floor_assigned)
    stopping_plan[elevator_id]["stops"].sort()
    if current_floor < stopping_plan[elevator_id]["stops"][0]:
        pass
    else:
        stopping_plan[elevator_id]["stops"].reverse()
    return stopping_plan