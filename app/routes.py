from flask_login import current_user, login_required
from app import app
import requests
from urllib import response


from flask import flash, redirect, render_template, request, url_for

from app.auth.forms import BattleForm, CreateCardForm, PokeForm
from .models import Pokemon, User




@app.route('/')
def land():
    user_list = User.query.all()
    print(user_list)
    return render_template('base.html')

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon_data():
    form = PokeForm()
    if request.method == 'POST':
        if form.validate():
            name = form.poke_name.data
            pokemon = Pokemon.query.filter_by(name=name).first()
            if pokemon:
                print(pokemon)
                return render_template('pokemon.html', form=form, poke=pokemon)
            
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
            if response.ok:
                data = response.json()
                print(data)
                pokemon = {}
                pokemon['name'] = data['forms'][0]['name'] 
                pokemon['ability'] = data['abilities'][0]['ability']['name']
                pokemon['base_exp'] = data['base_experience']
                pokemon['sprite'] = data['sprites']['front_shiny']
                pokemon['attack'] = data['stats'][1]['base_stat']
                pokemon['defense'] = data['stats'][2]['base_stat']
                pokemon['hp'] = data['stats'][0]['base_stat']
                
                new_pokemon = Pokemon(
                    name=pokemon['name'],
                    base_exp=pokemon['base_exp'],
                    ability=pokemon['ability'],
                    sprite=pokemon['sprite'])
                
                new_pokemon.save_pokemon()
                return render_template('pokemon.html', form=form, poke=new_pokemon)
            else:
                flash('Pokemon not found plz try again!', 'danger')
                return redirect(url_for('pokemon_data'))
                
                
    return render_template('pokemon.html',form=form)

@app.route('/card', methods= ['GET', 'POST'])
def create_card():
    form = CreateCardForm()

    return render_template('pokemon', form=form)

@app.route('/info/catch/<int:pokemon_id>', methods=['GET', 'POST'])
@login_required
def my_poke(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    pokes = current_user.caught
    print(pokes)
    if len(pokes) >= 5: 
        flash(f"Your team is full!", 'warning')
        
        return redirect(url_for('pokemon_data'))

    if pokemon in pokes:
        flash(f"You've already caught this Pokemon!", 'warning')
        
        return redirect(url_for('pokemon_data'))
    else:
        pokemon.caught_poke(current_user)
        flash(f"Pokemon added to your team!", 'success')
        return redirect(url_for('pokemon_data'))


@app.route('/info/released/<int:pokemon_id>')
@login_required
def noMore(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    pokes = current_user.caught
    print(pokes)
    if pokemon in pokes:
        pokemon.release_poke(current_user)
        flash(f"I don't want this pokemon anymore", 'danger')
    else:
        flash("You haven't caught this pokemon yet!", 'warning')

    return redirect(url_for('pokemon_data'))


@app.route('/battle_us/<int:pokemon_id1>/<int:pokemon_id2>/', methods=['GET', 'POST'])
@login_required
def battle_Us(pokemon_id1,pokemon_id2):
    pokemon1 = Pokemon.query.get(pokemon_id1)
    pokemon2 = Pokemon.query.get(pokemon_id2)
    
    if pokemon1.base_exp > pokemon2.base_exp:
        winner = pokemon1
        loser = pokemon2
        flash(f"YOU WON!!", 'sucess')
    else:
        winner = pokemon2
        loser = pokemon1
        flash(f"YOU LOST!!", 'warning')

        winner.wins += 1
        loser.losses += 1
    return render_template('battle.html', winner=winner, loser=loser)


@app.route('/battle/', methods=['GET', 'POST'])
@login_required
def battle():
    users = User.query.all()
    form = BattleForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user_id = form.user_id.data
            user = User.query.get(current_user.id)
            
        
        return redirect(url_for('battle'))
    return render_template('battle.html', form=form, users=users)

    
    

    





