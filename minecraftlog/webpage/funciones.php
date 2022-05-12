<?php

// GUARDA UN NUEVO JUGADOR EN BBDD
function guardaJugadorBBDD($player){
	require("db/connection.php");
	$image = 'todo';
	$sql = "INSERT INTO `users` (`player`, `image`) VALUES ('" .$player. "', '" .$image. "');";
	
	if (mysqli_query($conn, $sql)) {
		return $player;
	} else {
		return NULL;
	}
}

// GUARDA LA HORA DE ENTRADA DE UN JUGADOR EN BBDD
function actualizaHoraEntradaBBDD($player, $date, $time){
	require("db/connection.php");
	$datetime = $date . " " . $time;
	$sql = "UPDATE `users` SET `join-date` = '" .$datetime. "' WHERE `users`.`player` = '" .$player. "';";
	if (mysqli_query($conn, $sql)) {
		return $player;
	} else {
		return NULL;
	}
}

// ACTUALIZA LAS HORAS JUGADAS DE UN JUGADOR Y RESETEA S HORA DE ENTRADA
function actualizaHorasJugandoBBDD($player, $date, $hora){
	require("db/connection.php");
	$datetime = $date . " " . $hora;
	
	$query = 'SELECT `join-date` as `joindate` FROM `users` WHERE `player` = "' .$player. '"';
	$resultado = mysqli_query( $conn, $query ) or die ("ERROR");
	
	if($resultado && $resultado->num_rows>0){		
		$obj = $resultado->fetch_object();
		
		if($obj->joindate == NULL)
			return NULL;
		
		$time = new DateTime($obj->joindate);
		$diff = $time->diff(new DateTime($datetime));
		$minutes = ($diff->days * 24 * 60) + ($diff->h * 60) + $diff->i;
		
		$sql = "UPDATE `users` SET `join-date` = NULL, `minutes-played` = `minutes-played` + " .$minutes. " WHERE `users`.`player` = '" .$player. "';";
		
		if (mysqli_query($conn, $sql)) {
			return $player;
		} else {
			return NULL;
		}
	} else {
		return NULL;
	}
}

// GUARDA EL LOGRO DE UN JUGADOR EN BBDD
function guardaLogroBBDD($player, $date, $hora, $logro){
	require("db/connection.php");
	$datetime = $date . " " . $hora;
	$sql = "INSERT INTO `logros` (`datetime`, `player`, `logro`) VALUES ('" .$datetime. "', '" .$player. "', '" .$logro. "');";
	if (mysqli_query($conn, $sql)) {
		return $player;
	} else {
		return NULL;
	}
}

// GUARDA UNA LINEA DE LOG DESCONOCIDA EN BBDD
function guardaLineaDesconocidaLogBBDD($player, $date, $hora, $log){
	require("db/connection.php");
	$datetime = $date . " " . $hora;
	$sql = "INSERT INTO `unknown_logs` (`datetime`, `player`, `log`) VALUES ('" .$datetime. "', '" .$player. "', '" .$log. "');";
	if (mysqli_query($conn, $sql)) {
		return $player;
	} else {
		return NULL;
	}
}

// GUARDA LA MUERTE DE UN JUGADOR EN BBDD
function guardaMuerteBBDD($player, $date, $hora, $tipo, $killer, $item){
	require("db/connection.php");
	$datetime = $date . " " . $hora;
	$sql = "INSERT INTO `muertes` (`datetime`, `player`, `tipo`, `killer`, `item`) VALUES ('" .$datetime. "', '" .$player. "', " .$tipo. ", '" .$killer. "', '" .$item. "');";
	if (mysqli_query($conn, $sql)) {
		return $player;
	} else {
		return NULL;
	}
}

// GUARDA UNA LINEA DE LOG CONOCIDA EN BBDD
function guardaLineaConocidaLogBBDD($player, $date, $hora, $log){
	require("db/connection.php");
	$datetime = $date . " " . $hora;
	$sql = "INSERT INTO `known_logs` (`datetime`, `player`, `log`) VALUES ('" .$datetime. "', '" .$player. "', '" .$log. "');";
	if (mysqli_query($conn, $sql)) {
		return $player;
	} else {
		return NULL;
	}
}

?>