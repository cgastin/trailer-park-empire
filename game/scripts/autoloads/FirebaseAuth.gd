extends Node

## Firebase Authentication singleton.
## Handles anonymous sign-in, token refresh, email/password account linking.
## Social login stubs are present; native plugin wiring is a future task.
##
## Signals:
##   auth_state_changed(user_id, is_anonymous) — emitted once auth is ready
##   sign_in_failed(error_message)
##   link_account_succeeded
##   link_account_failed(error_message)

const AUTH_PATH := "user://auth.json"

signal auth_state_changed(user_id: String, is_anonymous: bool)
signal needs_auth  # emitted on first launch when no stored token exists
signal sign_in_failed(error_message: String)
signal link_account_succeeded
signal link_account_failed(error_message: String)

var user_id: String = ""
var id_token: String = ""
var is_anonymous: bool = true

var _api_key: String = ""
var _auth_base_url: String = ""
var _token_base_url: String = ""
var _refresh_token: String = ""
var _token_expiry_time: float = 0.0  # Time.get_ticks_msec() value when token expires


func _ready() -> void:
	_load_config()
	_initialize()


func is_signed_in() -> bool:
	return user_id != ""


# --- Public API ---------------------------------------------------------------

func sign_in_with_email(email: String, password: String) -> void:
	var body := {"email": email, "password": password, "returnSecureToken": true}
	_post(_auth_base_url + "/accounts:signInWithPassword?key=" + _api_key, body,
		_on_email_sign_in_completed)


func sign_up_with_email(email: String, password: String) -> void:
	## Creates a new email/password account. Always uses signUp (no anonymous linking)
	## because Identity Platform blocks accounts:update before email verification.
	## Local save data is preserved on device and uploads to the new account after sign-up.
	var body := {"email": email, "password": password, "returnSecureToken": true}
	_post(_auth_base_url + "/accounts:signUp?key=" + _api_key, body,
		_on_email_sign_up_completed)


func sign_in_with_apple() -> void:
	_emit_social_stub("Apple")


func sign_in_with_google() -> void:
	_emit_social_stub("Google")


func sign_in_with_facebook() -> void:
	_emit_social_stub("Facebook")


func link_account(provider_token: String, provider: String) -> void:
	## Placeholder for future native plugin integration.
	## When native plugins exist they call sign_in_with_provider_token() instead.
	sign_in_failed.emit("Native plugin not available for " + provider)


func sign_in_with_provider_token(_token: String, _provider: String) -> void:
	## Called by native plugins after obtaining a social ID token.
	## Implementation deferred to Milestone 4b (social auth phase).
	sign_in_failed.emit("Social auth REST exchange not yet implemented")


# --- Internal auth flow -------------------------------------------------------

func sign_in_as_guest() -> void:
	_sign_in_anonymously()


func _initialize() -> void:
	var stored := _load_auth_file()
	if stored.is_empty():
		# First launch — let the user choose (guest or account)
		needs_auth.emit()
		return
	_refresh_token = stored.get("refresh_token", "")
	user_id = stored.get("user_id", "")
	is_anonymous = stored.get("is_anonymous", true)
	if _refresh_token == "":
		needs_auth.emit()
	else:
		_exchange_refresh_token()


func _sign_in_anonymously() -> void:
	var body := {"returnSecureToken": true}
	_post(_auth_base_url + "/accounts:signUp?key=" + _api_key, body,
		_on_anonymous_sign_in_completed)


func _exchange_refresh_token() -> void:
	var body := {"grant_type": "refresh_token", "refresh_token": _refresh_token}
	_post(_token_base_url + "/token?key=" + _api_key, body,
		_on_token_refresh_completed)


func _link_anonymous_to_email(email: String, password: String) -> void:
	var body := {
		"idToken": id_token,
		"email": email,
		"password": password,
		"returnSecureToken": true
	}
	_post(_auth_base_url + "/accounts:update?key=" + _api_key, body,
		_on_link_completed)


# --- Response handlers --------------------------------------------------------

func _on_anonymous_sign_in_completed(code: int, data: Dictionary) -> void:
	if code != 200:
		sign_in_failed.emit(_extract_error(data))
		return
	_apply_auth_response(data, true)


