for (let i = 1; i <= 251; i++) {
    $.get("https://pokeapi.co/api/v2/pokemon/" + i, function(pkmn){
        console.log(i);
        console.log(pkmn.id);
        let html_str = "";
        html_str += "<a href='/pkmn/" + pkmn.id + "'>";
        html_str += "<div class='card'>";
        html_str += "<h3>#"+ pkmn.id +"</h3>";
        html_str += "<img src='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/" + i + ".png'>";
        html_str += "<h2>"+ pkmn.name +"</h2>";
        html_str += "</div>";
        html_str += "</a>";
        $('.card-grid').append(html_str);
    })
}
