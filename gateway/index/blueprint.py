from flask import Blueprint, render_template

blueprint = Blueprint('index', __name__, url_prefix='/', template_folder="templates")


@blueprint.route("/")
def index():
    return render_template("login.html")
