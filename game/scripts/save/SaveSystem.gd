extends Node

## Saves and loads GameState to/from user://save.json.
## Call save() after any state change. Call load_save() on startup.
## Emits local_save_completed(data) after every successful local write so
## Main.gd can trigger a cloud upload without SaveSystem knowing about Firebase.

const SAVE_PATH := "user://save.json"

signal local_save_completed(data: Dictionary)

var quest_manager: Node = null

func save() -> void:
	var unlock_manager: Node = get_parent().unlock_manager
	var data := {
		"currency": GameState.currency,
		"lots": _serialize_lots(),
		"full_grid_unlocked": unlock_manager.get_full_grid_unlocked() if unlock_manager else false,
		"saved_at": int(Time.get_unix_time_from_system()),
	}
	if quest_manager:
		data["quests"] = quest_manager.get_save_data()
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	file.store_string(JSON.stringify(data, "\t"))
	local_save_completed.emit(data)

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
	if data.has("full_grid_unlocked"):
		var um: Node = get_parent().unlock_manager
		if um:
			um.set_full_grid_unlocked(data["full_grid_unlocked"])
	if data.has("quests") and quest_manager:
		quest_manager.load_save_data(data["quests"])

func apply_cloud_data(data: Dictionary) -> void:
	## Applies a downloaded cloud save dictionary to GameState and saves locally.
	## Called by Main.gd when the cloud save is newer than local.
	if data.has("currency"):
		GameState.currency = int(data["currency"])
	if data.has("lots"):
		_deserialize_lots(data["lots"])
	var um: Node = get_parent().unlock_manager if get_parent() else null
	if data.has("full_grid_unlocked") and um:
		um.set_full_grid_unlocked(data["full_grid_unlocked"])
	if data.has("quests") and quest_manager:
		quest_manager.load_save_data(data["quests"])
	save()


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
