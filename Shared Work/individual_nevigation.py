def individual_nevigation(stops:list[int], floors_assigned:int, current_floor:int) -> list[list]:
    # only take on floors_assigned when the elevator is empty
    # OR the elevator will pass the floor and heading the same direction
    stops = sorted(stops)
    if not stops and (floors_assigned > (current_floor & floors_assigned) or floors_assigned < (current_floor & floors_assigned)):
        print(f"the elevator cannnot accept the floor: {floors_assigned}")
    else:
        stops.append(floors_assigned)
        stops = sorted(stops)
        if current_floor < stops[0]:
            pass
        else:
            stops.reverse()
    return stops