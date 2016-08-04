<?php
	require_once("pubnub-php/composer/lib/autoloader.php");
	use Pubnub\Pubnub;

	// group ID for this iamge
	$id = ((isset($_GET["id"]) && $_GET["id"] != "") ? $_GET["id"] : "default");

	// choose folder with the given group ID
	$uploaddir = 'uploads/'.$id.'/';

	// upload the file
	$filename = basename($_FILES['file']['name']);
	$uploadfile = getcwd() . '/' . $uploaddir . $filename;
    move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile);

    // Load the image
    $source = imagecreatefromjpeg($uploadfile);

    // Rotate the image by 90°
    $rotate = imagerotate($source, 90, 0);

    // save the rotated image
    $final = imagejpeg($rotate, $uploadfile);

	$pubnub = new Pubnub('PUBLISH_KEY', 'SUBSCRIBE_KEY');
	$publish_result = $pubnub->publish('portrait_dev', array('action' => 'reload', 'id' => $id, 'target' => substr($filename,0,2), 'item' => $uploaddir.$filename));

	echo "OK";
?>	