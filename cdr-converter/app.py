from flask import Flask, render_template, request
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
        file = request.files.get("cdr_file")
        output_type = request.form.get("format")

        if not file:
            return "No file uploaded"

        uid = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, uid + ".cdr")
        file.save(input_path)

        output_path = os.path.join(OUTPUT_FOLDER, uid + "." + output_type)

        # Inkscape conversion (disabled on Render)
        try:
            cmd = [
                "inkscape",
                input_path,
                f"--export-type={output_type}",
                f"--export-filename={output_path}"
            ]
            subprocess.run(cmd, check=True)
            return "Conversion completed (local/VPS only)"
        except Exception as e:
            return f"Conversion not available on this server: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
