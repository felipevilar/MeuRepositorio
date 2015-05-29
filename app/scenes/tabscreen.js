alert('Scenetabscreen.js loaded');

function Scenetabscreen() {
	
	this.urls = new Array();
	this.numberPlayers = "";
	this.CurrentTurn = 0;
	
	this.timeOut = null;
	
	this.option = '';
	this.isRotating = false;
	
};
Scenetabscreen.prototype.initialize = function () {
	alert("Scenetabscreen.initialize()");
	// this function will be called only once when the scene manager show this scene first time
	// initialize the scene controls and styles, and initialize your variables here
	// scene HTML and CSS will be loaded before this function is called
};

Scenetabscreen.prototype.handleShow = function (data) {
	alert("Scenetabscreen.handleShow()"+this.numberPlayers);
	$("#Scenetabscreen").css({'opacity':'1'});
	// this function will be called when the scene manager show this scene
};

Scenetabscreen.prototype.handleHide = function () {
	alert("Scenetabscreen.handleHide()");
	// this function will be called when the scene manager hide this scene
};

Scenetabscreen.prototype.handleFocus = function () {
	alert("Scenetabscreen.handleFocus()");
	// this function will be called when the scene manager focus this scene
};

Scenetabscreen.prototype.handleBlur = function () {
	alert("Scenetabscreen.handleBlur()");
	// this function will be called when the scene manager move focus to another scene from this scene
};

Scenetabscreen.prototype.handleKeyDown = function (keyCode) {
	alert("Scenetabscreen.handleKeyDown(" + keyCode + ")");
	// TODO : write an key event handler when this scene get focused
	switch (keyCode) {
		case sf.key.LEFT:
			alert("this.isRotating: "+this.isRotating);
			break;
		case sf.key.RIGHT:
			break;
		case sf.key.UP:
			this.isRotating = false;
			break;
		case sf.key.DOWN:
			break;
		case sf.key.ENTER:
			this.onEnter();
			break;
		default:
			alert("handle default key event, key code(" + keyCode + ")");
			break;
	}
};

Scenetabscreen.prototype.onEnter = function() {
	alert("Scenetabscreen.prototype.onEnter");	
	
	if(this.isRotating == false) {
		
		this.isRotating = true;
		
		$('#roleta').css({'-webkit-transition-duration':'0s'});
		document.getElementById("roleta").style.webkitTransform = "rotate(0deg)";
		
		var randomNumber = Math.floor(Math.random() * 6) + 1;
		alert(randomNumber);
		
		document.getElementById("roleta").style.webkitTransform = "rotate(0deg)";
		
		if(randomNumber == 1) {
			this.rotateStyle(30);
		}else if(randomNumber == 2) {
			this.rotateStyle(-30);
		}else if(randomNumber == 3) {
			this.rotateStyle(-90);
		}else if(randomNumber == 4) {
			this.rotateStyle(-150);
		}else if(randomNumber == 5) {
			this.rotateStyle(147);
		} else if(randomNumber == 6) {
			this.rotateStyle(90);
		}
	}
}


Scenetabscreen.prototype.rotateStyle = function (rotateAngle) {
	alert("Scenetabscreen.prototype.rotateStyle");
	
	var angle = 2160+rotateAngle;
	$('#roleta').css({'-webkit-transition-duration':'5s'});
	document.getElementById("roleta").style.webkitTransform = "rotate("+angle+"deg)";

}

