$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
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
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

function trade_players() {
	var own_player = $("#trade_own_id").val();
	var other_player = $("#trade_other_id").val();
	var postData = {"own_player" : own_player, "other_player" : other_player, }
	$.post("/ajax/tradePlayers", postData, function(data, status) {
		var success_html;
		if (data.error == 1) {
			success_html = "<h1>Error</h1><p>Trades not processed with the following errors:<ul>" + data.msg + "</ul></p>";
		} else {
			success_html = "<h1>Success!</h1><p>Your trades were successfully processed</p>";
		}
		$("#success_div").html(success_html);
	});
}

function trade_own_player(e, input) {
        var code = (e.keyCode ? e.keyCode : e.which);
        if (((code >= 48) && (code <= 90)) || (code == 8)) {
		var player_name = $('#trade_own').val();
		if (player_name.length > 2) {
			$.get("/ajax/getTradeOwn/"+player_name + "/")
			.done(function(data) {
				$('#suggestions_own').html(data)
			});
		}
	}
}

function trade_other_player(e, input) {
	var code = (e.keyCode ? e.keyCode : e.which);
	if (((code >= 48) && (code <= 90)) || (code == 8)) {
		var player_name = $('#trade_other').val();
		if (player_name.length > 2) {
			$.get("/ajax/getTradeOther/"+player_name + "/")
			.done(function(data) {
				$('#suggestions_other').html(data)
			});
		}
	}
}

function replace_trade_own_text(name, id) {
	$('#trade_own').val(name);
	$('#trade_own_id').val(id);
	$.get("/ajax/getTradeOwn/"+name + "/")
	.done(function(data) {
		$('#suggestions_own').html(data)
	});

}

function replace_trade_other_text(name, id) {
	$('#trade_other').val(name);
	$('#trade_other_id').val(id);
        $.get("/ajax/getTradeOther/"+name + "/")
        .done(function(data) {
                $('#suggestions_other').html(data)
        });

}

