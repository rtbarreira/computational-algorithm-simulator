from flask import Flask, jsonify, send_file, send_from_directory
import subprocess
import os
import shutil
import tempfile

app = Flask(__name__)
WORKDIR = os.getcwd()

def run_cmd(cmd, cwd=WORKDIR):
    result = subprocess.run(
        cmd, cwd=cwd, shell=True,
        capture_output=True, text=True
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }

# Rota raiz
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API de análise de código rodando!",
        "endpoints": [
            "/coverage (POST)",
            "/coverage/report (GET)",
            "/coverage/artifact (GET)",
            "/mutation (POST)",
            "/mutation/log (GET)",
            "/mutation/report (GET)",
            "/mutation/artifact (GET)"
        ]
    })

# CLOVERAGE
@app.route("/coverage", methods=["POST"])
def run_cloverage():
    cmd = "lein do clean, test, cloverage --html"
    result = run_cmd(cmd)

    coverage_file = os.path.join(WORKDIR, "target/coverage/codecov.json")
    if os.path.exists(coverage_file):
        with open(coverage_file) as f:
            result["codecov"] = f.read()

    return jsonify(result)

@app.route("/coverage/report", methods=["GET"])
def get_cloverage_report():
    report_file = os.path.join(WORKDIR, "target/coverage/index.html")
    if os.path.exists(report_file):
        return send_file(report_file, mimetype="text/html")
    return jsonify({"error": "Relatório de cobertura não encontrado"}), 404

@app.route("/coverage/<path:filename>", methods=["GET"])
def coverage_static(filename):
    coverage_dir = os.path.join(WORKDIR, "target/coverage")
    file_path = os.path.join(coverage_dir, filename)
    if os.path.exists(file_path):
        return send_from_directory(coverage_dir, filename)
    return jsonify({"error": "Arquivo não encontrado"}), 404

@app.route("/coverage/artifact", methods=["GET"])
def get_cloverage_artifact():
    report_dir = os.path.join(WORKDIR, "target/coverage")
    if os.path.exists(report_dir):
        tmp_dir = tempfile.mkdtemp()
        zip_path = shutil.make_archive(os.path.join(tmp_dir, "coverage-report"), 'zip', report_dir)
        return send_file(zip_path, mimetype="application/zip", as_attachment=True, download_name="coverage-report.zip")
    return jsonify({"error": "Diretório de cobertura não encontrado"}), 404

# MUTATION usando lein-mutate
@app.route("/mutation", methods=["POST"])
def run_mutation():
    report_dir = os.path.join(WORKDIR, "target/mutant")
    print(report_dir)
    os.makedirs(report_dir, exist_ok=True)
    log_file = os.path.join(report_dir, "mutation.log")

    # Executa lein-mutate e salva tudo no log
    with open(log_file, "w") as f:
        result = subprocess.run(
            "lein mutate",          # string e shell=True
            cwd=WORKDIR,
            shell=True,             # importante para redirecionar stdout/stderr
            stdout=f,
            stderr=subprocess.STDOUT,
            text=True
        )

    return jsonify({
        "message": "Mutação executada com lein-mutate",
        "returncode": result.returncode,
        "log_file": "target/mutant/mutation.log"
    })


@app.route("/mutation/log", methods=["GET"])
def get_mutation_log():
    log_file = os.path.join(WORKDIR, "target/mutant/mutation.log")
    if os.path.exists(log_file):
        return send_file(log_file, mimetype="text/plain")
    return jsonify({"error": "Log de mutação não encontrado"}), 404

@app.route("/mutation/report", methods=["GET"])
def get_mutation_report():
    log_file = os.path.join(WORKDIR, "target/mutant/mutation.log")
    if not os.path.exists(log_file):
        return jsonify({"error": "Mutação ainda não foi executada"}), 404

    with open(log_file) as f:
        log_content = f.read()

    # resumo básico de mutantes
    killed = log_content.lower().count("killed")
    survived = log_content.lower().count("survived")

    return jsonify({
        "killed": killed,
        "survived": survived,
        "raw_log": log_content[:2000]  # preview dos primeiros 2000 caracteres
    })

@app.route("/mutation/artifact", methods=["GET"])
def get_mutation_artifact():
    report_dir = os.path.join(WORKDIR, "target/mutant")
    if os.path.exists(report_dir) and os.listdir(report_dir):
        tmp_dir = tempfile.mkdtemp()
        zip_path = shutil.make_archive(os.path.join(tmp_dir, "mutation-report"), 'zip', report_dir)
        return send_file(zip_path, mimetype="application/zip", as_attachment=True, download_name="mutation-report.zip")
    return jsonify({"error": "Nenhum relatório de mutação encontrado"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
