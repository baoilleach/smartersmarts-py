import os
import sys
import argparse

import bottle
import showmatches

mainhtml = open("smartsrefine.html").read()
URLPREFIX = "/smartsrefine"

@bottle.get("/")
def redirect_to_index():
    """This will only ever be accessed when developing locally"""
    bottle.redirect(PREFIX)

@bottle.get(PREFIX)
def index():
    # Do not cache
    bottle.response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
    bottle.response.set_header('Pragma', 'no-cache')
    bottle.response.set_header('Expires', '0')
    return mainhtml

@bottle.get('/smartsrefine_static/js/<filename:re:.*\.js>')
def javascripts(filename):
    return bottle.static_file(filename, root='static/js')
@bottle.get('/smartsrefine_static/ext/js/<filename:re:.*\.js>')
def javascripts_ext(filename):
    return bottle.static_file(filename, root='static/ext/js')
@bottle.get('/smartsrefine_static/ext/fonts/<filename:re:.*\.(woff2|woff|ttf)>')
def javascripts_ext(filename):
    return bottle.static_file(filename, root='static/ext/fonts')
@bottle.get('/smartsrefine_static/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return bottle.static_file(filename, root="static/css")
@bottle.get('/smartsrefine_static/ext/css/<filename:re:.*\.css>')
def stylesheets_ext(filename):
    return bottle.static_file(filename, root="static/ext/css")
@bottle.get('/smartsrefine_static/imgs/<filename:re:.*\.(png|gif|ico)>')
def imgs(filename):
    return bottle.static_file(filename, root="static/imgs")
@bottle.get('/smartsrefine_static/ext/imgs/jquery-ui-1.10.3/<filename:re:.*\.png>')
def imgs_jquery_ui(filename):
    return bottle.static_file(filename, root="static/ext/imgs/jquery-ui-1.10.3")

@bottle.route('%s/search' % URLPREFIX, method="Get")
def search():
    alldata = bottle.request.GET
    smarts = alldata.get('smarts')
    print("Searching for smarts: '%s'" % smarts)
    smiles = showmatches.FindMatches(smarts)
    if smiles == -1:
        return {"valid": False}
    ans = {"valid": True, "matches": smiles}
    bottle.response.set_header('Cache-Control', 'public,max-age=3600')
    return ans

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="Specify the port")
    args = parser.parse_args()

    app = bottle.app()
    bottle.run(app=app, server="paste", port=args.port, host="0.0.0.0")
