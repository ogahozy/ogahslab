from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db,storage
from . import main
from app.main.forms import EditProfileForm, PostForm,\
    EditProfileAdminForm, CommentForm,SearchForm
    #,MessageForm
from app.models import User, Post, Role, Permission, Comment
#from flask_cloudy import Storage
#,Message,Notification
from app.translate import translate
from app.decorators import admin_required, permission_required
#storage =Storage()

@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.search_form = SearchForm()
    g.locale = str(get_locale())


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/services', methods=['GET', 'POST'])
def services():
    return render_template('services.html')


@main.route('/blog', methods=['GET', 'POST'])
def blog():
    page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.blog', page=post.next_num) \
        if post.has_next else None
    prev_url = url_for('main.blog', page=post.prev_num) \
        if post.has_prev else None
    posts = post.items
    return render_template('blog.html', title=_('Blog'), posts=posts,
                           next_url=next_url, prev_url=prev_url)


@main.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post( body=form.post.data, title=form.title.data,
                    language=language,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.blog'))
    return render_template('create.html', title=_('Create'), form=form)


@main.route('/blog/<slug>/', methods=['GET', 'POST'])
def detail(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    form1 = CommentForm()
    if form1.validate_on_submit():
        comm = Comment(body=form1.body.data, post=post, author=current_user._get_current_object())
        db.session.add(comm)
        db.session.commit()
        flash('Your comment  has been published')
        return redirect(url_for('main.detail', slug=post.slug, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page  = (post.comments.count() - 1) // current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(page, 
					current_app.config['COMMENTS_PER_PAGE'],False)
    comments = pagination.items
    next_url = url_for('main.detail', slug=slug,page=pagination.next_num)if pagination.has_next else None
    prev_url = url_for('main.detail', slug=slug,page=pagination.prev_num)if pagination.has_prev else None
    return render_template('detail.html',post=post, form1=form1,comments=comments,
                           pagination=pagination,next_url=next_url, prev_url=prev_url)


@main.route('/blog/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.post.data
        post.title = form.title.data
        db.session.commit()
        flash(_('Your post has being edited successfully!'))
        return redirect(url_for('main.edit', slug=post.slug))
    elif request.method == 'GET':
        form.post.data = post.body
        form.title.data = post.title
    return render_template( 'edit.html', form=form )

@main.route("/store")
@login_required
@admin_required
def store():
    return render_template("storage.html", storage=storage)

@main.route("/view/<path:object_name>")
@login_required
@admin_required
def view(object_name):
    obj = storage.get(object_name)
    print (obj.name)
    return render_template("view.html", obj=obj)

@main.route("/upload", methods=["POST"])
@login_required
@admin_required
def upload():
    file = request.files.get("file")
    my_object = storage.upload(file)
    return redirect(url_for("view", object_name=my_object.name))


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
			page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@main.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)



@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.user', username=current_user.username))
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)



@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('main.user', username=username))


@main.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})

@main.route('/moderate/')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, 
                          current_app.config['COMMENTS_PER_PAGE'],False)
    comments = pagination.items
    return render_template('moderate.html',
			comments=comments,pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 0, type=int)))

@main.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)


#@main.route('/send_message/<recipient>', methods=['GET', 'POST'])
#@login_required
#def send_message(recipient):
 #   user = User.query.filter_by(username=recipient).first_or_404()
  #  form = MessageForm()
   # if form.validate_on_submit():
    #    msg = Message(author=current_user, recipient=user,
     #                 body=form.message.data)
      #  db.session.add(msg)
       # user.add_notification('unread_message_count', user.new_messages())
        #db.session.commit()
        #flash(_('Your message has been sent.'))
        #return redirect(url_for('main.user', username=recipient))
    #return render_template('send_message.html', title=_('Send Message'),
     #                      form=form, recipient=recipient)


"""
@main.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@main.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

"""