var errors = {
    "fname" : "error",
    "lname" : "error",
    "username" : "error",
    "email" : "error",
    "password" : "error",
    "confirm" : "error",
}
//validation function
function validate_length(class_name, min, max) {
    $('form').on('keyup', '.'+ class_name , function(){
        let temp = $(this).children('input').val()
        if ( temp.length < min ) {
            $(this).children('.error2').show();
            errors[class_name] = "name too short"
            $(this).children('i').hide()
        } 
        else if (temp.length > max) {
            $(this).children('.error').show();
            errors[class_name] = "name too long"
            $(this).children('i').hide()
        } else {
            $(this).children('small').hide();
            $(this).children('i').show()
            delete errors[class_name]
        }
        check_button()
    })
}
//activate button
function check_button(){
    if ( $.isEmptyObject(errors) ) {
        $('button').prop("disabled", false)
    } else {
        $('button').prop("disabled", true)
    }
}
//first name validation
validate_length('fname', 2, 25)

//last name validation
validate_length('lname', 2, 25)

//Username validation
validate_length('username', 6, 13)

//Email validation
function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  }
$('form').on('keyup', '.email', function(){
    let email = $(this).children('input').val()
    if ( !validateEmail(email) ) {
        $(this).children('.error').show();
        errors['email'] = "invalid"
        $(this).children('i').hide()
    } else {
        $(this).children('small').hide();
        $(this).children('i').show()
        delete errors['email']
    }
    check_button()
})
//Password validation
validate_length('password', 8, 16)

//Confirmation validation
$('form').on('keyup', '.confirm-pw', function(){
    let pw = $('.pw').val();
    let confirm = $('.confirm').val();
    if ( pw != confirm ) {
        $(this).children('.error').show()
        errors['confirm'] = "dont match"
        $(this).children('i').hide()
    } else {
        $(this).children('small').hide();
        $(this).children('i').show()
        delete errors['confirm']
    }
    check_button()
})

