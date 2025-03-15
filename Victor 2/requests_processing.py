def requests_processing(requests, elevator_data):
    # classifing elevators into: free, up, down
    free_elevators = []
    up_elevators = []
    down_elevators = []
    
    for elevator in elevator_data:
        if not elevator["buttons_pressed"]:
            free_elevators.append(elevator)
        elif elevator["direction"] == UP:
            up_elevators.append(elevator)
        elif elevator["direction"] == DOWN:
            down_elevators.append(elevator)
    
    # Assigning elevator

    for request in requests:
        # calculating the distance between the request and the elevators and check for direction
        request_elevators = {}
        for elevator in free_elevators:
            dist = abs(request["floor"] - elevator["floor"])  # Use abs() for absolute distance
            request_elevators[elevator["id"]] = {"distance": dist, "direction": None}
        for elevator in up_elevators:
            dist = abs(request["floor"] - elevator["floor"])
            request_elevators[elevator["id"]] = {"distance": dist, "direction": UP}
        for elevator in down_elevators:
            dist = abs(request["floor"] - elevator["floor"])
            request_elevators[elevator["id"]] = {"distance": dist, "direction": DOWN}

        # Sort elevators by distance
        sorted_elevators = dict(sorted(distances.items(), 
                                     key=lambda x: x[1]["distance"]))
        
        print(f"DEBUG: Sorted elevators by distance: {sorted_elevators}")

# Testing
UP, DOWN = True, False
test_requests = [
    {"floor": 5, "direction": UP},
    {"floor": 2, "direction": UP},
    {"floor": 7, "direction": DOWN},
]

test_elevators = [
    {"id": 1, "floor": 3, "direction": UP, "buttons_pressed": []},
    {"id": 2, "floor": 6, "direction": DOWN, "buttons_pressed": [4, 8]},
    {"id": 3, "floor": 4, "direction": UP, "buttons_pressed": [9]},
]

requests_processing(test_requests, test_elevators)