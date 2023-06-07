function clearInputForm() {
            $("#login_username").val("");
            $("#login_password").val("");
            $("#email").val("");
            $("#rega_username").val("");
            $("#rega_password").val("");
            $("#confirm_password").val("");
            $(".error_form_registration").text("");
            $("#restore_input").val("");
        }


$(document).ready(function() {
    $("#registration").submit(function(event) {
        event.preventDefault();

        let password = $("#rega_password").val();
        let confirmPassword = $("#confirm_password").val();

        if (password !== confirmPassword) {
            $(".error_form_registration").text("Пароли не совпадают.");
        } else {
            let email = $("#email").val();
            let username = $("#rega_username").val();
            checkUsernameExists(email, username);
        }
    });

    $("#restore_account").submit(function(event) {
        event.preventDefault();

        let email = $("#restore_input").val();
        if (email !== "") {
            checkEmailExists(email);
        }
    });

    $("#login").submit(function(event) {
        event.preventDefault();
        let username = $("#login_username").val();
        let password = $("#login_password").val();
        if (username !== "") {
            checkUserCredentials(username, password);
        }
    });
});

function checkUsernameExists(email, username) {
    $.ajax({
        url: "/profile/check_user_exists/",
        data: {
            email: email,
            username: username
        },
        success: function(response) {
            if (response.email_taken) {
                $(".error_form_registration").text("Пользователь с таким адресом электронной почты уже существует.").css("font-size", "13px").css("color", "red");
            } else if (response.username_taken) {
                $(".error_form_registration").text("Пользователь с таким именем уже существует.").css("font-size", "14px").css("color", "red");
            } else {
                $(".error_form_registration").text("");
                $("#registration").unbind('submit').submit();
            }
        }
    });
}

function checkEmailExists(email) {
    $.ajax({
        url: "/profile/check_email_exists/",
        data: {
            email: email
        },
        success: function(response) {
            if (response.email_taken) {
                $(".error_form_registration").text("Инструкция по восстановлению пароля отправлена на указанный электронный адрес").css("font-size", "13px").css("color", "green");

            } else {
                $(".error_form_registration").text("Пользователь с таким адресом электронной почты не существует.").css("font-size", "13px").css("color", "red");
            }
        }
    });
}

function checkUserCredentials() {
    let username = $("#login_username").val();
    let password = $("#login_password").val();


    $.ajax({
        url: "/profile/check_user_credentials/",
        data: {
            username: username,
            password: password
        },
        success: function(response) {
            if (response.credentials_valid) {
                $(".error_form_registration").text(""); // Очищаем сообщение об ошибке
                // Здесь можно выполнить дополнительные действия, например, выполнить вход пользователя
                $("#login").unbind('submit').submit(); // Продолжить отправку формы
            } else {
                $(".error_form_registration").text("Неправильное имя пользователя или пароль.");
            }
        }
    });
}