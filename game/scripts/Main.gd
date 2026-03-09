extends Node2D

const TrailerPlacerScript  := preload("res://scripts/TrailerPlacer.gd")
const TrailerUpgraderScript := preload("res://scripts/economy/TrailerUpgrader.gd")

@onready var lot_grid: Node2D = $LotGrid
@onready var status_label: Label   = $UI/StatusLabel
@onready var currency_label: Label = $UI/CurrencyLabel
@onready var save_system: Node     = $SaveSystem

var trailer_placer: Node
var trailer_upgrader: Node

func _ready() -> void:
	save_system.load_save()

	trailer_placer = TrailerPlacerScript.new()
	add_child(trailer_placer)
	trailer_placer.trailer_placed.connect(_on_trailer_placed)
	trailer_placer.insufficient_funds.connect(_on_insufficient_funds)

	trailer_upgrader = TrailerUpgraderScript.new()
	add_child(trailer_upgrader)
	trailer_upgrader.trailer_upgraded.connect(_on_trailer_upgraded)
	trailer_upgrader.upgrade_maxed.connect(_on_upgrade_maxed)
	trailer_upgrader.insufficient_funds.connect(_on_insufficient_funds)

	lot_grid.lot_clicked.connect(_on_lot_clicked)
	GameState.currency_changed.connect(_on_currency_changed)
	_update_currency_label()

# Route clicks: occupied lots go to upgrader, empty lots go to placer
func _on_lot_clicked(grid_pos: Vector2i) -> void:
	if GameState.is_lot_occupied(grid_pos):
		trailer_upgrader.upgrade_trailer(grid_pos)
	else:
		trailer_placer.place_trailer(grid_pos)

func _on_trailer_placed(grid_pos: Vector2i) -> void:
	lot_grid.queue_redraw()
	save_system.save()
	status_label.text = "Trailer placed at %s" % str(grid_pos)

func _on_trailer_upgraded(grid_pos: Vector2i) -> void:
	lot_grid.queue_redraw()
	save_system.save()
	status_label.text = "Trailer upgraded at %s!" % str(grid_pos)

func _on_upgrade_maxed(_grid_pos: Vector2i) -> void:
	status_label.text = "Already at max level!"

func _on_insufficient_funds(_grid_pos: Vector2i) -> void:
	status_label.text = "Not enough coins!"

func _on_currency_changed(new_amount: int) -> void:
	currency_label.text = "Coins: %d" % new_amount

func _update_currency_label() -> void:
	currency_label.text = "Coins: %d" % GameState.currency
