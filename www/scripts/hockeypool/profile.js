function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
	var cookies = document.cookie.split(';');
	for (var i = 0; i < cookies.length; i++) {
	    var cookie = jQuery.trim(cookies[i]);
	    // Does this cookie string begin with the name we want?
	    if (cookie.substring(0, name.length + 1) == (name + '=')) {
		cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		break;
	    }
	}
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
	if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	    xhr.setRequestHeader("X-CSRFToken", csrftoken);
	}
    }
});

function update_password() {
	var old_pass = $('#old_pass').val();
	var password1 = $('#password1').val();
	var password2 = $('#password2').val();
	var postData = JSON.stringify({ "old_pass" : old_pass, "password1" : password1, "password2" : password2, csrfmiddlewaretoken : getCookie('csrftoken')});

	$.post("/ajax/changePassword", postData, function(data, status) {
		if (data.error == 0) {
			message(data.msg,"black","#notification_div");
		} else {
			message(data.msg,"red","#notification_div");
		}

	});
}

function update_team_name() {
	var new_team_name = $('#change_team_name').val()
        var postData = JSON.stringify({ "new_team_name" : new_team_name, csrfmiddlewaretoken : getCookie('csrftoken')});

        $.post("/ajax/updateTeamName", postData, function(data, status) {
		if (data.error == 0) {
			message(data.msg,"black","#notification_div");
		} else {
			message(data.msg,"red","#notification_div");
		}

        });

}

function update_theme() {
        var new_theme = $('#theme_select').val();
        var postData = JSON.stringify({ "new_theme" : new_theme, csrfmiddlewaretoken : getCookie('csrftoken')});

        $.post("/ajax/updateTheme", postData, function(data, status) {
		if (data.error == 0) {
			message(data.msg,"black","#notification_div");
		} else {
			message(data.msg,"red","#notification_div");
		}

        });

}

function update_user_name() {
        var new_user_name = $('#change_user_name').val();
        var postData = JSON.stringify({ "new_user_name" : new_user_name, csrfmiddlewaretoken : getCookie('csrftoken')});

        $.post("/ajax/updateUsername", postData, function(data, status) {
		if (data.error == 0) {
			message(data.msg,"black","#notification_div");
		} else {
			message(data.msg,"red","#notification_div");
		}
        });

}

