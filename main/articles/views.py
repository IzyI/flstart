from flask import render_template, request, url_for
from .models import Articles
from flask import current_app as app
from ..articles import article

@article.route('/', defaults={'tag': 'all_articles'}, methods=['GET'])
@article.route('/<string:tag>', methods=['GET'])
def article_index(tag=None):
    if tag == "all_articles" or tag == None:
        t = ""
        page = request.args.get('page', 1, type=int)
        ar = Articles.query.order_by(Articles.date.desc()).paginate(page, 6, False)
        next_url = url_for('article.article_index', page=ar.next_num) if ar.has_next else None
        prev_url = url_for('article.article_index', page=ar.prev_num) if ar.has_prev else None
    else:
        page = request.args.get('page', 1, type=int)
        ar = Articles.query.filter(Articles.tags.any(slug=tag)).order_by(Articles.id.desc()).paginate(page, 6, False)
        next_url = url_for('article.article_index', page=ar.next_num) if ar.has_next else None
        prev_url = url_for('article.article_index', page=ar.prev_num) if ar.has_prev else None
        for i in ar.items[0].tags:
            if i.slug == tag:
                t = "(" + i.name + ")"
                break
    return render_template("articles.html", articles=ar.items, next_url=next_url, prev_url=prev_url,tag_filter=t)

@article.route('/<string:tag>/<string:url>', methods=['GET'])
def article_index_once(tag,url):
    ar =  Articles.query.filter_by(url=url).first()
    return render_template("article_once.html", article=ar,back_path=tag)