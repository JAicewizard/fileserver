var ID = "";
$(document).ready(function(){
	webStart();
});
function webStart(ID){
var messageContainer = document.getElementById('messages');
if ('WebSocket' in window) {
	append("websocked is available")
	var ws = new WebSocket('ws://82.95.120.43:8888/WS?I_D='+ID);
	ws.onopen = function () {
		append("connection opend");
	};
	var received_msg = "";
	ws.onmessage = function (evt) {
		var received_old =received_msg;
		received_msg = evt.data;
		console.log(received_old,"hoi", received_msg)
		if(received_old.charAt(0) == "1"){
			files = $.parseJSON(received_msg);
			for(i=0; i< files.length; i++){
				append(files[i].mpn);
				addfile(files[i].mpn, files[i].Fdt);				
			}
		}if(received_old.charAt(0) == "0"){
			ID = received_msg;
			append(received_msg)
			ws.close();
		}else{
			append("message received: " + received_msg);
		}
	};
	ws.onclose = function () {
		console.log('closed');
		append("connection closed")
		webStart(ID);
	}	
}else{
	append("no suport for websocket");
}

function addfile(fileN,fileMD){
	var file = document.getElementById('Dfiles');
	file.innerHTML = "<span id='filecontainer'><div id='F'>"+fileN+"</div><div id='DTA'><div id='MDT'>last modification:"+fileMD+"</div></div></span>"+file.innerHTML
}

function append(string){
	var messageContainer = document.getElementById('messages');
	messageContainer.innerHTML = string+"<br/>"+messageContainer.innerHTML;
}
$("#in").keyup(function (e) {
	if (e.keyCode == 13) {
		console.log("send");
		ws.send($("#in").val());
	}
}); 
}
