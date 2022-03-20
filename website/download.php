<?php

	if(!isset($_GET["file"]) || $_GET["file"] == "") {
		die("No file name!");
	}

	if(!isset($_GET["type"]) || $_GET["type"] == "") {
		die("No file type!");
	}

	// sanitize filename and type
	$file_name      = preg_replace("/[^a-zA-Z0-9_]/", "", $_GET["file"]);
	$animation_type = preg_replace("/[^a-zA-Z0-9_]/", "", $_GET["type"]);

	// build the file name
	$animation_id = "uploads/" . $file_name . "/animation." . $animation_type;

	header('Content-Type: application/octet-stream');
	header('Content-Disposition: attachment; filename=animation.'.$animation_type);
	readfile($animation_id);

	exit;

?>
