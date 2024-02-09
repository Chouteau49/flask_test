from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Chemin pour enregistrer les fichiers téléchargés
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'upload_folder')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/uploader', methods=['GET', 'POST'])
def uploader_fichier():
    if request.method == 'POST':
        # Vérifier si le post a le fichier part
        if 'fichier' not in request.files:
            return 'Aucun fichier part'
        fichier = request.files['fichier']
        # Si l'utilisateur ne sélectionne pas de fichier, le navigateur
        # soumet un fichier vide sans nom de fichier.
        if fichier.filename == '':
            return 'Aucun fichier sélectionné'
        if fichier:
            fichier_path = os.path.join(app.config['UPLOAD_FOLDER'], fichier.filename)
            fichier.save(fichier_path)
            return f'Fichier téléchargé avec succès. Télécharger <a href="/uploads/{fichier.filename}">ici</a>.'


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
