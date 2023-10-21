window.PAGINATION_COUNT = 0;

export default class API
{
    static async retrievePokemons()
    {
        return await (await fetch('/api/pokemon')).json();
    }
    static async retrievePokemon(pokemon_name)
    {
        return await (await fetch('/api/pokemon/'+pokemon_name)).json();
    }
    static async sendBattleResult(battle_result_array)
    {
        return await fetch("/api/battle/write-result", {
          method: "POST",
          body: JSON.stringify(battle_result_array),
          headers: {
              "Content-type": "application/json; charset=UTF-8"
          }
        });
    }
    static async sendSavePokemonToFTPRequest(pokemon_name)
    {
        return await fetch("/api/ftp/save-pokemon", {
          method: "POST",
          body: pokemon_name,
          headers: {
              "Content-type": "text/plain; charset=UTF-8"
          }
        });
    }
}
