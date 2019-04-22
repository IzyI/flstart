from flask import render_template, abort
from main.pages.models import Pages
from ..pages import page

@page.route('/<string:p>', methods=['GET'])
def page(p):
    # try:
    print(p)
    print("!!!")
    page_content=Pages.query.filter_by(url=p).one()
    # if not content:
    #     return abort(404)
    print(page_content,"##")

    return render_template('page.html',
                           page_content=page_content)
