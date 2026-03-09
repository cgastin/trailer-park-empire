extends Node

## Global game state singleton.
## Registered as autoload "GameState" in project.godot.
##
## lots: keyed by Vector2i grid position.
## Each value is a lot data Dictionary created by _new_lot_data().
## Add fields to _new_lot_data() when new systems (economy, timers) are introduced.

var lots: Dictionary = {}
var currency: int = 500

signal currency_changed(new_amount: int)

# --- Lot API -----------------------------------------------------------------

func place_trailer(grid_pos: Vector2i) -> void:
	lots[grid_pos] = _new_lot_data("trailer")

func is_lot_occupied(grid_pos: Vector2i) -> bool:
	return lots.has(grid_pos)

func get_lot(grid_pos: Vector2i) -> Dictionary:
	return lots.get(grid_pos, {})

# --- Currency API ------------------------------------------------------------

func add_currency(amount: int) -> void:
	currency += amount
	currency_changed.emit(currency)

func deduct_currency(amount: int) -> bool:
	if currency < amount:
		return false
	currency -= amount
	currency_changed.emit(currency)
	return true

# --- Private -----------------------------------------------------------------

func _new_lot_data(type: String) -> Dictionary:
	# All lot fields live here. Future systems add fields without touching callers.
	return {
		"type": type,
	}
