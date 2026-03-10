extends Control

## Auth screen UI logic.
## Shown automatically on first launch (needs_auth) or via the Account button.
## Closes automatically when FirebaseAuth emits auth_state_changed.

@onready var email_field: LineEdit   = $Panel/VBox/EmailField
@onready var password_field: LineEdit = $Panel/VBox/PasswordField
@onready var status_label: Label      = $Panel/VBox/StatusLabel
@onready var guest_button: Button     = $Panel/VBox/GuestButton
@onready var create_button: Button    = $Panel/VBox/CreateButton
@onready var sign_in_button: Button   = $Panel/VBox/SignInButton
@onready var apple_button: Button     = $Panel/VBox/AppleButton
@onready var google_button: Button    = $Panel/VBox/GoogleButton
@onready var facebook_button: Button  = $Panel/VBox/FacebookButton
@onready var close_button: Button     = $Panel/VBox/CloseButton

## Set to true when opened from the Account button (not first-launch gate).
var show_close_button: bool = false


func _ready() -> void:
	close_button.visible = show_close_button

	FirebaseAuth.auth_state_changed.connect(_on_auth_state_changed)
	FirebaseAuth.sign_in_failed.connect(_on_sign_in_failed)
	FirebaseAuth.link_account_succeeded.connect(_on_link_succeeded)
	FirebaseAuth.link_account_failed.connect(_on_link_failed)

	guest_button.pressed.connect(_on_guest_pressed)
	create_button.pressed.connect(_on_create_pressed)
	sign_in_button.pressed.connect(_on_sign_in_pressed)
	apple_button.pressed.connect(FirebaseAuth.sign_in_with_apple)
	google_button.pressed.connect(FirebaseAuth.sign_in_with_google)
	facebook_button.pressed.connect(FirebaseAuth.sign_in_with_facebook)
	close_button.pressed.connect(queue_free)

	_refresh_ui()


func _refresh_ui() -> void:
	if FirebaseAuth.is_signed_in() and not FirebaseAuth.is_anonymous:
		status_label.text = "Signed in. Progress is backed up."
		guest_button.visible = false
		create_button.disabled = true
		sign_in_button.disabled = true
		email_field.editable = false
		password_field.editable = false
	else:
		guest_button.visible = true


func _on_guest_pressed() -> void:
	status_label.text = "Starting as guest..."
	guest_button.disabled = true
	FirebaseAuth.sign_in_as_guest()


func _on_create_pressed() -> void:
	var email := email_field.text.strip_edges()
	var password := password_field.text
	if email == "" or password == "":
		status_label.text = "Enter email and password."
		return
	status_label.text = "Creating account..."
	_set_form_enabled(false)
	FirebaseAuth.sign_up_with_email(email, password)


func _on_sign_in_pressed() -> void:
	var email := email_field.text.strip_edges()
	var password := password_field.text
	if email == "" or password == "":
		status_label.text = "Enter email and password."
		return
	status_label.text = "Signing in..."
	_set_form_enabled(false)
	FirebaseAuth.sign_in_with_email(email, password)


func _on_auth_state_changed(_user_id: String, _anonymous: bool) -> void:
	queue_free()


func _on_link_succeeded() -> void:
	queue_free()


func _on_sign_in_failed(error_message: String) -> void:
	status_label.text = error_message
	_set_form_enabled(true)
	guest_button.disabled = false


func _on_link_failed(error_message: String) -> void:
	status_label.text = error_message
	_set_form_enabled(true)


func _set_form_enabled(enabled: bool) -> void:
	email_field.editable = enabled
	password_field.editable = enabled
	create_button.disabled = not enabled
	sign_in_button.disabled = not enabled