func _on_token_refresh_completed(code: int, data: Dictionary) -> void:
	if code != 200:
		# Refresh token invalid — fall back to new anonymous sign-in
		_sign_in_anonymously()
		return
	id_token = data.get("id_token", "")
	_refresh_token = data.get("refresh_token", _refresh_token)
	var expires_in: float = float(data.get("expires_in", "3600"))
	_token_expiry_time = Time.get_ticks_msec() + (expires_in - 60.0) * 1000.0
	_save_auth_file()
	auth_state_changed.emit(user_id, is_anonymous)


func _on_email_sign_in_completed(code: int, data: Dictionary) -> void:
	if code != 200:
		sign_in_failed.emit(_extract_error(data))
		return
	_apply_auth_response(data, false)


func _on_email_sign_up_completed(code: int, data: Dictionary) -> void:
	if code != 200:
		sign_in_failed.emit(_extract_error(data))
		return
	_apply_auth_response(data, false)


func _on_link_completed(code: int, data: Dictionary) -> void:
	if code != 200:
		link_account_failed.emit(_extract_error(data))
		return
	id_token = data.get("idToken", id_token)
	_refresh_token = data.get("refreshToken", _refresh_token)
	is_anonymous = false
	_save_auth_file()
	link_account_succeeded.emit()


func _apply_auth_response(data: Dictionary, anonymous: bool) -> void:
	user_id = data.get("localId", data.get("user_id", ""))
	id_token = data.get("idToken", data.get("id_token", ""))
	_refresh_token = data.get("refreshToken", data.get("refresh_token", ""))
	var expires_in: float = float(data.get("expiresIn", data.get("expires_in", "3600")))
	_token_expiry_time = Time.get_ticks_msec() + (expires_in - 60.0) * 1000.0
	is_anonymous = anonymous
	_save_auth_file()
	auth_state_changed.emit(user_id, is_anonymous)


# --- Token freshness ----------------------------------------------------------

func ensure_fresh_token() -> Signal:
	## Callers await this before using id_token for API calls.
	## If token is still fresh, emits immediately via a one-shot signal.
	var sig := auth_state_changed
	if Time.get_ticks_msec() < _token_expiry_time:
		# Already fresh — emit immediately so callers can await
		call_deferred("_emit_auth_unchanged")
	else:
		_exchange_refresh_token()
	return sig


func _emit_auth_unchanged() -> void:
	auth_state_changed.emit(user_id, is_anonymous)


# --- File I/O -----------------------------------------------------------------

func _load_auth_file() -> Dictionary:
	if not FileAccess.file_exists(AUTH_PATH):
		return {}
	var file := FileAccess.open(AUTH_PATH, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) != OK:
		return {}
	return json.get_data()


func _save_auth_file() -> void:
	var file := FileAccess.open(AUTH_PATH, FileAccess.WRITE)
	file.store_string(JSON.stringify({
		"user_id": user_id,
		"refresh_token": _refresh_token,
		"is_anonymous": is_anonymous,
	}))


# --- HTTP helpers -------------------------------------------------------------

func _post(url: String, body: Dictionary, callback: Callable) -> void:
	var http := HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(_on_http_done.bind(http, callback))
	var headers := ["Content-Type: application/json"]
	http.request(url, headers, HTTPClient.METHOD_POST, JSON.stringify(body))


func _on_http_done(result: int, code: int, _headers: PackedStringArray,
		body: PackedByteArray, http: HTTPRequest, callback: Callable) -> void:
	http.queue_free()
	if result != HTTPRequest.RESULT_SUCCESS:
		callback.call(0, {})
		return
	var json := JSON.new()
	var data: Dictionary = {}
	if json.parse(body.get_string_from_utf8()) == OK:
		data = json.get_data()
	callback.call(code, data)


# --- Config -------------------------------------------------------------------

func _load_config() -> void:
	var path := "res://data/firebase_config.json"
	if not FileAccess.file_exists(path):
		push_error("FirebaseAuth: firebase_config.json not found")
		return
	var file := FileAccess.open(path, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) != OK:
		push_error("FirebaseAuth: failed to parse firebase_config.json")
		return
	var cfg: Dictionary = json.get_data()
	_api_key = cfg.get("api_key", "")
	_auth_base_url = cfg.get("auth_base_url", "")
	_token_base_url = cfg.get("token_base_url", "")


# --- Utility ------------------------------------------------------------------

func _extract_error(data: Dictionary) -> String:
	var error: Dictionary = data.get("error", {})
	return error.get("message", "Unknown error")


func _emit_social_stub(provider: String) -> void:
	sign_in_failed.emit(provider + " sign-in coming soon")
