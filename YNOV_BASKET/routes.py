from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from YNOV_BASKET.models import User, Player, Team, Match
from YNOV_BASKET.forms import RegistrationForm, LoginForm
from YNOV_BASKET import db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('routes', __name__)

@bp.route('/')
@login_required
def index():
    return redirect(url_for('routes.joueurs'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        print(f"Utilisateur créé : {user.username}, {user.email}")
        
        login_user(user)
        return redirect(url_for('routes.index'))
    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(f"Tentative de connexion pour l'email : {form.email.data}")
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print(f"Utilisateur trouvé : {user.username}, {user.email}")
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('routes.index'))
            else:
                print("Mot de passe incorrect")
        else:
            print("Utilisateur non trouvé")
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

@bp.route('/joueurs')
@login_required
def joueurs():
    players = Player.query.all()
    return render_template('joueurs.html', players=players)

@bp.route('/joueur/<int:player_id>')
@login_required
def joueur(player_id):
    player = Player.query.get_or_404(player_id)
    return render_template('joueur.html', player=player)

@bp.route('/equipes')
@login_required
def equipes():
    teams = Team.query.all()
    return render_template('equipes.html', teams=teams)

@bp.route('/equipe/<int:team_id>')
@login_required
def equipe(team_id):
    team = Team.query.get_or_404(team_id)
    players = Player.query.filter_by(team_id=team_id).all()
    return render_template('equipe.html', team=team, players=players)

@bp.route('/matchs')
@login_required
def matchs():
    matchs = Match.query.all()
    return render_template('matchs.html', matchs=matchs)

@bp.route('/match/<int:match_id>')
@login_required
def match(match_id):
    match = Match.query.get_or_404(match_id)
    home_team = Team.query.get_or_404(match.home_team_id)
    visitor_team = Team.query.get_or_404(match.visitor_team_id)
    return render_template('match.html', match=match, home_team=home_team, visitor_team=visitor_team)
