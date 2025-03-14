def get_non_holos_avg_value(C_cards, U_cards):
	C_card_values, C_card_slots = [], 4
	U_card_values, U_card_slots = [], 3

	for cards, card_values in ((C_cards, C_card_values), (U_cards, U_card_values)):
		for card in cards:
			try:
				card_values.append(card['tcgplayer']['prices']['normal']['market'])
			except KeyError:
				print(f'Failed to fetch price data for card id {card["id"]} ({card["name"]})')

	C_cards_avg_value = (sum(C_card_values) / len(C_card_values)) * C_card_slots
	U_cards_avg_value = (sum(U_card_values) / len(U_card_values)) * U_card_slots

	non_holos_avg_value = C_cards_avg_value + U_cards_avg_value

	print(f'Average Value of Common cards (Slots 1-4): ${C_cards_avg_value:.2f}')
	print(f'Average Value of Uncommon cards (Slots 5-7): ${U_cards_avg_value:.2f}')
	print()

	return non_holos_avg_value

def get_slot8_avg_value(ACE_cards, SR_cards, SUR_cards, rh_cards, pull_rates):
	if len(ACE_cards) == 0:
		ACE_card_avg_value, pull_rates['ACE'] = 0, 0
	else:
		ACE_card_values = []

		for card in ACE_cards:
			try:
				ACE_card_values.append(card['tcgplayer']['prices']['holofoil']['market'])
			except KeyError:
				print(f'Failed to fetch price data for card id {card["id"]} ({card["name"]})')

		ACE_card_avg_value = sum(ACE_card_values) / len(ACE_card_values)

	if len(SR_cards) == 0:
		SR_card_avg_value, pull_rates['SR'] = 0, 0
		SUR_card_avg_value, pull_rates['SUR'] = 0, 0
	else:
		SR_card_values = []
		SUR_card_values = []

		for cards, card_values in ((SR_cards, SR_card_values), (SUR_cards, SUR_card_values)):
			for card in cards:
				try:
					card_values.append(card['tcgplayer']['prices']['holofoil']['market'])
				except KeyError:
					print(f'Failed to fetch price data for card id {card["id"]} ({card["name"]})')

		SR_card_avg_value = sum(SR_card_values) / len(SR_card_values)
		SUR_card_avg_value = sum(SUR_card_values) / len(SUR_card_values)

	rh_card_values = []

	for card in rh_cards:
		try:
			rh_card_values.append(card['tcgplayer']['prices']['reverseHolofoil']['market'])
		except KeyError:
			print(f'Failed to fetch price data for card id {card["id"]} ({card["name"]})')

	rh_card_avg_value = sum(rh_card_values) / len(rh_card_values)
	rh_card_pull_rate = 1 - (pull_rates['ACE'] + pull_rates['SR'] + pull_rates['SUR'])

	slot8_avg_value = (
		ACE_card_avg_value * pull_rates['ACE'] +
		SR_card_avg_value * pull_rates['SR'] +
		SUR_card_avg_value * pull_rates['SUR'] +
		rh_card_avg_value * rh_card_pull_rate
	)

	if ACE_cards:
		print(
			f'Average value of all ACE cards: ${ACE_card_avg_value:.2f} '
			f'[Pull Rate: {pull_rates["ACE"] * 100:.2f}%]'
		)
	if SR_cards:
		print(
			f'Average value of all SR cards: ${SR_card_avg_value:.2f} '
			f'[Pull Rate: {pull_rates["SR"] * 100:.2f}%]'
		)
		print(
			f'Average value of all SUR cards: ${SUR_card_avg_value:.2f} '
			f'[Pull Rate: {pull_rates["SUR"] * 100:.2f}%]'
		)
	print(
		f'Average value of all rh cards: ${rh_card_avg_value:.2f} '
		f'[Pull Rate: {rh_card_pull_rate * 100:.2f}%]'
	)
	print('-' * 50)
	print(f'Average Value of Slot 8 card: ${slot8_avg_value:.2f}')
	print()

	return slot8_avg_value

