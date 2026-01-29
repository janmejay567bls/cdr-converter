from flask import Flask, render_template, request, send_file
import os
import subprocess
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["cdr_file"]
        output_type = request.form["format"]

        if not file:
            return "No file uploaded"

        uid = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, uid + ".cdr")
        file.save(input_path)

        output_path = os.path.join(OUTPUT_FOLDER, uid + "." + output_type)

        # Inkscape conversion
        cmd = [
            "inkscape",
            input_path,
            f"--export-type={output_type}",
            f"--export-filename={output_path}"
        ]

        subprocess.run(cmd, check=True)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


