
# Define the filename with .py extension
filename = "and.aag"

# Use the open function to create the file
# 'w' mode is used to create a new file or overwrite an existing one
with open(filename, 'w') as file:
    # Optionally, you can write some initial content to the file
    # List of numbers
    file.write(str(circ1.aig))

print(f"File '{filename}' created successfully.")