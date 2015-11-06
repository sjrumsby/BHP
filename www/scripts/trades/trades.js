function trade_players() {
	var own_player = $("#trade_own").val();
	var other_player = $("#trade_other").val();
	var postData = {"own_player" : own_player, "other_player" : other_player}
	$.post("/ajax/tradePlayers", postData, function(data, status) {
		var success_html;
		if (data.error == 1) {
			success_html = "<h1>Error</h1><p>Trades not processed with the following errors:<ul>";
		} else {
			success_html = "<h1>Success!</h1><p>Your trades were successfully processed</p>>";
		}
		$("#success_div").html(success_html);
	});
}

