const svSetBtns = document.querySelectorAll('.pokemon-sets .box');

svSetBtns.forEach(btn => {
	btn.onclick = (event) => {
		svSetBtns.forEach(btn => {
			btn.classList.remove('active');
		});

		let svSet = event.currentTarget.getAttribute("data-sv-set");
		fetch(`/open-pack?sv-set=${svSet}`)
			.then(response => response.json())
			.then(pack_cards => {
				let nonHoloSlots = document.querySelectorAll('.non-holo-cards .box');
				let holoSlots = document.querySelectorAll('.holo-cards .box');

				nonHoloSlots.forEach((slot, index) => {
					let oldCardImg = slot.querySelector('.card-img');
					let newCardImg = document.createElement('img');
					let oldCardValue = slot.querySelector('p');
					let newCardValue = document.createElement('p');

					newCardImg.src = pack_cards.non_holos[index].images.large;
					newCardImg.className = `card-img fadein-${index+1} enlarge-on-hover`;
					oldCardImg.replaceWith(newCardImg);

					newCardValue.className = 'card-value fadeup-2';
					newCardValue.innerHTML = '$' + parseFloat(pack_cards.non_holos[index].tcgplayer.prices.normal.market).toFixed(2);
					oldCardValue.replaceWith(newCardValue);
				});

				holoSlots.forEach((slot, index) => {
					let oldCardImg = slot.querySelector('.card-img');
					let newCardImg = document.createElement('img');
					let oldCardValue = slot.querySelector('p');
					let newCardValue = document.createElement('p');

					newCardImg.src = pack_cards.holos[index].images.large;
					newCardImg.className = 'card-img cursor-pointer';
					oldCardImg.replaceWith(newCardImg);

					newCardValue.className = 'card-value';
					if (['Common', 'Uncommon', 'Rare'].includes(pack_cards.holos[index].rarity) && index < 2) {
						newCardValue.innerHTML = '$' + parseFloat(pack_cards.holos[index].tcgplayer.prices.reverseHolofoil.market).toFixed(2);
					} else {
						newCardValue.innerHTML  = '$' + parseFloat(pack_cards.holos[index].tcgplayer.prices.holofoil.market).toFixed(2);
					};
					oldCardValue.replaceWith(newCardValue);

					newCardImg.onclick = (event) => {
						newCardImg.classList.replace('cursor-pointer', 'fadein-1');
						newCardImg.classList.add('enlarge-on-hover');
						newCardValue.classList.add('fadeup-1');

						newCardImg.onclick = null;
					};
				});
			})
			.catch(error => console.error('Error:', error));

		event.currentTarget.classList.add('active');
	};
});

const refreshBtn = document.querySelector('.refresh-btn a')

refreshBtn.onclick = (event) => {
	refreshBtn.querySelector('.icon').classList.add('rotate360');
	refreshBtn.style.pointerEvents = "none";

	svSetBtns.forEach(btn => {
		btn.style.pointerEvents = "none";
	});
};