def get_slot9_avg_value(IR_cards, SIR_cards, HR_cards, rh_cards, pull_rates):
	IR_card_values = []
	SIR_card_values = []
	HR_card_values = []

	for cards, card_values in ((IR_cards, IR_card_values), (SIR_cards, SIR_card_values), (HR_cards, HR_card_values)):
		for card in cards:
			try:
				card_values.append(card['tcgplayer']['prices']['holofoil']['market'])
			except KeyError:
				print(f'Failed to fetch price data for card id {card["id"]} ({card["name"]})')

	IR_card_avg_value = sum(IR_card_values) / len(IR_card_values)
	SIR_card_avg_value = sum(SIR_card_values) / len(SIR_card_values)
	HR_card_avg_value = sum(HR_card_values) / len(HR_card_values)

	rh_card_values = []

	for card in rh_cards:
		try:
			rh_card_values.append(card['tcgplayer']['prices']['reverseHolofoil']['market'])
		except KeyError:
			print(f'Failed to fetch price data for card id {card["id"]} ({card["name"]})')

	rh_card_avg_value = sum(rh_card_values) / len(rh_card_values)
	rh_card_pull_rate = 1 - (pull_rates['IR'] + pull_rates['SIR'] + pull_rates['HR'])

	slot9_avg_value = (
		IR_card_avg_value * pull_rates['IR'] +
		SIR_card_avg_value * pull_rates['SIR'] +
		HR_card_avg_value * pull_rates['HR'] +
		rh_card_avg_value * rh_card_pull_rate
	)

	print(
		f'Average value of all IR cards: ${IR_card_avg_value:.2f} '
		f'[Pull Rate: {pull_rates["IR"] * 100:.2f}%]'
	)
	print(
		f'Average value of all SIR cards: ${SIR_card_avg_value:.2f} '
		f'[Pull Rate: {pull_rates["SIR"] * 100:.2f}%]'
	)
	print(
		f'Average value of all HR cards: ${HR_card_avg_value:.2f} '
		f'[Pull Rate: {pull_rates["HR"] * 100:.2f}%]'
	)
	print(
		f'Average value of all rh cards: ${rh_card_avg_value:.2f} '
		f'[Pull Rate: {rh_card_pull_rate * 100:.2f}%]'
	)
	print('-' * 50)
	print(f'Average Value of Slot 9 card: ${slot9_avg_value:.2f}')
	print()

	return slot9_avg_value

def get_slot10_avg_value(R_cards, DR_cards, UR_cards, pull_rates):
	R_card_values = []
	DR_card_values = []
	UR_card_values = []

	for cards, card_values in ((R_cards, R_card_values), (DR_cards, DR_card_values), (UR_cards, UR_card_values)):
		for card in cards:
			try:
				card_values.append(card['tcgplayer']['prices']['holofoil']['market'])
			except KeyError:
				print(f'Failed to fetch price data for card id {card["id"]} ({card["name"]})')

	R_card_avg_value = sum(R_card_values) / len(R_card_values)
	R_card_pull_rate = 1 - (pull_rates['DR'] + pull_rates['UR'])

	DR_card_avg_value = sum(DR_card_values) / len(DR_card_values)
	UR_card_avg_value = sum(UR_card_values) / len(UR_card_values)

	slot10_avg_value = (
		R_card_avg_value * R_card_pull_rate +
		DR_card_avg_value * pull_rates['DR'] +
		UR_card_avg_value * pull_rates['UR']
	)

	print(
		f'Average value of all R cards: ${R_card_avg_value:.2f} '
		f'[Pull Rate: {R_card_pull_rate * 100:.2f}%]'
	)
	print(
		f'Average value of all DR cards: ${DR_card_avg_value:.2f} '
		f'[Pull Rate: {pull_rates["DR"] * 100:.2f}%]'
	)
	print(
		f'Average value of all UR cards: ${UR_card_avg_value:.2f} '
		f'[Pull Rate: {pull_rates["UR"] * 100:.2f}%]'
	)
	print('-' * 50)
	print(f'Average Value of Slot 10 card: ${slot10_avg_value:.2f}')
	print()

	return slot10_avg_value
