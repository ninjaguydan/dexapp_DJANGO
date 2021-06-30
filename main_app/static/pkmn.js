var dexid = $('forjs').attr("id");
console.log(dexid);

$.get("https://pokeapi.co/api/v2/pokemon/" + dexid + "/", function(pkmn) {
        var html_str = "";
        for(var i = 0; i < pkmn.types.length; i++) {
            html_str += "<span class='type " + pkmn.types[i].type.name + "'>" + pkmn.types[i].type.name + "</span>\n";
        }
        $('.types').append(html_str);
}, "json");