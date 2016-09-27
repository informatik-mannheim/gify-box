<?php

	if(!isset($_GET["file"]) || $_GET["file"] == "") {
		die("No file name!");
	}

	if(!isset($_GET["type"]) || $_GET["type"] == "") {
		die("No file type!");
	}

	// get the file name
	$animation_type = $_GET["type"];
	$animation_id = "uploads/".$_GET["file"]."/animation.".$animation_type;

	header('Content-Type: application/octet-stream');
	header('Content-Disposition: attachment; filename=animation.'.$animation_type);
	readfile($animation_id);

	exit;

?>