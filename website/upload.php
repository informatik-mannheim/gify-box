<?php
	require_once("pubnub-php/composer/lib/autoloader.php");
	use Pubnub\Pubnub;

	// choose folder with the given group ID
	$uploadroot = 'uploads/';

	// get the image files
	$images = $_FILES['images'];

	if(!empty($images)) {
		$images_desc = reArrayFiles($images);

		// get the target dir
		$rand_dir = date('YmdHis', time()) . '-' . mt_rand();
		$uploaddir = getcwd() . '/' . $uploadroot . '/' . $rand_dir;

		// create dir if not there
		if (!file_exists($uploaddir)) {
			mkdir($uploaddir, 0777, true);
		}

		// upload the image files
		foreach($images_desc as $val) {
			$filename = $uploaddir . basename($val['name']);
			move_uploaded_file($val['tmp_name'], $filename);
		}
	}

	/*/ upload the file
	$filename = basename($_FILES['images']['name']);
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
	*/

	function reArrayFiles($file) {
		$file_ary = array();
		$file_count = count($file['name']);
		$file_key = array_keys($file);

		for($i=0;$i<$file_count;$i++) {
		    foreach($file_key as $val) {
		        $file_ary[$i][$val] = $file[$val][$i];
		    }
		}

		return $file_ary;
	}

	echo "OK";
?>	