extends Node

## Ticks income every TICK_INTERVAL seconds.
## Reads income_per_tick per trailer type from data/trailers.json.
## Calls GameState.add_currency() — no direct UI coupling.

const TRAILERS_CONFIG := "res://data/trailers.json"
const TICK_INTERVAL    := 5.0

var _income_per_tick: Dictionary = {}  # type (String) -> coins per tick (int)

func _ready() -> void:
	_load_config()
	var timer := Timer.new()
	timer.wait_time = TICK_INTERVAL
	timer.autostart = true
	timer.timeout.connect(_on_tick)
	add_child(timer)

func _load_config() -> void:
	if not FileAccess.file_exists(TRAILERS_CONFIG):
		return
	var file := FileAccess.open(TRAILERS_CONFIG, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) == OK:
		var cfg: Dictionary = json.get_data()
		for type in cfg:
			if cfg[type].has("income_per_tick"):
				_income_per_tick[type] = int(cfg[type]["income_per_tick"])

func _on_tick() -> void:
	var total := 0
	for grid_pos in GameState.lots:
		var lot: Dictionary = GameState.get_lot(grid_pos)
		total += _income_per_tick.get(lot.get("type", ""), 0)
	if total > 0:
		GameState.add_currency(total)
