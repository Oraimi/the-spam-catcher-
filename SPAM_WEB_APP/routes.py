import os
import time
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from SPAM_WEB_APP import app, db, bcrypt, mail
from SPAM_WEB_APP.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                PostForm, PostForm2,RequestResetForm, ResetPasswordForm, ScanByUploadForm)
from SPAM_WEB_APP.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import warnings
import nltk
import string
from nltk.corpus import stopwords
import pickle
import zipfile
import glob

nltk.download('stopwords')
warnings.filterwarnings("ignore")


def mapper(txt):
  return [word for word in ''.join([char for char in txt if char not in string.punctuation]).split() if word.lower() not in stopwords.words('english')]


def token_maker(inn):
    keeper = pickle.load(open('./SPAM_WEB_APP/DICT.pk', 'rb'))
    data = [0]*len(keeper)
    for i in mapper(inn):
        try:
            data[keeper.index(i)] += 1
        except ValueError:
            pass
    return [data]


def models_loader(email):
    gaussian_naive_bayes_value = pickle.load(open('./SPAM_WEB_APP/MODEL.pk', 'rb'))
    ins = token_maker(email)

    results = {
        'GUS': gaussian_naive_bayes_value.predict(ins)[0],
    }

    if results.get('GUS') >= 0.51:
        results['SPAM'] = 'A SPAM'
    else:
        results['SPAM'] = 'NOT A SPAM'

    return results


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        results = models_loader(form.content.data)

        gaussian_naive_bayes_value = results['GUS']
        spam_or_ham = results['SPAM']

        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    gaussian_naive_bayes_value=gaussian_naive_bayes_value,
                    spam_or_ham=spam_or_ham)
        db.session.add(post)
        db.session.commit()
        flash('Your Scan has been completed!', 'success')
        return redirect(url_for('my_scans'))
    return render_template('new_scan.html', title='New Scan',
                           form=form, legend='New Scan')


@app.route('/post/new/hscan', methods=['GET', 'POST'])
@login_required
def hscan():
    form = PostForm2()
    if form.validate_on_submit():
        results = models_loader(form.content.data)

        gaussian_naive_bayes_value = results['GUS']
        spam_or_ham = results['SPAM']

        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    gaussian_naive_bayes_value=gaussian_naive_bayes_value,
                    spam_or_ham=spam_or_ham)
        db.session.add(post)
        db.session.commit()
        flash('Your Scan has been completed!', 'success')
        return redirect(url_for('my_scans'))
    return render_template("hscan.html",title="email header scan", form=form,legend="email header scan")

@app.route('/post/new/getfile', methods=['GET', 'POST'])
@login_required
def getfile():
    if request.method == 'POST':
        try:
            file = request.files['myfile']
            NAME = file.filename
            path = os.path.join(app.root_path, 'static//data', NAME)
            file.save(path)
            if file.filename.split('.')[-1] == 'zip':
                PATH = path.split('.')[0]
                try:
                    os.mkdir(PATH)
                except FileExistsError:
                    PATH = PATH+str(time.time())
                    os.mkdir(PATH)
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    zip_ref.extractall(PATH)
                data = str()
                gus_dir = list()
                for dirs in [os.path.join(PATH, o) for o in os.listdir(PATH)]:
                    for file in glob.glob(dirs+'/*'):
                        reads = open(file, 'r').read()
                        results = models_loader(reads)
                        gus_dir.append(results['GUS'])
                        data = data + file.split('//')[-1] + ' GNB :' + str(results['GUS']) + ' STATUS :' + results['SPAM'] + '\n'
                message = 'NOT SPAM'
                pops = sum(gus_dir)/len(gus_dir)
                if pops >= 0.45:
                    message = 'A SPAM'
                scan_by_file = Post(title="File Scan " + NAME,
                                    content=data,
                                    author=current_user,
                                    gaussian_naive_bayes_value=pops,
                                    spam_or_ham=message)
                db.session.add(scan_by_file)
                db.session.commit()
                flash('Your scan has been completed!', 'success')
                return redirect(url_for('my_scans'))
            else:
                with open(path, 'r') as f:
                    file_content = f.read()
                results = models_loader(file_content)
                gaussian_naive_bayes_value = results['GUS']
                spam_or_ham = results['SPAM']
                scan_by_file = Post(title="Archive Scan "+NAME,
                                    content=file_content,
                                    author=current_user,
                                    gaussian_naive_bayes_value=gaussian_naive_bayes_value,
                                    spam_or_ham=spam_or_ham)
                db.session.add(scan_by_file)
                db.session.commit()
                flash('Your Scan has been completed!', 'success')
                return redirect(url_for('my_scans'))
        except FileNotFoundError:
            flash('Upload a file')
            return render_template('uploadfile.html', title="Upload file(s) for scan")
    if request.method == 'GET':
        return render_template('uploadfile.html', title="Upload file(s) for scan")
    flash('Something went Wrong')
    return render_template('uploadfile.html', title="Upload file(s) for scan")


@app.route('/post/myscans')
@login_required
def my_scans():
    username = current_user.username
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('scan.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        results = models_loader(form.content.data)
        gaussian_naive_bayes_value = results['GUS']
        spam_or_ham = results['SPAM']
        post.title = form.title.data
        post.content = form.content.data
        post.spam_or_ham = spam_or_ham
        post.gaussian_naive_bayes_value = gaussian_naive_bayes_value
        db.session.commit()
        flash('Your Scan has been rescanned!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_scan.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your scan has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='thespamc@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
                {url_for('reset_token', token=token, _external=True)}
                If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
