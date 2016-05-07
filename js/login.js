$(document).ready(function(){
	function getCookie(name) {
		var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
		return r ? r[1] : undefined;
	}
	$("#loginBTN").click(function(){
		var P = $.post("/login",{name: $("#name").val(), pass: $("#pass").val(), _xsrf: getCookie("_xsrf") });
		P.done(function(data){
			console.log(data.error);
			if(data.error == false){
				window.location.href="http://82.95.120.43:8888";
				
			}			
		})
	});
});
