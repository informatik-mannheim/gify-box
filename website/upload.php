<?php
	require_once("pubnub-php/composer/lib/autoloader.php");
	use Pubnub\Pubnub;

	// choose folder with the given group ID
	$uploadroot = 'uploads/';

	if(!empty($_FILES['image0'])) {

		// get the target dir
		$rand_dir = date('YmdHis', time()) . '-' . mt_rand();
		$uploaddir = getcwd() . '/' . $uploadroot . '/' . $rand_dir;

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
		    $animation->setImageDelay(50);
		    $animation->nextImage();
		}

		// save gif animation
		$animation->writeImages($uploaddir.'/animation.gif', true);
	}

	/*
	$pubnub = new Pubnub('PUBLISH_KEY', 'SUBSCRIBE_KEY');
	$publish_result = $pubnub->publish('portrait_dev', array('action' => 'reload', 'id' => $id, 'target' => substr($filename,0,2), 'item' => $uploaddir.$filename));
	*/

	echo "OK";
?>	