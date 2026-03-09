extends Node

## Saves and loads GameState to/from user://save.json.
## Call save() after any state change. Call load_save() on startup.

const SAVE_PATH := "user://save.json"

func save() -> void:
	var data := {
		"currency": GameState.currency,
		"lots": _serialize_lots(),
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	file.store_string(JSON.stringify(data, "\t"))

func load_save() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) != OK:
		return
	var data: Dictionary = json.get_data()
	if data.has("currency"):
		GameState.currency = int(data["currency"])
	if data.has("lots"):
		_deserialize_lots(data["lots"])

func _serialize_lots() -> Array:
	var result := []
	for grid_pos in GameState.lots:
		var entry: Dictionary = GameState.lots[grid_pos].duplicate()
		entry["x"] = grid_pos.x
		entry["y"] = grid_pos.y
		result.append(entry)
	return result

func _deserialize_lots(lots_data: Array) -> void:
	GameState.lots.clear()
	for entry in lots_data:
		var pos := Vector2i(int(entry["x"]), int(entry["y"]))
		var lot: Dictionary = entry.duplicate()
		lot.erase("x")
		lot.erase("y")
		GameState.lots[pos] = lot
