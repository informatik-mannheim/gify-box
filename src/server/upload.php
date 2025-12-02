<?php

	// increase time limit for this script to deal
	// with slow uploads and the encoding time
	// needed
	set_time_limit(180);

	// choose folder with the given group ID
	$uploadroot = 'uploads';

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


		// generate MP4
		exec('ffmpeg -framerate 3 -i '.$uploadroot.'/'.$timeId.'/frame%02d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p '.$uploadroot.'/'.$timeId.'/animation.mp4');
		exec('ffmpeg -framerate 3 -i '.$uploadroot.'/'.$timeId.'/frame%02d.jpg -c:v gif '.$uploadroot.'/'.$timeId.'/animation.gif');
		// print server URI, the "y" for the detail view route and id for the new gif
		echo 'http'. (($_SERVER['SERVER_PORT'] == '443') ? 's' : '') .'://'. $_SERVER['SERVER_NAME'] .'/y';
		echo $timeId;
	}

	function GetIdTimestring() {
		$charstring = "C7rNA5h2ktBKEsU9c3PS6FRHqpinbfQaT841jJue";
		$datestring = date('y-m-d-H-i-s', time());

		$uniqueId = "";
		foreach (explode("-", $datestring) as $val) {
			$uniqueId .= $charstring[$val%strlen($charstring)];
		}

		return $uniqueId;
	}
?>