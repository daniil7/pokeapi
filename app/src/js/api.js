window.PAGINATION_COUNT = 0;

export default class API
{
    static async retrievePokemons() {
        return await (await fetch('/api/pokemon')).json();
    }
    static async retrieveSprite(pokemon_name) {
        return await (await fetch('/api/pokemon-sprite/'+pokemon_name)).text();
    }
}
