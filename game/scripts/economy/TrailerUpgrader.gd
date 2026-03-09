class_name TrailerUpgrader
extends Node

signal trailer_upgraded(grid_pos: Vector2i)
signal upgrade_maxed(grid_pos: Vector2i)
signal insufficient_funds(grid_pos: Vector2i)

const TRAILERS_CONFIG := "res://data/trailers.json"

var _upgrade_cost: int = 150
var _max_level: int = 2

func _ready() -> void:
	_load_config()

func _load_config() -> void:
	if not FileAccess.file_exists(TRAILERS_CONFIG):
		return
	var file := FileAccess.open(TRAILERS_CONFIG, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) == OK:
		var cfg: Dictionary = json.get_data()
		if cfg.has("trailer"):
			if cfg["trailer"].has("upgrade_cost"):
				_upgrade_cost = int(cfg["trailer"]["upgrade_cost"])
			if cfg["trailer"].has("max_level"):
				_max_level = int(cfg["trailer"]["max_level"])

func upgrade_trailer(grid_pos: Vector2i) -> bool:
	var lot: Dictionary = GameState.get_lot(grid_pos)
	if lot.is_empty():
		return false
	if lot.get("level", 1) >= _max_level:
		upgrade_maxed.emit(grid_pos)
		return false
	if not GameState.deduct_currency(_upgrade_cost):
		insufficient_funds.emit(grid_pos)
		return false

	GameState.upgrade_trailer(grid_pos)
	trailer_upgraded.emit(grid_pos)
	return true
