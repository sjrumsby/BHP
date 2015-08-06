        function draft_player(){
                var xmlhttp;
                str = document.getElementById("draft_pick").value;
                if (str.length < 2) {
                        document.getElementById("draft_suggestions").innerHTML = "";
                        return;
                }
                if (window.XMLHttpRequest){
                        xmlhttp=new XMLHttpRequest();
                } else {
                        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
                }
                xmlhttp.onreadystatechange = function(){
                        if (xmlhttp.readyState==4 && xmlhttp.status==200){
                                document.getElementById("draft_suggestions").innerHTML = xmlhttp.responseText;
                        }
                }
                xmlhttp.open("GET","/ajax/getPlayer/"+str+"/",true);
                xmlhttp.send();
        }
	
	function add_player() {
		var xmlhttp;
		str = document.getElementById("waiver_add").value.replace("\\", "");
		if (str.length < 2) {
			document.getElementById("add_suggestions").innerHTML = "";
			return;
		}
		if (window.XMLHttpRequest){
                        xmlhttp=new XMLHttpRequest();
                } else {
                        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
                }
                xmlhttp.onreadystatechange = function(){
                        if (xmlhttp.readyState==4 && xmlhttp.status==200){
				document.getElementById("add_suggestions").innerHTML = xmlhttp.responseText;
			}
		}
                xmlhttp.open("GET","/ajax/getWaiverPlayer/"+str+"/",true);
                xmlhttp.send();
        }

        function replace_draft_text(str) {
                document.getElementById("draft_pick").value = str;
                draft_player();
        }

	function replace_waiver_text(str1, str2) {
		document.getElementById("waiver_add").value = str1;
		document.getElementById("waiver_add_id").value = str2;
		add_player();
	}

	function trade_own_player(){
		var xmlhttp;
                str = document.getElementById("trade_own").value;
                if (str.length < 2) {
                        document.getElementById("trade_suggestions_own").innerHTML = "";
                        return;
                }
                if (window.XMLHttpRequest){
                        xmlhttp=new XMLHttpRequest();
                } else {
                        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
                }
                xmlhttp.onreadystatechange = function(){
                        if (xmlhttp.readyState==4 && xmlhttp.status==200){
                                document.getElementById("trade_suggestions_own").innerHTML = xmlhttp.responseText;
                        }
                }
                xmlhttp.open("GET","/ajax/getTradeOwn/"+str+"/",true);
                xmlhttp.send();
        }

        function trade_other_player(){
                var xmlhttp;
                str = document.getElementById("trade_other").value;
                if (str.length < 2) {
                        document.getElementById("trade_suggestions_other").innerHTML = "";
                        return;
                }
                if (window.XMLHttpRequest){
                        xmlhttp=new XMLHttpRequest();
                } else {
                        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
                }
                xmlhttp.onreadystatechange = function(){
                        if (xmlhttp.readyState==4 && xmlhttp.status==200){
                                document.getElementById("trade_suggestions_other").innerHTML = xmlhttp.responseText;
                        }
                }
                xmlhttp.open("GET","/ajax/getTradeOther/"+str+"/",true);
                xmlhttp.send();
        }

        function replace_trade_own_text(str) {
                document.getElementById("trade_own").value = str;
                trade_own_player()
        }

	function replace_trade_other_text(str) {
		document.getElementById("trade_other").value = str;
		trade_other_player();
	}
