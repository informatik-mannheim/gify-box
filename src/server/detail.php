<?php

	if(!isset($_GET["file"]) || $_GET["file"] == "") {
		die("No file name!");
	}

	// get the file name and sanitize it
	$animation_id = preg_replace("/[^a-zA-Z0-9_]/", "", $_GET["file"]);

?>

<!DOCTYPE html>
<html>
<head>
	<link rel="icon" type="image/vnd.microsoft.icon" href="pics/favicon.ico"/>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

	<title>GIFy-Box</title>
    <meta name="author" content="UXID">

	<meta property="og:title" content="GIFy-Box"/>
	<meta property="og:type" content="gif"/>
	<meta property="og:url" content="http://gifbox.ux-lab.xyz/y<?=$animation_id?>"/>
	<meta property="og:image" content="http://gifbox.ux-lab.xyz/xg<?=$animation_id?>"/>
	<meta property="og:site_name" content="GIFy-Box"/>
	<meta property="og:description" content="Check out this animation from the GIFy-Box"/>

	<link href="https://fonts.googleapis.com/css?family=Open+Sans:400,600" rel="stylesheet">
	<style type="text/css">
		html, body {
			padding: 0;
			margin: 0;
			height: 100%;
			overflow: hidden;
			font-family: 'Open Sans', sans-serif;
		}

		html {
			background-color: #000;
		}

		body {
			background: url('/xg<?=$animation_id?>') no-repeat center center fixed;
			-webkit-background-size: cover;
			-moz-background-size: cover;
			-o-background-size: cover;
			background-size: cover;
		}

		#header_overlay {
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			background-color: rgba(0, 0, 0, 0.35);
			color: #FFFFFF;

			text-align: center;
			padding: 10px;
		}

		#share_overlay {
			position: absolute;
			bottom: 0;
			left: 0;
			right: 0;
			background-color: rgba(0, 0, 0, 0.35);
			color: #FFFFFF;

			text-align: center;
			padding: 7px 0;
		}

		#share_overlay a {
			display: inline-block;
		}

		#share_overlay img {
			height: 32px;
		}

		a, a:visited {
			padding: 10px;
			color: #FFFFFF;
			text-decoration: none;
		}

		a:hover, a:active {
			padding: 10px;
			color: #FFFFFF;
			text-decoration: none;
			background-color: rgba(0, 0, 0, 0.65);
		}

	</style>
</head>

<body>

	<div id="header_overlay">
		<a href="/">
			&lt;&lt; &nbsp;  GIFy-Box
		</a>
	</div>

	<div id="share_overlay">
		<a target="_blank" href="http://www.facebook.com/sharer.php?u=http://gifbox.ux-lab.xyz/xg<?=$animation_id?>">
			<img src="/pics/facebook.png">
		</a>
		<a target="_blank" href="https://twitter.com/share?url=http://gifbox.ux-lab.xyz/y<?=$animation_id?>&amp;text=Look%20at%20my%20GIF&amp;hashtags=animatedgifbox">
			<img src="/pics/twitter.png">
		</a>
		<a target="_blank" href="/dlg<?=$animation_id?>">
			<img src="/pics/gif.png">
		</a>
		<a target="_blank" href="/dlm<?=$animation_id?>">
			<img src="/pics/mp4.png">
		</a>
	</div>

</body>

</html>