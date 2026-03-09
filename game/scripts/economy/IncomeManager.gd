extends Node

## Ticks income every TICK_INTERVAL seconds.
## income_per_tick is an array indexed by level-1: [level1_rate, level2_rate, ...]
## Calls GameState.add_currency() — no direct UI coupling.

const TRAILERS_CONFIG := "res://data/trailers.json"
const TICK_INTERVAL    := 5.0

var _income_per_tick: Dictionary = {}  # type -> Array of income per level

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
				_income_per_tick[type] = cfg[type]["income_per_tick"]

func _on_tick() -> void:
	var total := 0
	for grid_pos in GameState.lots:
		var lot: Dictionary = GameState.get_lot(grid_pos)
		var type: String = lot.get("type", "")
		var level: int = lot.get("level", 1)
		var rates: Array = _income_per_tick.get(type, [])
		if rates.size() > 0:
			var idx: int = clampi(level - 1, 0, rates.size() - 1)
			total += int(rates[idx])
	if total > 0:
		GameState.add_currency(total)
