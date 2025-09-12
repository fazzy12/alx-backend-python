#!/usr/bin/python3
from itertools import islice
import importlib.util

# Dynamically import the module since its name starts with a number
spec = importlib.util.spec_from_file_location("stream_users_module", "0-stream_users.py")
stream_users_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stream_users_module)

# Get the function from the imported module
stream_users = stream_users_module.stream_users

# iterate over the generator function and print only the first 6 rows
for user in islice(stream_users(), 100):
    print(user)