def resting_floor(num_floors:int, stopping_plan:dict, elevator_data:list) -> dict:
    elevators = len(elevator_data)
    spacing = num_floors/elevators
    print(spacing)
    for i, key in enumerate(stopping_plan):
        stopping_plan[key]["resting_floor"] = int((i+0.5)*spacing)
    return stopping_plan

test_data = resting_floor(10,
              {
                  "1":{"stops":[3, 5], "resting_floor":0}, 
                  "2":{"stops":[3, 5], "resting_floor":0}, 
                  "3":{"stops":[3, 5], "resting_floor":0}, 

              },
              [{"buttons_pressed": [2, 3], "floor": 1, "id": "elevator-0"},
               {"buttons_pressed": [], "floor": 6, "id": "elevator-1"},
               {"buttons_pressed": [], "floor": 6, "id": "elevator-2"}]
               )
print(test_data)