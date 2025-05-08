import json


# Correct JSON string (escaped properly)
json_string = "{\"tests\": \"assert(factorial(3) == 6);\\nassert(factorial(4) == 120);\\nassert(factorial(0) == 1);\\nassert(factorial(-1) == 0);\"}"

# Load it with json.loads()
data = json.loads(json_string)

# Print the result
print(json.dumps(data, indent=4))