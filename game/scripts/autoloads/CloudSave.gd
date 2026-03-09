extends Node

## Firestore cloud save singleton.
## Uploads and downloads the save document for the authenticated user.
## All operations are async and non-blocking — local save always runs first.
##
## Document path: users/{uid}/save/game
## The entire save dictionary is stored as a JSON string in a single "data" field,
## with a top-level "saved_at" integer field for query/rule use.

signal upload_completed
signal download_completed(data: Dictionary)
signal cloud_save_failed(reason: String)

var _project_id: String = ""
var _firestore_base_url: String = ""


func _ready() -> void:
	_load_config()


# --- Public API ---------------------------------------------------------------

func upload(data: Dictionary) -> void:
	if not FirebaseAuth.is_signed_in():
		return
	if FirebaseAuth.id_token == "":
		return
	var uid := FirebaseAuth.user_id
	var url := _doc_url(uid)
	var saved_at: int = int(data.get("saved_at", 0))
	var firestore_body := {
		"fields": {
			"data": {"stringValue": JSON.stringify(data)},
			"saved_at": {"integerValue": str(saved_at)},
		}
	}
	var headers := [
		"Content-Type: application/json",
		"Authorization: Bearer " + FirebaseAuth.id_token,
	]
	_request(url, HTTPClient.METHOD_PATCH, headers, firestore_body,
		_on_upload_completed)


func download() -> void:
	if not FirebaseAuth.is_signed_in():
		download_completed.emit({})
		return
	var uid := FirebaseAuth.user_id
	var url := _doc_url(uid)
	var headers := [
		"Authorization: Bearer " + FirebaseAuth.id_token,
	]
	_request(url, HTTPClient.METHOD_GET, headers, {},
		_on_download_completed)


# --- Response handlers --------------------------------------------------------

func _on_upload_completed(code: int, data: Dictionary) -> void:
	if code == 200:
		upload_completed.emit()
	else:
		var msg := _extract_error(data)
		cloud_save_failed.emit("Upload failed (%d): %s" % [code, msg])


func _on_download_completed(code: int, data: Dictionary) -> void:
	if code == 404:
		# No cloud save yet — this is normal for new users
		download_completed.emit({})
		return
	if code != 200:
		var msg := _extract_error(data)
		cloud_save_failed.emit("Download failed (%d): %s" % [code, msg])
		download_completed.emit({})
		return
	var fields: Dictionary = data.get("fields", {})
	var data_field: Dictionary = fields.get("data", {})
	var json_str: String = data_field.get("stringValue", "")
	if json_str == "":
		download_completed.emit({})
		return
	var json := JSON.new()
	if json.parse(json_str) != OK:
		cloud_save_failed.emit("Failed to parse cloud save data")
		download_completed.emit({})
		return
	download_completed.emit(json.get_data())


# --- HTTP helpers -------------------------------------------------------------

func _request(url: String, method: int, headers: Array,
		body: Dictionary, callback: Callable) -> void:
	var http := HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(_on_http_done.bind(http, callback))
	var body_str := "" if body.is_empty() else JSON.stringify(body)
	http.request(url, headers, method, body_str)


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


# --- Config & helpers ---------------------------------------------------------

func _load_config() -> void:
	var path := "res://data/firebase_config.json"
	if not FileAccess.file_exists(path):
		push_error("CloudSave: firebase_config.json not found")
		return
	var file := FileAccess.open(path, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) != OK:
		push_error("CloudSave: failed to parse firebase_config.json")
		return
	var cfg: Dictionary = json.get_data()
	_project_id = cfg.get("project_id", "")
	_firestore_base_url = cfg.get("firestore_base_url", "")


func _doc_url(uid: String) -> String:
	return "%s/projects/%s/databases/(default)/documents/users/%s/save/game" \
		% [_firestore_base_url, _project_id, uid]


func _extract_error(data: Dictionary) -> String:
	var error: Dictionary = data.get("error", {})
	return error.get("message", "Unknown error")
