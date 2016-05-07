$(document).ready(function() {
  //register
  $("#RGBTN").click(function(){
      var pass1 = document.getElementById("NWW").value;
      var pass2 = document.getElementById("NWWR").value;
      var lastname = document.getElementById("NUSSNM").value;
      var firstname = document.getElementById("NUSNM").value;
      var email = document.getElementById("NUSEM").value;
      alert(lastname+firstname+email);
      if(lastname && firstname && email){
	alert(":)");
	if(pass1 == pass2){
	  alert("doei");
	  
	  $('#registerform').ajaxForm({
	    dataType : 'json',
	    success : function (submit_return){
	      console.log("hoi:" + submit_return);
	      if (submit_return == "NU"){
		$("#Overlay").show();
	      }else if(submit_return == "JU") {
		document.getElementById("COS").innerHTML = "wachtwoord";
		$("#registerBTN").remove();
		$("#usrnm").type = 'password';
		$("#usrnm").hide();
		$("#usrpw").show();
		console.log("aaaijod");
	      }else if(submit_return == "JP"){
		location.reload(true);
		console.log("dddoiai");
	      }else if(submit_return == "NP"){
		$("#OverlayP").show();
	      }
	    }
	  });
	  
	  $('#registerform').submit();
	}else{
	}
      }
  });
});