alert('ScenepickPlayer.js loaded');

function ScenepickPlayer() {
	this.currentFocus = 1; 
	this.lastFocus = 1;
	
	this.numberOfPlayer = '';
	this.selectedPlayers = 0;

	this.imageUrl = new Array();
};

ScenepickPlayer.prototype.initialize = function () {
	alert("ScenepickPlayer.initialize()");
	// this function will be called only once when the scene manager show this scene first time
	// initialize the scene controls and styles, and initialize your variables here
	// scene HTML and CSS will be loaded before this function is called

};

ScenepickPlayer.prototype.handleShow = function (data) {
	alert("ONSCENEPICKPLAYER : HANDLESHOW: "+this.numberOfPlayer);
	$("#ScenepickPlayer").css({'opacity':'1'});
	// this function will be called when the scene manager show this scene
};

ScenepickPlayer.prototype.handleHide = function () {
	alert("ScenepickPlayer.handleHide()");
	// this function will be called when the scene manager hide this scene
};

ScenepickPlayer.prototype.handleFocus = function () {
	alert("ScenepickPlayer.handleFocus()");
	// this function will be called when the scene manager focus this scene
};

ScenepickPlayer.prototype.handleBlur = function () {
	alert("ScenepickPlayer.handleBlur()");
	// this function will be called when the scene manager move focus to another scene from this scene
};

ScenepickPlayer.prototype.handleKeyDown = function (keyCode) {
	alert("ScenepickPlayer.handleKeyDown(" + keyCode + ")");
	// TODO : write an key event handler when this scene get focused
	switch (keyCode) {
		case sf.key.LEFT:
			if(this.currentFocus != 1) {
			this.lastFocus = this.currentFocus; 
			this.currentFocus -= 1;
			this.moveFocus();
			}
			break;
		case sf.key.RIGHT:
			if(this.currentFocus != 6) {
			this.lastFocus = this.currentFocus; 
			this.currentFocus += 1;
			this.moveFocus();
			}
			break;
		case sf.key.UP:
			if(this.currentFocus != 1 && this.currentFocus != 2 && this.currentFocus != 3) {
			this.lastFocus = this.currentFocus; 
			this.currentFocus -= 3;
			this.moveFocus();
			}
			break;
		case sf.key.DOWN:
			if(this.currentFocus != 4 && this.currentFocus != 5 && this.currentFocus != 6) {
			this.lastFocus = this.currentFocus; 
			this.currentFocus += 3;
			this.moveFocus();
			}
			break;
		case sf.key.ENTER:
			this.onEnter();
			break;
		default:
			alert("handle default key event, key code(" + keyCode + ")");
			break;
	}
};

ScenepickPlayer.prototype.moveFocus = function() {
	alert("ScenepickPlayer.prototype.moveFocus()");

	$( "#box"+this.lastFocus+"_selectplayer" ).removeClass( "selected" );
	$( "#box"+this.currentFocus+"_selectplayer" ).addClass( "selected" );
}

ScenepickPlayer.prototype.onEnter = function() {
	alert("ScenepickPlayer.prototype.onEnter()");
		
	if(!$( "#box"+this.currentFocus+"_selectplayer" ).hasClass( "ok" )) {
		
		this.selectedPlayers += 1;
	 
		if(this.selectedPlayers == 1) {

			document.getElementById("box"+this.currentFocus+"_selectplayer").style.backgroundColor = "#CC3333";
			document.getElementById("box"+this.currentFocus+"_selectplayer").style.borderColor = "red";
			document.getElementById("box"+this.currentFocus+"_selectplayer").style.borderWidth = "2px";
			document.getElementById("box"+this.currentFocus+"_selectplayer").className += " ok";
						$(".selected").css({"background-color":"yellow"});
			var imagePath = document.getElementById("img"+this.currentFocus+"").src;
			this.imageUrl.push(imagePath);

		} else if(this.selectedPlayers == 2) {
			document.getElementById("box"+this.currentFocus+"_selectplayer").style.borderColor = "blue";
			document.getElementById("box"+this.currentFocus+"_selectplayer").style.borderWidth = "2px";
			document.getElementById("box"+this.currentFocus+"_selectplayer").className += " ok";
			var imagePath = document.getElementById("img"+this.currentFocus+"").src;
			this.imageUrl.push(imagePath);
		} else if(this.selectedPlayers == 3) {

			document.getElementById("box"+this.currentFocus+"_selectplayer").style.borderColor = "green";
			document.getElementById("box"+this.currentFocus+"_selectplayer").style.borderWidth = "2px";
			document.getElementById("box"+this.currentFocus+"_selectplayer").className += " ok";
			var imagePath = document.getElementById("img"+this.currentFocus+"").src;
			this.imageUrl.push(imagePath);
		} else {
			
			document.getElementById("box"+this.currentFocus+"_selectplayer").style.borderColor = "yellow";
			document.getElementById("box"+this.currentFocus+"_selectplayer").style.borderWidth = "2px";
			document.getElementById("box"+this.currentFocus+"_selectplayer").className += " ok";
			var imagePath = document.getElementById("img"+this.currentFocus+"").src;
			this.imageUrl.push(imagePath);
		}
	
	}
	
	if(this.selectedPlayers == this.numberOfPlayer) {
		
		var that = this;

		setTimeout(function() {
			CenaTabuleiro.numberPlayers = that.numberOfPlayer;

			sf.scene.hide('pickPlayer');
			sf.scene.show('tabscreen');
			sf.scene.focus('tabscreen');

			var numberMagic = that.numberOfPlayer;
			for(var i=1; i<=numberMagic;i++) {
				var player = "player"+i;
				var point = "point-"+i;
				document.getElementById(""+player).style.visibility = "visible";
				document.getElementById(""+point).style.visibility = "visible";
				$('#'+player).css('background-image', 'url(' + that.imageUrl[i-1] + ')');			
			}
		}, 800);
	}

}