class_name TrailerPlacer
extends Node

signal trailer_placed(grid_pos: Vector2i)
signal placement_failed(grid_pos: Vector2i)

func place_trailer(grid_pos: Vector2i) -> bool:
	var lot_grid: Node2D = get_parent().get_node("LotGrid")
	if not _is_in_bounds(grid_pos, lot_grid):
		return false
	if GameState.is_lot_occupied(grid_pos):
		placement_failed.emit(grid_pos)
		return false

	GameState.place_trailer(grid_pos)
	trailer_placed.emit(grid_pos)
	return true

func _is_in_bounds(grid_pos: Vector2i, lot_grid: Node2D) -> bool:
	return (
		grid_pos.x >= 0 and grid_pos.x < lot_grid.grid_cols and
		grid_pos.y >= 0 and grid_pos.y < lot_grid.grid_rows
	)
