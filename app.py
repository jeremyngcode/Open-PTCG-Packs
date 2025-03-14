import os, json, random, time, webbrowser, pprint
import requests
from flask import (
	Flask, render_template, redirect, url_for,
	request, jsonify
)

from functions import *
# -------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_pyfile("config.py")

EXCLUDED_SETS = app.config['EXCLUDED_SETS']

PKMN_SV_SETS = os.path.join(app.root_path, app.config['PKMN_SV_SETS'])
PKMN_CARDS_DATA = os.path.join(app.root_path, app.config['PKMN_CARDS_DATA'])

# -------------------------------------------------------------------------------------------------
@app.route("/")
def home():
	if not os.path.exists(PKMN_CARDS_DATA):
		session = requests.Session()
		cards_url = "https://api.pokemontcg.io/v2/cards"

		with open(PKMN_SV_SETS) as f:
			SV_SETS = json.load(f)

		for sv_set in EXCLUDED_SETS:
			del SV_SETS[sv_set]

		for sv_set, sv_set_data in SV_SETS.items():
			print(f'RETRIEVING DATA FOR {sv_set_data["name"].upper()}..')
			print()

			cards = {
				'C': [],
				'U': [],
				'R': [],
				'rh': [],

				'DR': [],
				'UR': [],

				'IR': [],
				'SIR': [],
				'HR': [],

				'ACE': [],
				'SR': [],
				'SUR': [],

				'avg_pack_value': None
			}

			params = {
				'q': f'!set.name:"{sv_set_data['name']}"',
				'select': 'id,number,name,images,rarity,tcgplayer',
				'page': 1,
				'orderBy': 'number'
			}

			while True:
				r = session.get(cards_url, params=params)
				sv_cards_data = r.json()

				for card in sv_cards_data['data']:
					if card['rarity'] == 'Common':
						cards['C'].append(card)
					elif card['rarity'] == 'Uncommon':
						cards['U'].append(card)
					elif card['rarity'] == 'Rare':
						cards['R'].append(card)

					elif card['rarity'] == 'Double Rare':
						cards['DR'].append(card)
					elif card['rarity'] == 'Ultra Rare':
						cards['UR'].append(card)

					elif card['rarity'] == 'Illustration Rare':
						cards['IR'].append(card)
					elif card['rarity'] == 'Special Illustration Rare':
						cards['SIR'].append(card)
					elif card['rarity'] == 'Hyper Rare':
						cards['HR'].append(card)

					elif card['rarity'] == 'ACE SPEC Rare':
						cards['ACE'].append(card)
					elif card['rarity'] == 'Shiny Rare':
						cards['SR'].append(card)
					elif card['rarity'] == 'Shiny Ultra Rare':
						cards['SUR'].append(card)

					if card['rarity'] in ('Common', 'Uncommon', 'Rare'):
						cards['rh'].append(card)

				if sv_cards_data['count'] < sv_cards_data['pageSize']:
					break
				params['page'] += 1

			non_holos_avg_value = get_non_holos_avg_value(cards['C'], cards['U'])

			slot8_avg_value = get_slot8_avg_value(
				cards['ACE'], cards['SR'], cards['SUR'], cards['rh'], sv_set_data['pull_rates']
			)
			slot9_avg_value = get_slot9_avg_value(
				cards['IR'], cards['SIR'], cards['HR'], cards['rh'], sv_set_data['pull_rates']
			)
			slot10_avg_value = get_slot10_avg_value(
				cards['R'], cards['DR'], cards['UR'], sv_set_data['pull_rates']
			)

			cards['avg_pack_value'] = round(
				non_holos_avg_value +
				slot8_avg_value +
				slot9_avg_value +
				slot10_avg_value, 2
			)

			print('=' * 50)
			print(f'{sv_set_data["name"]} Average Pack Value: ${cards["avg_pack_value"]:.2f}')
			print('=' * 50)
			print()

			SV_SETS[sv_set]['cards'] = cards

		SV_SETS['last_updated'] = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime())

		with open(PKMN_CARDS_DATA, 'w') as f:
			json.dump(SV_SETS, f, indent=4)

	with open(PKMN_CARDS_DATA) as f:
		sv_cards_data = json.load(f)

	last_updated = sv_cards_data['last_updated']
	sv_cards_data = dict(list(sv_cards_data.items())[:-1])

	sv_pack_values = {
		sv_set: f'{sv_set_data['cards']['avg_pack_value']:.2f}'
		for sv_set, sv_set_data in sv_cards_data.items()
	}

	return render_template("home.html.j2", **sv_pack_values, last_updated=last_updated)

@app.route("/open-pack")
def open_pack():
	with open(PKMN_CARDS_DATA) as f:
		sv_cards_data = json.load(f)

	sv_set = request.args.get('sv-set')
	sv_set = sv_cards_data[sv_set]

	pull_rates = sv_set['pull_rates']
	set_cards = sv_set['cards']

	# non holos (card slots 1-7)
	C_cards = random.choices(set_cards['C'], k=4)
	U_cards = random.choices(set_cards['U'], k=3)

	slot8_card = random.choice(set_cards['C'] + set_cards['U'] + set_cards['R'])
	slot9_card = random.choice(set_cards['C'] + set_cards['U'] + set_cards['R'])
	slot10_card = random.choice(set_cards['R'])

	# card slot 8
	if pull_rates['ACE'] > 0:
		rh_pull_rate = 1 - pull_rates['ACE']

		selected_card_type = random.choices(
			('ACE', 'rh'), weights=[pull_rates['ACE'], rh_pull_rate], k=1
		)[0]
		if selected_card_type == 'ACE':
			slot8_card = random.choice(set_cards[selected_card_type])

	elif pull_rates['SR'] > 0:
		rh_pull_rate = 1 - (pull_rates['SR'] + pull_rates['SUR'])

		selected_card_type = random.choices(
			('SR', 'SUR', 'rh'), weights=[pull_rates['SR'], pull_rates['SUR'], rh_pull_rate], k=1
		)[0]
		if selected_card_type in ('SR', 'SUR'):
			slot8_card = random.choice(set_cards[selected_card_type])

	# card slot 9
	rh_pull_rate = 1 - (pull_rates['IR'] + pull_rates['SIR'] + pull_rates['HR'])

	selected_card_type = random.choices(
		('IR', 'SIR', 'HR', 'rh'), weights=[pull_rates['IR'], pull_rates['SIR'], pull_rates['HR'], rh_pull_rate], k=1
	)[0]
	if selected_card_type in ('IR', 'SIR', 'HR'):
		slot9_card = random.choice(set_cards[selected_card_type])

	# card slot 10
	rh_pull_rate = 1 - (pull_rates['DR'] + pull_rates['UR'])

	selected_card_type = random.choices(
		('DR', 'UR', 'rh'), weights=[pull_rates['DR'], pull_rates['UR'], rh_pull_rate], k=1
	)[0]
	if selected_card_type in ('DR', 'UR'):
		slot10_card = random.choice(set_cards[selected_card_type])

	# all cards
	pack_cards = {
		'non_holos': C_cards + U_cards,
		'holos': [slot8_card, slot9_card, slot10_card]
	}
	print('---PACK CARDS---')
	pprint.pprint(pack_cards, sort_dicts=False)

	return jsonify(pack_cards)

@app.route("/refresh")
def refresh_data():
	os.remove(PKMN_CARDS_DATA)

	return redirect(url_for('home'))

# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	webbrowser.open(f"http://{app.config['HOST']}:{app.config['PORT']}")
	app.run(
		host=app.config['HOST'],
		port=app.config['PORT']
	)
