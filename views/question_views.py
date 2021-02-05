from datetime import datetime

from werkzeug.utils import redirect
from flask import Blueprint, render_template, request, url_for, g, flash

from .. import db
from ..forms import QuestionForm
from ..models import Question, Answer, User
from ..views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')

    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username)\
            .join(User, Answer.user_id == User.id).subquery()

        question_list = question_list\
            .join(User)\
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)\
            .filter(
                Question.subject.ilike(search) |
                Question.content.ilike(search) |
                User.username.ilike(search) |
                sub_query.c.content.ilike(search) |
                sub_query.c.username.ilike(search)
            )\
            .distinct()

    question_list = question_list.paginate(page, per_page=10)
    

    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        # 위와 같은 방식인것 같으나, question_id를 파라미터로 받아 해당 query를 실행하지않기때문에 가져오는 변수가 없으므로 사용 불가능.
        # 실질적으로 로그아웃 상태에서는 질문등록이 버튼이 비활성화되기 때문에 이대로 내비둔것으로 보임.
        #form.populate_obj(question)
        #question.create_date = datetime.now()
        #question.user = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET','POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제할 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))