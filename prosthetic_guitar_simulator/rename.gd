@tool
extends Node

# Prefix to remove from child nodes
const PREFIX = "Target_"

# Function to rename children
func rename_children():
	# Iterate through all children of the parent node
	for child in get_children():
		# Check if the child's name starts with the PREFIX
		if child.name.begins_with(PREFIX):
			# Remove the prefix by setting the name to exclude the first part
			var new_name = child.name.substr(PREFIX.length(), child.name.length() - PREFIX.length())
			child.name = new_name
			print("Renamed ", child.name, " to ", new_name)

# Run the rename function in the editor only
func _ready():
	if Engine.is_editor_hint():
		rename_children()
