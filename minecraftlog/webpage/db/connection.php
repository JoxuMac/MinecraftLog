<?php
 
   require("config.php");
   
   // Set up the PDO parameters
/*   $dsn 	= "mysql:host=" . $hn . ";port=3306;dbname=" . $db . ";charset=" . $cs;
   $opt 	= array(
                        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_OBJ,
                        PDO::ATTR_EMULATE_PREPARES   => false,
                       );
   // Create a PDO instance (connect to the database)
   $pdo 	= new PDO($dsn, $un, $pwd, $opt);*/
   
   // Create connection
	$conn = mysqli_connect($hn, $un, $pwd, $db);
	$conn->set_charset("utf8");
	// Check connection
	if (!$conn) {
		die("ERROR: " . mysqli_connect_error());
	}
   
?>