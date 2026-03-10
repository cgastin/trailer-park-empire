extends Node2D

signal lot_clicked(grid_pos: Vector2i)

@export var grid_cols: int = 10
@export var grid_rows: int = 8
@export var tile_width: int = 128
@export var tile_height: int = 64
@export var origin_x: int = 640
@export var origin_y: int = 90

const CONFIG_PATH := "res://data/grid_config.json"

const GRID_COLOR           := Color(0.2, 0.15, 0.08, 0.35)
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
	texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
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
		if cfg.has("grid_cols"):   grid_cols   = cfg["grid_cols"]
		if cfg.has("grid_rows"):   grid_rows   = cfg["grid_rows"]
		if cfg.has("tile_width"):  tile_width  = cfg["tile_width"]
		if cfg.has("tile_height"): tile_height = cfg["tile_height"]
		if cfg.has("origin_x"):    origin_x    = cfg["origin_x"]
		if cfg.has("origin_y"):    origin_y    = cfg["origin_y"]


# --- Coordinate helpers -------------------------------------------------------

func grid_to_screen(col: int, row: int) -> Vector2:
	var hw := tile_width / 2   # 64
	var hh := tile_height / 2  # 32
	return Vector2(
		origin_x + (col - row) * hw,
		origin_y + (col + row) * hh
	)


func world_to_grid(world_pos: Vector2) -> Vector2i:
	var lx := world_pos.x - origin_x
	var ly := world_pos.y - origin_y
	var hw := float(tile_width) / 2.0   # 64
	var hh := float(tile_height) / 2.0  # 32
	var col := int(floor((lx / hw + ly / hh) / 2.0))
	var row := int(floor((ly / hh - lx / hw) / 2.0))
	return Vector2i(col, row)


func _is_valid_hit(world_pos: Vector2, col: int, row: int) -> bool:
	var center := grid_to_screen(col, row)
	var hw: float = float(tile_width) / 2.0
	var hh: float = float(tile_height) / 2.0
	var dx: float = abs(world_pos.x - center.x) / hw
	var dy: float = abs(world_pos.y - center.y) / hh
	return (dx + dy) <= 1.0


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


# --- Diamond shape helper -----------------------------------------------------

func _cell_diamond(col: int, row: int) -> PackedVector2Array:
	var c := grid_to_screen(col, row)
	var hw := float(tile_width) / 2.0
	var hh := float(tile_height) / 2.0
	return PackedVector2Array([
		Vector2(c.x,       c.y - hh),  # north
		Vector2(c.x + hw,  c.y),       # east
		Vector2(c.x,       c.y + hh),  # south
		Vector2(c.x - hw,  c.y),       # west
	])


# --- Draw --------------------------------------------------------------------

func _draw() -> void:
	# Painter's algorithm: back rows first so front rows render on top
	for row in range(grid_rows):
		for col in range(grid_cols):
			_draw_cell_ground(col, row)
	for row in range(grid_rows):
		for col in range(grid_cols):
			_draw_cell_contents(col, row)


func _draw_cell_ground(col: int, row: int) -> void:
	var diamond := _cell_diamond(col, row)
	if _tex_lot_empty:
		# Draw textured diamond using the tile texture fitted to the diamond bounding rect
		var c := grid_to_screen(col, row)
		var hw := float(tile_width) / 2.0
		var hh := float(tile_height) / 2.0
		draw_texture_rect(_tex_lot_empty,
			Rect2(c.x - hw, c.y - hh, tile_width, tile_height), false)
	else:
		draw_colored_polygon(diamond, Color(0.6, 0.5, 0.35, 1.0))
	# Grid outline
	draw_polyline(
		PackedVector2Array([diamond[0], diamond[1], diamond[2], diamond[3], diamond[0]]),
		GRID_COLOR, 1.0
	)


func _draw_cell_contents(col: int, row: int) -> void:
	var gp := Vector2i(col, row)

	# Locked overlay
	if _unlock_manager != null and not _unlock_manager.is_lot_unlocked(gp):
		var diamond := _cell_diamond(col, row)
		draw_colored_polygon(diamond, LOCKED_OVERLAY_COLOR)
		if _tex_lock:
			var c := grid_to_screen(col, row)
			var lock_size := 32.0
			draw_texture_rect(_tex_lock,
				Rect2(c.x - lock_size / 2.0, c.y - lock_size / 2.0, lock_size, lock_size),
				false)
		return

	# Placed trailer
	if GameState.is_lot_occupied(gp):
		_draw_trailer(col, row)

	# Hover overlay
	if gp == _hovered_lot:
		var diamond := _cell_diamond(col, row)
		if GameState.is_lot_occupied(gp):
			var lot := GameState.get_lot(gp)
			if lot.get("level", 1) < _max_upgrade_level:
				draw_colored_polygon(diamond, UPGRADE_HOVER_COLOR)
		else:
			draw_colored_polygon(diamond, HOVER_COLOR)

	# Flash overlay
	if gp == _flash_lot:
		draw_colored_polygon(_cell_diamond(col, row), INVALID_COLOR)


func _draw_trailer(col: int, row: int) -> void:
	var gp := Vector2i(col, row)
	var lot := GameState.get_lot(gp)
	var level: int = lot.get("level", 1)
	var tex := _tex_trailer_l2 if level >= 2 else _tex_trailer_l1
	if tex == null:
		return

	# South-anchor: sprite sits on the south vertex of the diamond
	var c := grid_to_screen(col, row)
	var sprite_w := float(tile_width)
	var sprite_h := float(tex.get_height()) * (float(tile_width) / float(tex.get_width()))
	var rect := Rect2(c.x - sprite_w / 2.0, c.y + tile_height / 2.0 - sprite_h, sprite_w, sprite_h)
	draw_texture_rect(tex, rect, false)


# --- Input -------------------------------------------------------------------

func _input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		_update_hover()
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var mouse_local := get_local_mouse_position()
		var grid_pos := world_to_grid(mouse_local)
		if _is_in_grid(grid_pos) and _is_valid_hit(mouse_local, grid_pos.x, grid_pos.y):
			lot_clicked.emit(grid_pos)


func _update_hover() -> void:
	var mouse_local := get_local_mouse_position()
	var grid_pos := world_to_grid(mouse_local)
	var new_hover: Vector2i
	if _is_in_grid(grid_pos) and _is_valid_hit(mouse_local, grid_pos.x, grid_pos.y):
		new_hover = grid_pos
	else:
		new_hover = NO_LOT
	if new_hover != _hovered_lot:
		_hovered_lot = new_hover
		queue_redraw()


# --- Helpers -----------------------------------------------------------------

func _is_in_grid(grid_pos: Vector2i) -> bool:
	return (
		grid_pos.x >= 0 and grid_pos.x < grid_cols and
		grid_pos.y >= 0 and grid_pos.y < grid_rows
	)
