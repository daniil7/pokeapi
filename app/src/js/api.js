window.PAGINATION_COUNT = 0;

export default class API
{
    static async retrievePokemons() {
        return await (await fetch('/api/pokemon')).json();
    }
    static async retrievePokemon(pokemon_name) {
        return await (await fetch('/api/pokemon/'+pokemon_name)).json();
    }
    static async retrieveSprite(pokemon_name) {
        return await (await fetch('/api/pokemon-sprite/'+pokemon_name)).text();
    }
    static async sendBattleResult(battle_result_array) {
        return await fetch("/api/battle/write-result", {
          method: "POST",
          body: JSON.stringify(battle_result_array),
          headers: {
              "Content-type": "application/json; charset=UTF-8"
          }
        });
    }
}
