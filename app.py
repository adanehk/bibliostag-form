from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

# Carpeta donde se guardarán los archivos
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Crear carpeta si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Conexión a MySQL
def conectar():
    return mysql.connector.connect(
        host="trolley.proxy.rlwy.net",
        user="root",
        password="TAwCngqaDeGFtlrVVWpFTzphoVcYbrbe",
        database="railway",
        port=11478
    )


@app.route("/")
def formulario():
    return render_template("formulario.html")

@app.route("/registro", methods=["POST"])
def registro():
    # Datos del formulario
    fecha = request.form.get("fecha")
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    dni = request.form.get("dni")
    telefono = request.form.get("telefono")
    empresa = request.form.get("empresa")
    tipo = request.form.get("tipo")
    detalle = request.form.get("detalle")
    documentacion = ", ".join(request.form.getlist("documentacion"))
    prioridad = request.form.get("prioridad")

    # Archivos subidos
    archivos = request.files.getlist("archivo")
    nombres_archivos = []

    for archivo in archivos:
        if archivo.filename != "":
            ruta = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
            archivo.save(ruta)
            nombres_archivos.append(archivo.filename)

    archivos_guardados = ", ".join(nombres_archivos)

    # Guardar en MySQL
    db = conectar()
    cursor = db.cursor()

    sql = """
    INSERT INTO registro (fecha, nombre, apellido, dni, telefono, empresa, tipo, detalle, documentacion, prioridad, archivo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (fecha, nombre, apellido, dni, telefono, empresa, tipo, detalle, documentacion, prioridad, archivos_guardados)

    cursor.execute(sql, valores)
    db.commit()

    cursor.close()
    db.close()

    return "Registro enviado correctamente"


    cursor.execute(sql, valores)
    db.commit()

    cursor.close()
    db.close()

    return f"""
    <h2>Solicitud registrada correctamente</h2>
    <p>Gracias, {nombre}. Tu solicitud ha sido guardada.</p>
    <p><strong>Archivos subidos:</strong> {archivos_guardados}</p>
    <a href="/">Volver al formulario</a>
    """

if __name__ == "__main__":
     app.run()
