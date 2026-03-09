extends Node2D

const TrailerPlacerScript := preload("res://scripts/TrailerPlacer.gd")

@onready var lot_grid: Node2D = $LotGrid
@onready var status_label: Label   = $UI/StatusLabel
@onready var currency_label: Label = $UI/CurrencyLabel
@onready var save_system: Node     = $SaveSystem

var trailer_placer: Node

func _ready() -> void:
	save_system.load_save()

	trailer_placer = TrailerPlacerScript.new()
	add_child(trailer_placer)
	lot_grid.lot_clicked.connect(trailer_placer.place_trailer)
	trailer_placer.trailer_placed.connect(_on_trailer_placed)
	trailer_placer.placement_failed.connect(_on_placement_failed)
	trailer_placer.insufficient_funds.connect(_on_insufficient_funds)

	GameState.currency_changed.connect(_on_currency_changed)
	_update_currency_label()

func _on_trailer_placed(grid_pos: Vector2i) -> void:
	lot_grid.queue_redraw()
	save_system.save()
	status_label.text = "Trailer placed at %s" % str(grid_pos)

func _on_placement_failed(grid_pos: Vector2i) -> void:
	lot_grid.flash_invalid(grid_pos)
	status_label.text = "That lot is already occupied!"

func _on_insufficient_funds(_grid_pos: Vector2i) -> void:
	status_label.text = "Not enough coins!"

func _on_currency_changed(new_amount: int) -> void:
	currency_label.text = "Coins: %d" % new_amount

func _update_currency_label() -> void:
	currency_label.text = "Coins: %d" % GameState.currency
