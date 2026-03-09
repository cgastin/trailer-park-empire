extends Node

## Manages a linear sequence of quests loaded from data/quests.json.
## Tracks per-condition counters and emits signals when quests complete or activate.
## Never touches UI — all display goes through Main.gd via signals.

signal quest_completed(quest: Dictionary)
signal quest_activated(quest: Dictionary)

const QUESTS_CONFIG := "res://data/quests.json"

var _quests: Array = []
var _active_quest_index: int = 0
var _trailers_placed: int = 0
var _trailers_upgraded: int = 0
var _income_earned: int = 0

func _ready() -> void:
	_load_config()

func _load_config() -> void:
	if not FileAccess.file_exists(QUESTS_CONFIG):
		return
	var file := FileAccess.open(QUESTS_CONFIG, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) == OK:
		_quests = json.get_data()

func get_active_quest() -> Dictionary:
	if _active_quest_index >= _quests.size():
		return {}
	return _quests[_active_quest_index]

func notify_trailer_placed() -> void:
	_trailers_placed += 1
	_check_active_quest()

func notify_trailer_upgraded() -> void:
	_trailers_upgraded += 1
	_check_active_quest()

func notify_income_earned(amount: int) -> void:
	_income_earned += amount
	_check_active_quest()

func _check_active_quest() -> void:
	var quest := get_active_quest()
	if quest.is_empty():
		return
	var condition: String = quest.get("condition", "")
	var threshold: int = int(quest.get("threshold", 0))
	var counter: int = _get_counter(condition)
	if counter >= threshold:
		quest_completed.emit(quest)
		_active_quest_index += 1
		var next := get_active_quest()
		quest_activated.emit(next)

func _get_counter(condition: String) -> int:
	match condition:
		"trailers_placed":
			return _trailers_placed
		"trailers_upgraded":
			return _trailers_upgraded
		"income_earned":
			return _income_earned
	return 0

# --- Save / Load -------------------------------------------------------------

func get_save_data() -> Dictionary:
	return {
		"active_quest_index": _active_quest_index,
		"trailers_placed": _trailers_placed,
		"trailers_upgraded": _trailers_upgraded,
		"income_earned": _income_earned,
	}

func load_save_data(data: Dictionary) -> void:
	_active_quest_index = int(data.get("active_quest_index", 0))
	_trailers_placed    = int(data.get("trailers_placed", 0))
	_trailers_upgraded  = int(data.get("trailers_upgraded", 0))
	_income_earned      = int(data.get("income_earned", 0))
