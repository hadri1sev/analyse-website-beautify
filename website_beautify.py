from bs4 import BeautifulSoup
import os
import html
import re

# Demander les fichiers à utiliser
index_to_convert = input('Fichier à convertir: ')

# Créer les dossiers et les chemins
sections_folder = os.path.join('resources', 'sections')
os.makedirs(sections_folder, exist_ok=True)
header_content_path = os.path.join('src', 'header-content.html')
header_path = os.path.join('src', 'header.html')
footer_path = os.path.join('src', 'footer.html')

# Ouvrir les fichiers ressources
header_content_file = open(header_content_path, "r", encoding="utf-8")
header_file = open(header_path, "r", encoding="utf-8")
footer_file = open(footer_path, "r", encoding="utf-8")
header_content = header_content_file.read()
header = header_file.read()
footer = footer_file.read()

# Ouvrir le fichier à convertir
with open(index_to_convert, encoding="utf-8") as fp:
    soup = BeautifulSoup(fp, 'lxml', from_encoding="UTF-8")

    #Récupérer le titre des chapitres
    menu_chapitre = soup.select('.dropdown-btn')

    # Créer le fichier 'index.html'
    with open("index.html", "w+", encoding="utf-8") as index:
        index.write(header)

        # Décomposer le code en chapitres
        chapter = soup.select('.chap')

        # Décomposer chaque chapitre en sections
        for i in range(0, len(chapter)):
            section = chapter[i].select('.sec')

            # Ajouter le chapitre dans le menu
            titre_chapitre = menu_chapitre[i].text
            index.write(f"""\t\t\t\t\t\t\t<li class="nav item">
            <a href="#chapitre{str(i)}" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">{titre_chapitre}</a>
            <ul class="collapse list-unstyled sidebarContent" id="chapitre{str(i)}">
            """)


            # Créer un fichier pour chaque section
            for j in range(0, len(section)):
                file = os.path.join(sections_folder, str(i) + "-" + str(j + 1) + ".html")

                # Ajouter la section dans le menu
                titre_section = section[j].h3.text
                index.write(f"""<li>
                <a href="resources/sections/{str(i)}-{str(j + 1)}.html" onclick="return loadIframe('ifrm', this.href)">{titre_section}</a>
                </li>
                """)

                # Mettre à jour les liens des pdfs
                for a in section[j].find_all('a'):
                    if 'pdfs' in a['href']:
                        a['href'] = f"../{a['href']}"

                # Mettre à jour les images
                for img in section[j].find_all('img'):
                    img['src'] = f"../{img['src']}"
                    img['class'] = f"img-fluid"

                # Mettre à jour les preuves
                preuves = section[j].select('.preuve')
                for k in range(len(preuves)):
                    preuve_id = preuves[k]['id']
                    preuve_text = BeautifulSoup(str(preuves[k]), 'html.parser')
                    for center in preuve_text.find_all('center'):
                        center.insert_before("</p>")
                        center.insert_after("<p>")
                    for ol in preuve_text.find_all('ol'):
                        ol.insert_before("</p>")
                        ol.insert_after("<p>")
                    for ul in preuve_text.find_all('ul'):
                        ul.insert_before("</p>")
                        ul.insert_after("<p>")
                    preuve_text.div.unwrap()
                    preuve_new = f"""<div class="preuve">
                    <a class="btn btn-outline-secondary" data-toggle="collapse" href="#{preuve_id}" role="button" aria-expanded="false" aria-controls="{preuve_id}">Preuve:</a>
                    <div class="collapse" id="{preuve_id}">
                    <div class="card card-body">
                    <p>{preuve_text}</p>
                    </div>
                    </div>
                    </div>
                    """
                    preuves[k].replace_with(preuve_new)
                preuves_entetes = section[j].select('.entete-preuve')
                for k in range(len(preuves_entetes)):
                    preuves_entetes[k].decompose()

                # Mettre à jour les quiz
                quiz = section[j].select('.quiz')
                for k in range(len(quiz)):
                    quiz_number = "quiz" + str(i) + "_" + str(j + 1) + "_" + str(k + 1)
                    quiz[k]['id'] = quiz_number
                    quiz_btn = f"""<span class="quiz-btn"><button type="button" class="btn btn-primary" onclick="montrer_cacher('{quiz_number}')">Solutions</button></span>"""
                    for span in quiz[k].find_all('span'):pass
                    span.replace_with(quiz_btn)

                # Mettre à jour les vidéos
                video_entete = section[j].select('.entete-video')
                videodiv = section[j].select('.videodiv')
                for k in range(len(video_entete)):
                    video_title = re.sub(r'(\s*)🎥(\s*)', '' , video_entete[k].text)
                    video = videodiv[k].script.string
                    video_url = re.search(r'([\w]+\.)+mp4', video).group()
                    video_thumbnail = re.search(r'([\w]+\.)+png', video).group()
                    video_id = re.search(r'ID([\w-]+)', video).group()
                    video_insert = f"""
                    <div class="video">
                    <a class="btn btn-outline-secondary" data-toggle="collapse" href="#{video_id}" role="button" aria-expanded="false" aria-controls="{video_id}">{video_title}</a>
                    <div class="collapse" id="{video_id}">
                    <div class="card card-body">
                    <video class="HTMLvideo" src="../videos/{video_url}" poster="../videos/{video_thumbnail}" controls=true></video>
                    </div>
                    </div>
                    </div>
                    """
                    videodiv[k].replace_with(video_insert)
                    video_entete[k].decompose()

                # Décoder les caractères spéciaux HTML
                content = html.unescape(str(section[j]))
                content_html = html.unescape(content)

                # Écrire la section
                with open(file, "w+", encoding="utf-8") as f:
                    f.write(header_content)
                    f.write(content_html)
                    f.write("\n</body>\n</html>")

            # Fermer la liste des sections dans le menu
            index.write("</ul>\n")

        # Écrire la fin du fichier 'index.html'
        index.write(footer)

# Fermer les fichiers ressources
header_content_file.close()
header_file.close()
footer_file.close()

print("Prêt !")