from flask import Flask , send_from_directory
from flask_flatpages import FlatPages
from flask import render_template
import os
from itertools import chain

FLATPAGES_EXTENSION = '.md'
FLATPAGES_AUTO_RELOAD = True

app = Flask(__name__) 
app.config['FLATPAGES_ROOT'] = '/miscell0rg-main'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FLATPAGES_MARKDOWN_EXTENSIONS = ['extra']
FLATPAGES_EXTENSION_CONFIGS = {
    'codehilite': {
        'linenums': 'True'
    }
}



app.config.from_object(__name__)
pages = FlatPages(app)
DNpages = FlatPages(app)
application = app
#{pages.get('foo')

def imagelist(articlename):
    dir_path = os.path.dirname(os.path.realpath(articlename))+'/pages/'  #avec OS,  il récupères l'adresse du dossier dans le serv/ordi. (+/pages/ = réfères au lieu depuis le dossier "vvenv", dossier parent) il dépends du nom "articlename"
    gallery_path = os.path.join(dir_path, articlename)
    if os.path.exists(gallery_path):
        images = [f for f in os.listdir(gallery_path) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.gif')] #récupères les noms des fichiers, en repérant leurs extensions, afin de créer une liste de noms de fichiers.
        return gallery_path ,images
    else:
        return None, None #possibilité de mettre plusieurs valeurs return à l'aide d'une virgule.

#Gère les onglets du menu, en gros les catégories de nos articles (sert au dynamisme du site internet)
def Liste_cat():
    articles = (p for p in pages if 'published' in p.meta)    #si dans les méta : 'published' est écrit avec une date fixe, on fait une liste de catégories.
    catList = []
    for a in articles:
        catList.append(a.meta['cat']) #ici on ajoute les catégories dans la liste, signifiées par la ligne "cat" dans les meta.
    catList = list(dict.fromkeys(catList)) #rends les catégories uniques, retires les doublons de chaque catégorie. 
    return catList #renvoie une liste des cat.

#def Liste_DNcat():
 #   articles = (p for p in DNpages if 'published' in p.meta)    #si dans les méta : 'published' est écrit avec une date fixe, on fait une liste de catégories.
 #     DNcatList = []
 #    for a in articles:
    #    DNcatList.append(a.meta['cat']) #ici on ajoute les catégories dans la liste, signifiées par la ligne "cat" dans les meta.
   # DNcatList = list(dict.fromkeys(DNcatList)) #rends les catégories uniques, retires les doublons de chaque catégorie. 
    #return DNcatList #renvoie une liste des cat de dN.

@app.route('/') #en mode Hello python... précises à quelle fonction appartient une action, ça s'appelle un décorateur le "@".
def rootpage():
    return render_template('rootpage.html') #renvoie au client les templates, ici "index.html" avec liste d'art. et de cat.


@app.route('/razzia909') #en mode Hello python... précises à quelle fonction appartient une action, ça s'appelle un décorateur le "@".
def uindex():
    # Articles are pages with a publication date
    articles = (p for p in pages if 'published' in p.meta)
    latest = sorted(articles, reverse=True, #fait la liste des articles écrits, classés par ordre de publication dans la liste "latest"
                    key=lambda p: p.meta['published'])
    catList = Liste_cat() #stockes les cat dans notre catList
    return render_template('uindex.html', articles=latest , catList=catList  ) #renvoie au client les templates, ici "index.html" avec liste d'art. et de cat.

@app.route('/razzia909/<path:path>')
def page(path):
    page = pages.get_or_404(path)
    catList = Liste_cat()
    g_path, imgs = imagelist(path)   #vérifies s'il y'a une galerie ou non
    if imgs:
        return render_template('single.html', page=page ,catList=catList  , g_path=g_path, imgs = imgs)
    else :
        return render_template('single.html', page=page ,catList=catList)

@app.route('/razzia909/info')
def info():
    page = pages.get_or_404('info')
    catList = Liste_cat()
    return render_template('staticpage.html', page=page , catList=catList)



@app.route('/razzia909/cat/<catname>')
def catPage(catname):
    articles = (p for p in pages if 'published' in p.meta and 'cat' in p.meta and p.meta['cat']==catname )
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    catList = Liste_cat()
    return render_template('uindex.html', articles=latest , catList=catList  )


@app.route('/razzia909/pages/<path:path>')
def serve_pages(path):
    return send_from_directory('pages', path) #le navigateur ne demande pas l'image au dossier mais à l'appli, donc au serveur. qui lui accepte etc....
#grave rien à changer ici dans le doute, les changements se font dans le html pour la mise en forme, le js pour les comportements, et css pour la gueule du truc.


@app.route('/skool')
def school():
    articles = (p for p in DNpages if 'published' in p.meta)
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    catList = Liste_cat()
    return render_template('school.html', menu='menu.html') # Ajout du paramètre 'menu' avec la valeur 'menuschool.html'


@app.route('/dechetsnation')
def d_nation():
    articles = (p for p in DNpages if 'published' in p.meta)
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    catList = Liste_cat()
    return render_template('dn.html', menu='menu.html') # Ajout du paramètre 'menu' avec la valeur 'menu.html'




@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return "erreur 303!!! ✜✜✜" \
           

if __name__ == "__main__":
    app.run(host='0.0.0.0')




