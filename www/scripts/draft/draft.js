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

setInterval(function(){reduceTimer()},1000);
setInterval(function(){pageUpdate()},5000);

function reduceTimer() {
	curr_time = $('#time_remaining_text').html().match(/[-\d]+/)
	if (curr_time) {
		new_time = curr_time - 1
		$('#time_remaining_text').html("Time remaining: " + new_time)
	}
}

function pageUpdate() {
	$.post("/ajax/draftUpdate",{'undrafted_sort' : $('#undrafted_sort_by').val(), 'csrfmiddlewaretoken' : getCookie('csrftoken')},function(data, textStatus, jqXHR){
		if (data.state == "draft") {
			var time_html = "Time remaining: " + data.time_left;
			var current_round_html = "The current round is: <b>" + data.current_round + "</b>";
			var round_order_html = '<tr><th>Pick</th><th>Team</th><th>Player</th></tr>';
			for(var i = 0; i < data.round_order.length; i++){
				pick = 8*(data.current_round - 1) + i + 1;
				round_order_html += "<tr><td>" + pick + "</td><td><span class='playerPopUp' id='player-" + data.round_order[i].id + "' player_id='" + data.round_order[i].id + "'><a href='#'>" + data.round_order[i].player + "</a></span></td>"
				if (data.round_order[i].pick != "None") {
					round_order_html += "<td><span class='skaterPopUp' id='skater-" + data.round_order[i].id + "' nhl_id='" + data.round_order[i].id + "'><a href='#'>" + data.round_order[i].pick + "</a></span></td>"
				} else {
					round_order_html += "<td>No pick yet</td>";
				}
				round_order_html += "</tr>";
			}
			var top_player_html = "";
			for(var i = 0; i < data.top_picks.length; i++){
				top_player_html += '<tr><td>' +  data.top_picks[i]['position']  + '</td><td><span id="skater-' + data.top_picks[i]['id'] + '" class="skaterPopUp" nhl_id="' + data.top_picks[i]['id'] + '"><a href="#">' + data.top_picks[i]['name'] + '</a></span></td></tr>';
			}

			var left_wing_html = "";
			var right_wing_html = "";
			var center_html = "";
			var ldefense_html = "";
			var rdefense_html = "";
			var goalie_html = "";

			for (i = 0; i < data.lw.length; i++){
				left_wing_html += "<li>" + data.lw[i]['name'] + "</li>";
			}

			for (i = 0; i < data.rw.length; i++){
				right_wing_html += "<li>" + data.rw[i]['name'] + "</li>";
			}

			for (i = 0; i < data.c.length; i++){
				center_html += "<li>" + data.c[i]['name'] + "</li>";
			}

			for (i = 0; i < data.rd.length; i++){
				if (i%2 == 1) {
					rdefense_html += "<li>" + data.rd[i]['name'] + "</li>";
				} else {
					ldefense_html += "<li>" + data.rd[i]['name'] + "</li>";
				}
			}

			for (i = 0; i < data.g.length; i++){
				goalie_html += "<li>" + data.g[i]['name'] + "</li>";
			}

			$("#left_wing ol").html(left_wing_html);
			$("#right_wing ol").html(right_wing_html);
			$("#center ol").html(center_html);
			$("#l_defense ol").html(ldefense_html);
			$("#r_defense ol").html(rdefense_html);
			$("#goalie ol").html(goalie_html);

			if (data.is_turn == 1) {
				if ($("#draft_pick_button").find("table").length == 0) {
					$('#draft_pick_button').html('<table><tr><td>Its your turn. Draft a player:  </td><td><form><input id="draft_pick" type="text" onkeyup="draft_player()" name="draft_pick" value=""><input id="draft_pick_id" type="hidden" name="draft_pick_id" value=""></form><div id="draft_suggestions"></div></td><td><button id="pick_player" onclick="select_player()">Pick!</button></td></tr></table>');
				}
			} else{
				$("#draft_player_select").html('<p>It is not currently your turn</p><div id="time_remaining"><h1 id="time_remaining_text">Time remaining: 60</h1></div>');
				$("#draft_suggestions").html("");
			}
			$("#time_remaining_text").html(time_html);
			$("#current_round_p").html(current_round_html);
			$("#draft_order_table").html(round_order_html);
			$("#top_player_list").html(top_player_html);

			$('.skaterPopUp').on('click', function(e) { 
				e.preventDefault();
				nhlID = $(this).attr("nhl_id")
				loadSkaterPopUp(nhlID) 
			});
			$('.playerPopUp').on('click', function(e) { 
				e.preventDefault();
				playerID = $(this).attr("player_id")
				loadPlayerPopUp(playerID) 
			});
		} else if (data.state == "ready") {
			var status_html = '<tr><th>Team</th><th>Status</th></tr>';
			for (var i = 0; i < data.player_status.length; i++) {
				status_html += "<tr><td>" + data.player_status[i][1] + "</td>";
				if (data.player_status[i][0] == 0) {
					status_html += "<td>Not Ready</td>";
				} else {
					status_html += "<td>Ready</td>";
				}
				status_html += "</tr>";
			}
			$("#ready_status").html(status_html);
			sortables_init();
		} else if (data.state == "finished") {
			$(".draft_container").html("<h1>Draft is over</h1>");
			$("#draft_player_select").html("");
		} else {
			$("#player_draft_status").html("<h1>Draft will commence in less than 60 seconds.</h1>");
			$("#ready_form").html(" ");
			$("#player_status_text").html("<p>All players ready. Draft will commence shortly</p>");
			var date = new Date();
		       var time = date.getTime();
			time = (time/1000) % 60;
			time = 65 - time;
			setTimeout("location.reload(true);", time*1000);
		}
	})
};

function update_status() {
	var e = document.getElementById("draft_ready");
	var draft_status = e.options[e.selectedIndex].value;
	if (draft_status == "not_ready") {
		var draft_var = 0;
	} else {
		var draft_var = 1;
	}
	var postData = {"status" : draft_var, "csrfmiddlewaretoken": getCookie('csrftoken')}
	$.post("/ajax/updateStatus", postData, function(data, status) {
		if (data.errors == 1) {
			alert("Fail:\n\n Did not successfully update status. Contact the comissioner");
		}
	});
}

function select_player() {
	var player_id = document.getElementById("draft_pick_id").value;
	var postData = {"player_id" : player_id, "csrfmiddlewaretoken": getCookie('csrftoken')};
	$.post("/ajax/pickPlayer", postData, function(data, status){
		if (data.errors == 1) {
			alert("Fail:\n\n" + data.message);
		} else {
			alert("Success:\n\n" + data.message);
			$('#draft_pick_button').html('')
		}
	});
}

function draft_player() {
	var player_name = $('#draft_pick').val()
	if (player_name.length > 2) {
		var postData = {"player_name" : player_name, "csrfmiddlewaretoken": getCookie('csrftoken')};
		$.post("/ajax/getPlayer", postData, function(data, status){
			$('#draft_suggestions').html(data)
		});
	}
}

function replace_draft_text(player_name, player_id) {
	$('#draft_pick').val(player_name);
	$('#draft_pick_id').val(player_id);
}
