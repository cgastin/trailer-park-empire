extends Node

## Global game state singleton.
## Registered as autoload "GameState" in project.godot.

var lots: Dictionary = {}   # Vector2i -> lot data dict
var currency: int = 500     # Starting cash (used in Milestone 2+)
