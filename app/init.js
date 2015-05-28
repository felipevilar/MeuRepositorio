
function onStart () {
	// TODO : Add your Initialize code here
	// NOTE : In order to start your app, call "sf.start()" at the end of this function!!
	
	CenaTabuleiro = sf.scene.get('tabscreen');
	CenaInicial = sf.scene.get('main');
	CenaEscolha = sf.scene.get('pickPlayer');
	
	sf.scene.show('main');
	sf.scene.focus('main');
}
function onDestroy () {
	//stop your XHR or Ajax operation and put codes to destroy your application here
	
}

alert("init.js loaded.");
