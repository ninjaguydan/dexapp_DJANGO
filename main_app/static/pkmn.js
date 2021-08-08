//Display Star Rating
function displayRating(num){
    var result = "";
    for (var i = 1; i < 11; i++) {
        if (i <= num) {
            result = result + "&#x2605"
        } else {
            result = result  + "&#x2606";
        }
    }
    return result
}
$('.n1').html(displayRating(1));
$('.n2').html(displayRating(2));
$('.n3').html(displayRating(3));
$('.n4').html(displayRating(4));
$('.n5').html(displayRating(5));
$('.n6').html(displayRating(6));
$('.n7').html(displayRating(7));
$('.n8').html(displayRating(8));
$('.n9').html(displayRating(9));
$('.n10').html(displayRating(10));