<?php
require("funciones.php");	

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  
	if (isset($_POST['json'])) {
		$json = $_POST['json'];
		echo $json;
		$obj = json_decode($json, true);
		echo $json;
		var_dump($obj);
		switch ($obj['msg']) {
			case 'guardaJugadorBBDD':
				guardaJugadorBBDD($obj['player']);
				break;
			case 'actualizaHoraEntradaBBDD':
				actualizaHoraEntradaBBDD($obj['player'], $obj['date'], $obj['time']);
				break;
			case 'actualizaHorasJugandoBBDD':
				actualizaHorasJugandoBBDD($obj['player'], $obj['date'], $obj['time']);
				break;
			case 'guardaLogroBBDD':
				guardaLogroBBDD($obj['player'], $obj['date'], $obj['time'], $obj['logro']);
				break;
			case 'guardaLineaDesconocidaLogBBDD':
				guardaLineaDesconocidaLogBBDD($obj['player'], $obj['date'], $obj['time'], $obj['log']);
				break;
			case 'guardaMuerteBBDD':
				guardaMuerteBBDD($obj['player'], $obj['date'], $obj['time'], $obj['type'], $obj['killer'], $obj['item']);
				break;
			case 'guardaLineaConocidaLogBBDD':
				guardaLineaConocidaLogBBDD($obj['player'], $obj['date'], $obj['time'], $obj['log']);
				break;
		}
	}
}
?>



