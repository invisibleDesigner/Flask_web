from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
from routes import (
    current_user,
    login_required,
    admin_required,
    csrf_token_required,
)
from models.topic import Topic
from models.board import Board
from models.csrf import Csrf
from utils import log


main = Blueprint('py_topic', __name__, static_folder='static')


@main.route("/")
@login_required
def index(u):
    boards = Board.all()
    if request.args.get('board_id') is None:
        topics = Topic.all()
    else:
        topics = Topic.all(board_id=request.args['board_id'])
    Csrf.generate_csrf()
    csrf_token = Csrf.get_csrf()
    log('====csrf_token====\n{}'.format(csrf_token))
    return render_template("topic/index.html", topics=topics, boards=boards, user=u, csrf_token=csrf_token)


@main.route('/<int:id>')
def detail(id):
    topic = Topic.get(id)
    return render_template("topic/detail.html", topic=topic)


@main.route("/add", methods=["POST"])
@csrf_token_required
def add():
    form = request.form.to_dict()
    form['views'] = 0
    u = current_user()
    m = Topic.add(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/new")
def new():
    csrf_token = Csrf.get_csrf()
    boards = Board.all()
    return render_template("topic/new.html", boards=boards, csrf_token=csrf_token)


@main.route("/board/add", methods=["POST"])
def add_board():
    form = request.form.to_dict()
    Board.new(form=form)
    return redirect(url_for('py_topic.index'))


@main.route("/board/view")
@admin_required
def view_board():
    return render_template('topic/board.html', )
