alert('Scenemain.js loaded');

function Scenemain() {
	this.index = 1;
	this.numeroDeJogadores = 2;
};

Scenemain.prototype.initialize = function () {
	alert("Scenemain.initialize()");
	// this function will be called only once when the scene manager show this scene first time
	// initialize the scene controls and styles, and initialize your variables here
	// scene HTML and CSS will be loaded before this function is called
}

Scenemain.prototype.handleShow = function (data) {
	alert("Scenemain.handleShow()");
	// this function will be called when the scene manager show this scene	
};

Scenemain.prototype.handleHide = function () {
	alert("Scenemain.handleHide()");
	// this function will be called when the scene manager hide this scene
};

Scenemain.prototype.handleFocus = function () {
	alert("Scenemain.handleFocus()");
	// this function will be called when the scene manager focus this scene
};

Scenemain.prototype.handleBlur = function () {
	alert("Scenemain.handleBlur()");
	// this function will be called when the scene manager move focus to another scene from this scene
};

Scenemain.prototype.handleKeyDown = function (keyCode) {
	alert("Scenemain.handleKeyDown(" + keyCode + ")");
	// TODO : write an key event handler when this scene get focused
	switch (keyCode) {
		case sf.key.LEFT:
			break;
		case sf.key.RIGHT:
			break;
		case sf.key.UP:
			this.moveUp();
			break;
		case sf.key.DOWN:
			this.moveDown();
			break;
		case sf.key.ENTER:
			this.onEnter();
			break;
		default:
			alert("handle default key event, key code(" + keyCode + ")");
			break;
	}
};

Scenemain.prototype.moveDown = function() {
	alert("SCENEMAIN :: MOVEDOWN "+this.index);
	
	if(this.index == 1) {
		$("#box1").removeClass( "ButtonSelected" );
		$("#box2").addClass( "ButtonSelected" );
		this.index = 2;
		this.numeroDeJogadores = 3;

	} else if(this.index == 2) {
		$("#box2").removeClass( "ButtonSelected" );
		$("#box3").addClass( "ButtonSelected" );
		this.index = 3;
		this.numeroDeJogadores = 4;
	} else if(this.index == 3) {
		$("#box3").removeClass( "ButtonSelected" );
		$("#box4").addClass( "ButtonSelected" );
		this.index = 4;
	} else {
		alert("invalid operation");
	}
};

Scenemain.prototype.moveUp = function() {
	alert("SCENEMAIN :: MOVEUP");
	if(this.index == 4) {
		$("#box4").removeClass( "ButtonSelected" );
		$("#box3").addClass( "ButtonSelected" );
		this.index = 3;
		this.numeroDeJogadores = 4; 
	} else if(this.index == 3) {
		$("#box3").removeClass( "ButtonSelected" );
		$("#box2").addClass( "ButtonSelected" );
		this.index = 2;
		this.numeroDeJogadores = 3;
	} else if(this.index == 2) {
		$("#box2").removeClass( "ButtonSelected" );
		$("#box1").addClass( "ButtonSelected" );
		this.index = 1;
		this.numeroDeJogadores = 2;
	} else {
		alert("invalid operation");
	}
};

Scenemain.prototype.onEnter = function() {
	alert("SCENEMAIN :: ONENTER");

	var nJogadores = this.numeroDeJogadores;
	alert("NUMERO DE JOGADORES: "+nJogadores);
	CenaEscolha.numberOfPlayer = nJogadores;

	/*$("#Scenemain").css({'opacity':'0'});
	$("#ScenepickPlayer").css({'visibility':'visible'});
	$("#ScenepickPlayer").css({'opacity':'1'});*/
	$("#Scenemain").css({'opacity':'0'});
	$("#Scenemain").bind("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd", function(){ 
		sf.scene.hide('main');
		sf.scene.show('pickPlayer');
		sf.scene.focus('pickPlayer');
	 });
	
};
