from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
NOTES_FILE = "notes.json"

# Helper functions
def read_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r") as f:
        return json.load(f)

def write_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)

# ---------------------------
# Home page
# ---------------------------
@app.route("/")
def home():
    notes = read_notes()
    return render_template("index.html", notes=notes)

# ---------------------------
# Get all notes
# ---------------------------
@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(read_notes())

# ---------------------------
# Add a new note
# ---------------------------
@app.route("/notes", methods=["POST"])
def add_note():
    data = request.json
    notes = read_notes()
    note_id = max([n["id"] for n in notes], default=0) + 1
    new_note = {"id": note_id, "title": data["title"], "content": data["content"]}
    notes.append(new_note)
    write_notes(notes)
    return jsonify(new_note)

# ---------------------------
# Update a note
# ---------------------------
@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.json
    notes = read_notes()
    for note in notes:
        if note["id"] == note_id:
            note["title"] = data.get("title", note["title"])
            note["content"] = data.get("content", note["content"])
            write_notes(notes)
            return jsonify(note)
    return jsonify({"error": "Note not found"}), 404

# ---------------------------
# Delete a note
# ---------------------------
@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    notes = read_notes()
    notes = [n for n in notes if n["id"] != note_id]
    write_notes(notes)
    return jsonify({"message": f"Note {note_id} deleted."})

if __name__ == "__main__":
    app.run(debug=True)
