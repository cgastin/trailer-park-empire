extends Node2D

signal lot_clicked(grid_pos: Vector2i)

@export var grid_cols: int = 10
@export var grid_rows: int = 8
@export var cell_size: int = 64

const CONFIG_PATH := "res://data/grid_config.json"

const GRID_COLOR         := Color(1.0, 1.0, 1.0, 0.25)
const CELL_BG_COLOR      := Color(0.0, 0.0, 0.0, 0.08)
const TRAILER_BODY_COLOR := Color(0.95, 0.90, 0.78, 1.0)
const TRAILER_TRIM_COLOR := Color(0.40, 0.35, 0.25, 1.0)
const WINDOW_COLOR       := Color(0.55, 0.78, 0.92, 1.0)

func _ready() -> void:
	_load_config()

func _load_config() -> void:
	if not FileAccess.file_exists(CONFIG_PATH):
		return
	var file := FileAccess.open(CONFIG_PATH, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) == OK:
		var cfg: Dictionary = json.get_data()
		if cfg.has("grid_cols"):
			grid_cols = cfg["grid_cols"]
		if cfg.has("grid_rows"):
			grid_rows = cfg["grid_rows"]
		if cfg.has("cell_size"):
			cell_size = cfg["cell_size"]

func world_to_grid(world_pos: Vector2) -> Vector2i:
	return Vector2i(
		int(world_pos.x) / cell_size,
		int(world_pos.y) / cell_size
	)

func is_occupied(grid_pos: Vector2i) -> bool:
	return GameState.lots.has(grid_pos)

func _draw() -> void:
	_draw_cell_backgrounds()
	_draw_grid_lines()
	_draw_placed_trailers()

func _draw_cell_backgrounds() -> void:
	for col in range(grid_cols):
		for row in range(grid_rows):
			var rect := Rect2(col * cell_size + 1, row * cell_size + 1, cell_size - 2, cell_size - 2)
			draw_rect(rect, CELL_BG_COLOR)

func _draw_grid_lines() -> void:
	for col in range(grid_cols + 1):
		var x := col * cell_size
		draw_line(Vector2(x, 0), Vector2(x, grid_rows * cell_size), GRID_COLOR, 1.0)
	for row in range(grid_rows + 1):
		var y := row * cell_size
		draw_line(Vector2(0, y), Vector2(grid_cols * cell_size, y), GRID_COLOR, 1.0)

func _draw_placed_trailers() -> void:
	for grid_pos in GameState.lots:
		_draw_trailer(grid_pos)

func _draw_trailer(grid_pos: Vector2i) -> void:
	var x := float(grid_pos.x * cell_size)
	var y := float(grid_pos.y * cell_size)
	var pad := 5.0
	var body_size := float(cell_size) - pad * 2.0

	# Trailer body
	var body := Rect2(x + pad, y + pad, body_size, body_size)
	draw_rect(body, TRAILER_BODY_COLOR)
	draw_rect(body, TRAILER_TRIM_COLOR, false, 2.0)

	# Two small windows near the top of the cell
	var win_size := 10.0
	var win_y := y + pad + 8.0
	draw_rect(Rect2(x + pad + 7.0, win_y, win_size, win_size), WINDOW_COLOR)
	draw_rect(Rect2(x + float(cell_size) - pad - 7.0 - win_size, win_y, win_size, win_size), WINDOW_COLOR)

func _input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var local_pos := get_local_mouse_position()
		var grid_pos := world_to_grid(local_pos)
		if grid_pos.x >= 0 and grid_pos.x < grid_cols and grid_pos.y >= 0 and grid_pos.y < grid_rows:
			lot_clicked.emit(grid_pos)
