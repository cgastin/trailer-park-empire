extends Node2D

signal lot_clicked(grid_pos: Vector2i)

@export var grid_cols: int = 10
@export var grid_rows: int = 8
@export var cell_size: int = 64

const CONFIG_PATH := "res://data/grid_config.json"

const GRID_COLOR           := Color(0.2, 0.15, 0.08, 0.4)
const HOVER_COLOR          := Color(1.0, 1.0, 1.0, 0.30)
const UPGRADE_HOVER_COLOR  := Color(1.0, 0.85, 0.0, 0.35)
const INVALID_COLOR        := Color(1.0, 0.2, 0.2, 0.50)
const LOCKED_OVERLAY_COLOR := Color(0.0, 0.0, 0.0, 0.55)

const NO_LOT          := Vector2i(-1, -1)
const TRAILERS_CONFIG := "res://data/trailers.json"

var _hovered_lot: Vector2i = NO_LOT
var _flash_lot:   Vector2i = NO_LOT
var _max_upgrade_level: int = 2
var _unlock_manager: Node = null

var _tex_lot_empty:  Texture2D = null
var _tex_trailer_l1: Texture2D = null
var _tex_trailer_l2: Texture2D = null
var _tex_lock:       Texture2D = null


func set_unlock_manager(mgr: Node) -> void:
	_unlock_manager = mgr


func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_load_config()
	_load_trailers_config()
	_load_textures()


func _load_textures() -> void:
	_tex_lot_empty  = load("res://assets/sprites/lot_empty.png")
	_tex_trailer_l1 = load("res://assets/sprites/trailer_l1.png")
	_tex_trailer_l2 = load("res://assets/sprites/trailer_l2.png")
	_tex_lock       = load("res://assets/sprites/icon_lock.png")


func _load_trailers_config() -> void:
	if not FileAccess.file_exists(TRAILERS_CONFIG):
		return
	var file := FileAccess.open(TRAILERS_CONFIG, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) == OK:
		var cfg: Dictionary = json.get_data()
		if cfg.has("trailer") and cfg["trailer"].has("max_level"):
			_max_upgrade_level = int(cfg["trailer"]["max_level"])


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
	return GameState.is_lot_occupied(grid_pos)


# Called by Main when a placement attempt fails. Flashes the lot red briefly.
func flash_invalid(grid_pos: Vector2i) -> void:
	_flash_lot = grid_pos
	queue_redraw()
	get_tree().create_timer(0.3).timeout.connect(_clear_flash)


func _clear_flash() -> void:
	_flash_lot = NO_LOT
	queue_redraw()


# --- Draw --------------------------------------------------------------------

func _draw() -> void:
	_draw_cell_backgrounds()
	_draw_grid_lines()
	_draw_placed_trailers()
	_draw_locked_overlays()
	_draw_hover()
	_draw_flash()


func _draw_cell_backgrounds() -> void:
	for col in range(grid_cols):
		for row in range(grid_rows):
			var rect := Rect2(col * cell_size, row * cell_size, cell_size, cell_size)
			if _tex_lot_empty:
				draw_texture_rect(_tex_lot_empty, rect, false)
			else:
				draw_rect(rect, Color(0.6, 0.5, 0.35, 1.0))


func _draw_grid_lines() -> void:
	for col in range(grid_cols + 1):
		var x := col * cell_size
		draw_line(Vector2(x, 0), Vector2(x, grid_rows * cell_size), GRID_COLOR, 1.0)
	for row in range(grid_rows + 1):
		var y := row * cell_size
		draw_line(Vector2(0, y), Vector2(grid_cols * cell_size, y), GRID_COLOR, 1.0)


func _draw_locked_overlays() -> void:
	if _unlock_manager == null:
		return
	for col in range(grid_cols):
		for row in range(grid_rows):
			var gp := Vector2i(col, row)
			if not _unlock_manager.is_lot_unlocked(gp):
				draw_rect(_cell_rect(gp), LOCKED_OVERLAY_COLOR)
				if _tex_lock:
					var lock_size := 24.0
					var cx := float(col * cell_size) + (cell_size - lock_size) / 2.0
					var cy := float(row * cell_size) + (cell_size - lock_size) / 2.0
					draw_texture_rect(_tex_lock, Rect2(cx, cy, lock_size, lock_size), false)


func _draw_hover() -> void:
	if _hovered_lot == NO_LOT:
		return
	var rect := _cell_rect(_hovered_lot)
	if _unlock_manager != null and not _unlock_manager.is_lot_unlocked(_hovered_lot):
		return  # no hover on locked lots
	if GameState.is_lot_occupied(_hovered_lot):
		var lot := GameState.get_lot(_hovered_lot)
		if lot.get("level", 1) < _max_upgrade_level:
			draw_rect(rect, UPGRADE_HOVER_COLOR)  # upgradeable
		# maxed lots: no hover
	else:
		draw_rect(rect, HOVER_COLOR)


func _draw_placed_trailers() -> void:
	for grid_pos in GameState.lots:
		_draw_trailer(grid_pos)


func _draw_trailer(grid_pos: Vector2i) -> void:
	var lot := GameState.get_lot(grid_pos)
	var level: int = lot.get("level", 1)

	var pad := 5.0
	var x := float(grid_pos.x * cell_size) + pad
	var y := float(grid_pos.y * cell_size) + pad
	var size := float(cell_size) - pad * 2.0

	var tex := _tex_trailer_l2 if level >= 2 else _tex_trailer_l1
	if tex:
		draw_texture_rect(tex, Rect2(x, y, size, size), false)


func _draw_flash() -> void:
	if _flash_lot == NO_LOT:
		return
	draw_rect(_cell_rect(_flash_lot), INVALID_COLOR)


# --- Input -------------------------------------------------------------------

func _input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		_update_hover()
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var grid_pos := world_to_grid(get_local_mouse_position())
		if _is_in_grid(grid_pos):
			lot_clicked.emit(grid_pos)


func _update_hover() -> void:
	var grid_pos := world_to_grid(get_local_mouse_position())
	var new_hover := grid_pos if _is_in_grid(grid_pos) else NO_LOT
	if new_hover != _hovered_lot:
		_hovered_lot = new_hover
		queue_redraw()


# --- Helpers -----------------------------------------------------------------

func _cell_rect(grid_pos: Vector2i) -> Rect2:
	return Rect2(
		grid_pos.x * cell_size + 1,
		grid_pos.y * cell_size + 1,
		cell_size - 2,
		cell_size - 2
	)


func _is_in_grid(grid_pos: Vector2i) -> bool:
	return (
		grid_pos.x >= 0 and grid_pos.x < grid_cols and
		grid_pos.y >= 0 and grid_pos.y < grid_rows
	)
