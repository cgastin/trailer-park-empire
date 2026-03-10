extends Node2D

const TrailerPlacerScript  := preload("res://scripts/TrailerPlacer.gd")
const TrailerUpgraderScript := preload("res://scripts/economy/TrailerUpgrader.gd")
const UnlockManagerScript   := preload("res://scripts/progression/UnlockManager.gd")
const QuestManagerScript    := preload("res://scripts/progression/QuestManager.gd")
const AuthScreenScene       := preload("res://scenes/ui/AuthScreen.tscn")

@onready var lot_grid: Node2D         = $LotGrid
@onready var status_label: Label      = $UI/StatusLabel
@onready var currency_label: Label    = $UI/CurrencyLabel
@onready var quest_label: Label       = $UI/QuestLabel
@onready var save_system: Node        = $SaveSystem
@onready var income_manager: Node     = $IncomeManager
@onready var account_button: Button   = $UI/AccountButton
@onready var park_background: Sprite2D = $ParkBackground

var trailer_placer: Node
var trailer_upgrader: Node
var unlock_manager: Node
var quest_manager: Node

var _local_saved_at: int = 0

func _ready() -> void:
	_load_background()
	unlock_manager = UnlockManagerScript.new()
	add_child(unlock_manager)
	unlock_manager.grid_unlocked.connect(_on_grid_unlocked)
	lot_grid.set_unlock_manager(unlock_manager)

	quest_manager = QuestManagerScript.new()
	add_child(quest_manager)
	quest_manager.quest_completed.connect(_on_quest_completed)
	quest_manager.quest_activated.connect(_on_quest_activated)
	save_system.quest_manager = quest_manager

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

	income_manager.income_ticked.connect(quest_manager.notify_income_earned)
	lot_grid.lot_clicked.connect(_on_lot_clicked)
	GameState.currency_changed.connect(_on_currency_changed)
	_update_currency_label()
	_update_quest_label(quest_manager.get_active_quest())

	# Wire auth and cloud save — non-blocking; local game already loaded above
	FirebaseAuth.needs_auth.connect(_show_auth_screen)
	FirebaseAuth.auth_state_changed.connect(_on_auth_state_changed)
	save_system.local_save_completed.connect(_on_local_save_completed)
	CloudSave.download_completed.connect(_on_cloud_download_completed)
	account_button.pressed.connect(_on_account_button_pressed)

# Route clicks: locked lots are blocked, occupied go to upgrader, empty go to placer
func _on_lot_clicked(grid_pos: Vector2i) -> void:
	if not unlock_manager.is_lot_unlocked(grid_pos):
		status_label.text = "Locked! Place more trailers to unlock."
		return
	if GameState.is_lot_occupied(grid_pos):
		trailer_upgrader.upgrade_trailer(grid_pos)
	else:
		trailer_placer.place_trailer(grid_pos)

func _on_trailer_placed(grid_pos: Vector2i) -> void:
	unlock_manager.check_unlocks()
	quest_manager.notify_trailer_placed()
	lot_grid.queue_redraw()
	save_system.save()
	status_label.text = "Trailer placed at %s" % str(grid_pos)

func _on_trailer_upgraded(grid_pos: Vector2i) -> void:
	quest_manager.notify_trailer_upgraded()
	lot_grid.queue_redraw()
	save_system.save()
	status_label.text = "Trailer upgraded at %s!" % str(grid_pos)

func _on_upgrade_maxed(_grid_pos: Vector2i) -> void:
	status_label.text = "Already at max level!"

func _on_insufficient_funds(_grid_pos: Vector2i) -> void:
	status_label.text = "Not enough coins!"

func _on_currency_changed(new_amount: int) -> void:
	currency_label.text = "Coins: %d" % new_amount

func _on_grid_unlocked() -> void:
	lot_grid.queue_redraw()
	status_label.text = "New area unlocked!"

func _on_quest_completed(quest: Dictionary) -> void:
	var reward: int = int(quest.get("reward", 0))
	if reward > 0:
		GameState.add_currency(reward)
	status_label.text = "Quest complete! +" + str(reward) + " coins"

func _on_quest_activated(quest: Dictionary) -> void:
	_update_quest_label(quest)

func _update_quest_label(quest: Dictionary) -> void:
	if quest.is_empty():
		quest_label.text = "Quest: All complete!"
	else:
		quest_label.text = "Quest: " + quest.get("description", "")

func _update_currency_label() -> void:
	currency_label.text = "Coins: %d" % GameState.currency

# --- Cloud save / auth handlers -----------------------------------------------

func _on_auth_state_changed(_user_id: String, _anonymous: bool) -> void:
	CloudSave.download()


func _on_local_save_completed(data: Dictionary) -> void:
	_local_saved_at = int(data.get("saved_at", 0))
	CloudSave.upload(data)


func _on_cloud_download_completed(data: Dictionary) -> void:
	if data.is_empty():
		# No cloud save — push local state up as initial backup
		if FirebaseAuth.is_signed_in():
			save_system.save()
		return
	var cloud_saved_at: int = int(data.get("saved_at", 0))
	if cloud_saved_at > _local_saved_at:
		save_system.apply_cloud_data(data)
		lot_grid.queue_redraw()
		_update_currency_label()
		_update_quest_label(quest_manager.get_active_quest())
		status_label.text = "Progress restored from cloud."


func _show_auth_screen(optional: bool = false) -> void:
	# Controls must live inside a CanvasLayer to render in screen space.
	var auth_screen = AuthScreenScene.instantiate()
	auth_screen.show_close_button = optional
	$UI.add_child(auth_screen)


func _on_account_button_pressed() -> void:
	_show_auth_screen(true)


func _load_background() -> void:
	park_background.texture = load("res://assets/sprites/bg_park.png")
