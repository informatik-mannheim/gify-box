<?php
	
	// current id of this session (used to identify working dir)
	$id = ((isset($_GET["id"]) && $_GET["id"] != "") ? $_GET["id"] : "default");

	// get the working dir and all files in it
	$dir = "uploads/".$id."/";
	$files = array_diff(scandir($dir), array('..', '.'));

	// all the possible image prefixes
	// new prefixes should be added here
	$imagetypes = array("sw", "ye", "rd", "gr", "bl");

	// get the latest image for each prefix
	$latest_images = array();
	foreach ($files as $key => $value) {
		$latest_images[substr($value, 0, 2)] = $value;
	}

	// get the file location for a given prefix
	function getLatestImage($id) {
		global $dir, $latest_images;
		return $dir.$latest_images[$id];
	}

?>

<!DOCTYPE html PUBLIC "-//w3c//dtd html 4.0 transitional//en">
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="keywords" content="">
		<meta name="author" content="Wasili Adamow">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Portrait</title>

		<style type="text/css">
			html, body {
				margin: 0;
				padding: 0;
				background-color: #000;
				height: 100%;
				overflow: hidden;
			}

			.wrapper {
				margin: 0;
				padding: 0;
			}

			.item {
				background-repeat: no-repeat;
				background-position: center center;
				background-size: contain;
			}

			#default {
				position: relative;
			}

			#default .item {
				position: absolute;
			}

			#default #it0 {
				top: 290px;
				left: 112px;
				width: 394px;
				height: 701px;
			}

			#default #it1 {
				top: 88px;
				left: 559px;
				width: 239px;
				height: 425px;
			}

			#default #it2 {
				top: 566px;
				left: 559px;
				width: 239px;
				height: 425px;
			}

			#default #it3 {
				top: 290px;
				left: 851px;
				width: 394px;
				height: 701px;
			}

			#default #it4 {
				top: 88px;
				left: 1300px;
				width: 507px;
				height: 903px;
			}

			/** ADD STYLES FOR THE NEW ITEMS */
		</style>
	</head>

	<body>
		<div id="default" class="wrapper" style="display: block">
			<div id="it0" class="item"></div>
			<div id="it1" class="item"></div>
			<div id="it2" class="item"></div>
			<div id="it3" class="item"></div>
			<div id="it4" class="item"></div>
		</div>
	</body>

	<script src="//cdn.pubnub.com/pubnub-3.7.14.min.js"></script>
	<script>

	// GET data
	queryDict = {}
	location.search.substr(1).split("&").forEach(function(item) {queryDict[item.split("=")[0]] = item.split("=")[1]})
	var useshuffle = !(queryDict.fixed == 'true');

	// current working dir id
	var _id = '<?= $id ?>';

	// name of the cookie used to store the random image display
	var cookiename = "naeheportrait-fixed";

	// current random image display
	var rotation = [0,1,2,3,4];

	// all possible image type prefixes
	var imagetypes = ["sw", "ye", "rd", "gr", "bl"];

	// latest image file names for each prefix
	var latest_images = [<?php
			foreach ($imagetypes as $key => $value) {
				echo '"'.getLatestImage($value).'", ';
			}
		?>];

	// array to store a prefix with the latest file name
	var assoc = new Array();

	// load the pictures for the current random image display and store the file name in the assoc array
	function loadPictures() {
		for (c = 0; c < rotation.length; c++) {
			var i = rotation[c];
		    reloadSingle("it"+c, latest_images[i]);
		    assoc[imagetypes[i]] = "it"+c;
		}
	}

	// if the image display should be random, get the cookie for the rotation or do a new random rotation
	if(useshuffle) {
		var cookieval = getCookie(cookiename);
		if(!cookieval) {
			doShuffle();
		} else {
			rotation = cookieval.split(",");
			for(var i=0; i < rotation.length; i++) {rotation[i] = parseInt(rotation[i]);}
			loadPictures();
		}
	} else { // if not random: display the images in the original order
		loadPictures();
	}

	// pressing 's' shuffles the image display
	window.onkeyup = function(e) {
		var key = e.keyCode ? e.keyCode : e.which;
		if (key >= 83) { doShuffle() }
	}

	// message handler for Pubnub
	function handleMsg(m) {
		if(m["id"] == _id) { // is this the right working id?
			if(m["action"] == "reload") { // reload a single image
					for(var c = 0; c < latest_images.length; c++) {if(latest_images[c].indexOf(m["target"]) > -1) latest_images[c] = m["item"];}
					reloadSingle(assoc[m["target"]], m["item"]);
			} else if(m["action"] == "refresh") { // refresh the whole page
				location.reload();
			}
		}
	}

	//PUBNUB
	var pubnub = PUBNUB({
		subscribe_key: 'SUBSCRIBE_KEY'
	});
	pubnub.time(function(time){console.log(time)});
	pubnub.subscribe({
		channel: 'portrait_dev',
		message: function(m)	{console.log(m); handleMsg(m);},
		error: function (error) {console.log(JSON.stringify(error));}
	});

	// reload a single image container
	function reloadSingle(target, name) {
		document.getElementById(target).style.backgroundImage = "url('"+name+"')";
	}

	// shuffle the display elements and reload the images
	function doShuffle() {
		rotation = shuffle(rotation);
		loadPictures();
		setCookie(cookiename, rotation.toString(), 90);
	}

	// shuffle algorithm
	function shuffle(array) {
		var currentIndex = array.length, temporaryValue, randomIndex ;
		// While there remain elements to shuffle...
		while (0 !== currentIndex) {
			// Pick a remaining element...
			randomIndex = Math.floor(Math.random() * currentIndex);
			currentIndex -= 1;
			// And swap it with the current element.
			temporaryValue = array[currentIndex];
			array[currentIndex] = array[randomIndex];
			array[randomIndex] = temporaryValue;
		}
		return array;
	}


	// write and read cookies
	function setCookie(cname, cvalue, exdays) {
		var d = new Date();
		d.setTime(d.getTime() + (exdays*24*60*60*1000));
		var expires = "expires="+d.toUTCString();
		document.cookie = cname + "=" + cvalue + "; " + expires;
	}

	function getCookie(cname) {
		var name = cname + "=";
		var ca = document.cookie.split(';');
		for(var i=0; i<ca.length; i++) {
			var c = ca[i];
			while (c.charAt(0)==' ') c = c.substring(1);
			if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
		}
		return false;
	}
	</script>
</html>