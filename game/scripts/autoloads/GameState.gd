extends Node

## Global game state singleton.
## Registered as autoload "GameState" in project.godot.
##
## lots: keyed by Vector2i grid position.
## Each value is a lot data Dictionary created by _new_lot_data().
## Add fields to _new_lot_data() when new systems (economy, timers) are introduced.

var lots: Dictionary = {}

# Milestone 2+: player currency
var currency: int = 500

# --- Lot API -----------------------------------------------------------------

func place_trailer(grid_pos: Vector2i) -> void:
	lots[grid_pos] = _new_lot_data("trailer")

func is_lot_occupied(grid_pos: Vector2i) -> bool:
	return lots.has(grid_pos)

func get_lot(grid_pos: Vector2i) -> Dictionary:
	return lots.get(grid_pos, {})

# --- Private -----------------------------------------------------------------

func _new_lot_data(type: String) -> Dictionary:
	# All lot fields live here. Future systems add fields without touching callers.
	return {
		"type": type,
	}
