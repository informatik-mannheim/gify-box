<?php
	require_once("pubnub-php/composer/lib/autoloader.php");
	use Pubnub\Pubnub;

	// choose folder with the given group ID
	$uploadroot = 'uploads/';

	if(!empty($_FILES['image0'])) {

		// get the target dir
		$timeId = GetIdTimestring();
		$uploaddir = getcwd() . '/' . $uploadroot . '/' . $timeId;

		// create dir if not there
		if (!file_exists($uploaddir)) {
			mkdir($uploaddir, 0777, true);
		}

		// uploaded file array
		$uploaded_files = array();

		// upload the image files
		foreach($_FILES as $val) {
			$filename = $uploaddir . '/' . basename($val['name']);
			move_uploaded_file($val['tmp_name'], $filename);

			// add uploaded file to array
			$uploaded_files[] = $filename;
		}

		// create gif
		$animation = new Imagick();
		$animation->setFormat("GIF");

		// frames
		foreach($uploaded_files as $jpg_file) {
		    $frame = new Imagick($jpg_file);
		    $animation->addImage($frame);
		    $animation->setImageDelay(35);
		    $animation->nextImage();
		}

		// save gif animation
		$animation->writeImages($uploaddir.'/animation.gif', true);
	
		// send data to pubnub
		$pubnub = new Pubnub('pub-c-d74ad429-a08c-4141-b850-de0497df1020', 'sub-c-69d90c20-798e-11e6-9387-02ee2ddab7fe');
		$publish_result = $pubnub->publish('gifbox', array('action' => 'reload', 'id' => $timeId));

		// print server URI, the "y" for the detail view route and id for the new gif
		echo 'http'. (($_SERVER['SERVER_PORT'] == '443') ? 's' : '') .'://'. $_SERVER['SERVER_NAME'] .'/y';
		echo $timeId;
	}

	function GetIdTimestring() {
		$charstring = "Cz7YMrLNA5h2ktxBKEgsmUD9c3PXS6FRHqpidnbfQaGyT841ZjJue";
		$datestring = date('y-m-d-H-i-s', time());

		$uniqueId = "";
		foreach (explode("-", $datestring) as $val) {
			$uniqueId .= $charstring[$val%strlen($charstring)];
		}

		return $uniqueId;
	}
?>