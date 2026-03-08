extends Node2D

const TrailerPlacerScript := preload("res://scripts/TrailerPlacer.gd")

@onready var lot_grid: Node2D = $LotGrid
@onready var status_label: Label = $UI/StatusLabel

var trailer_placer: Node

func _ready() -> void:
	trailer_placer = TrailerPlacerScript.new()
	add_child(trailer_placer)
	lot_grid.lot_clicked.connect(trailer_placer.place_trailer)
	trailer_placer.trailer_placed.connect(_on_trailer_placed)
	trailer_placer.placement_failed.connect(_on_placement_failed)

func _on_trailer_placed(grid_pos: Vector2i) -> void:
	lot_grid.queue_redraw()
	status_label.text = "Trailer placed at %s" % str(grid_pos)

func _on_placement_failed(_grid_pos: Vector2i) -> void:
	status_label.text = "That lot is already occupied!"
