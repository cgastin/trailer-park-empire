extends Node

## Tracks unlock conditions and gates lot availability.
## Instantiated dynamically in Main.gd — not placed in the scene file.
##
## Initial state: only the top-left 6x4 area (cols 0-5, rows 0-3) is unlocked.
## Condition: place 3 trailers → full grid unlocks.

signal grid_unlocked

const UNLOCKS_CONFIG   := "res://data/unlocks.json"
const INITIAL_COLS     := 6
const INITIAL_ROWS     := 4

var _full_grid_unlocked: bool = false
var _threshold: int = 3

func _ready() -> void:
	_load_config()

func _load_config() -> void:
	if not FileAccess.file_exists(UNLOCKS_CONFIG):
		return
	var file := FileAccess.open(UNLOCKS_CONFIG, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) == OK:
		var cfg: Dictionary = json.get_data()
		if cfg.has("expand_grid") and cfg["expand_grid"].has("threshold"):
			_threshold = int(cfg["expand_grid"]["threshold"])

func is_lot_unlocked(grid_pos: Vector2i) -> bool:
	if _full_grid_unlocked:
		return true
	return grid_pos.x < INITIAL_COLS and grid_pos.y < INITIAL_ROWS

func check_unlocks() -> void:
	if _full_grid_unlocked:
		return
	if GameState.lots.size() >= _threshold:
		_full_grid_unlocked = true
		grid_unlocked.emit()

# --- Save / Load -------------------------------------------------------------

func get_full_grid_unlocked() -> bool:
	return _full_grid_unlocked

func set_full_grid_unlocked(value: bool) -> void:
	_full_grid_unlocked = value
