Open Pokemon Packs!
===================

Intro
-----
As Pokemon card collectors, it's usually more economical to simply buy the singles we're looking for instead of ripping packs. But ripping packs also tends to be more fun - The element of surprise and pulling that big chase card! So I created this simple app to simulate that dopamine inducing experience without having to actually buy expensive packs!

The App / Usage
---------------
![sample-app-page](https://github.com/jeremyngcode/Open-PTCG-Packs/assets/156220343/957247aa-00f9-4ceb-9314-346a6a8acb14)

Simply run [app.py](app.py) and click on the set you'd like to open!

Below the set logo is the per pack average value. This is the average amount you can expect to get back if you sold all 10 cards at market value.

Once you've selected the desired set to open, the first 7 cards will be revealed instantly. The last 3 cards enclosed in the orange box will only reveal on click to provide a little more suspense since these are the slots the chase cards will be appearing in!

For card data, the API I used is from https://pokemontcg.io. To fetch the latest data / market prices, click on the refresh button at the bottom right corner.

For pull rates which is needed for both pack composition and calculating the per pack average value, I used the data provided by TCGplayer. Example data for Scarlet & Violet 151 pull rates can be found [here](https://infinite.tcgplayer.com/article/Pok%C3%A9mon-TCG-Scarlet-Violet%E2%80%94151-Pull-Rates/b237df74-fbb0-40d0-9e13-d69ee6e804d9/).

At the moment, the API has insufficient data for Prismatic Evolutions and TCGplayer seems to have no pull rate data for Shrouded Fable. So for now, selecting these two sets will not work.

#### Notable libraries used for this project:
- [Flask](https://pypi.org/project/Flask/)
- [Jinja](https://pypi.org/project/Jinja2/)
- [requests](https://pypi.org/project/requests/)
