class_name TrailerPlacer
extends Node

signal trailer_placed(grid_pos: Vector2i)
signal placement_failed(grid_pos: Vector2i)
signal insufficient_funds(grid_pos: Vector2i)

const TRAILERS_CONFIG := "res://data/trailers.json"

var _trailer_cost: int = 100

func _ready() -> void:
	_load_config()

func _load_config() -> void:
	if not FileAccess.file_exists(TRAILERS_CONFIG):
		return
	var file := FileAccess.open(TRAILERS_CONFIG, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) == OK:
		var cfg: Dictionary = json.get_data()
		if cfg.has("trailer") and cfg["trailer"].has("cost"):
			_trailer_cost = int(cfg["trailer"]["cost"])

func place_trailer(grid_pos: Vector2i) -> bool:
	var lot_grid: Node2D = get_parent().get_node("LotGrid")
	if not _is_in_bounds(grid_pos, lot_grid):
		return false
	if GameState.is_lot_occupied(grid_pos):
		placement_failed.emit(grid_pos)
		return false
	if not GameState.deduct_currency(_trailer_cost):
		insufficient_funds.emit(grid_pos)
		return false

	GameState.place_trailer(grid_pos)
	trailer_placed.emit(grid_pos)
	return true

func _is_in_bounds(grid_pos: Vector2i, lot_grid: Node2D) -> bool:
	return (
		grid_pos.x >= 0 and grid_pos.x < lot_grid.grid_cols and
		grid_pos.y >= 0 and grid_pos.y < lot_grid.grid_rows
	)
