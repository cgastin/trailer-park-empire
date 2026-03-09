extends Control

## Auth screen UI logic.
## Shown via a settings button in Main. Allows players to create an account
## or sign in to link their anonymous progress to a permanent identity.

@onready var email_field: LineEdit        = $Panel/VBox/EmailField
@onready var password_field: LineEdit     = $Panel/VBox/PasswordField
@onready var status_label: Label          = $Panel/VBox/StatusLabel
@onready var create_button: Button        = $Panel/VBox/CreateButton
@onready var sign_in_button: Button       = $Panel/VBox/SignInButton
@onready var apple_button: Button         = $Panel/VBox/AppleButton
@onready var google_button: Button        = $Panel/VBox/GoogleButton
@onready var facebook_button: Button      = $Panel/VBox/FacebookButton
@onready var close_button: Button         = $Panel/CloseButton


func _ready() -> void:
	FirebaseAuth.link_account_succeeded.connect(_on_link_succeeded)
	FirebaseAuth.sign_in_failed.connect(_on_sign_in_failed)
	FirebaseAuth.link_account_failed.connect(_on_link_failed)
	FirebaseAuth.auth_state_changed.connect(_on_auth_state_changed)

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
		create_button.disabled = true
		sign_in_button.disabled = true
		email_field.editable = false
		password_field.editable = false
	else:
		status_label.text = "Create an account to back up your progress."


func _on_create_pressed() -> void:
	var email := email_field.text.strip_edges()
	var password := password_field.text
	if email == "" or password == "":
		status_label.text = "Enter email and password."
		return
	status_label.text = "Creating account..."
	FirebaseAuth.sign_up_with_email(email, password)


func _on_sign_in_pressed() -> void:
	var email := email_field.text.strip_edges()
	var password := password_field.text
	if email == "" or password == "":
		status_label.text = "Enter email and password."
		return
	status_label.text = "Signing in..."
	FirebaseAuth.sign_in_with_email(email, password)


func _on_link_succeeded() -> void:
	status_label.text = "Account linked! Progress is now backed up."
	_refresh_ui()


func _on_sign_in_failed(error_message: String) -> void:
	status_label.text = error_message


func _on_link_failed(error_message: String) -> void:
	status_label.text = error_message


func _on_auth_state_changed(_user_id: String, _anonymous: bool) -> void:
	_refresh_ui()
