<?php

	if(!isset($_GET["file"]) || $_GET["file"] == "") {
		die("No file name!");
	}

	// get the file name
	$animation_id = $_GET["file"];


?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>GIFy-Box</title>

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
			background-color: #000;
		}

		img {
			width: 100%;
			height: auto;
			position: absolute;
		    top: 0;
		    bottom: 0;
		    left: 0;
		    right: 0;
		    margin: auto;
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
			padding: 10px;
		}

		#share_overlay .share {
			margin-right: 20px;
		}

		#share_overlay .dimmed {
			color: #aaa;
			padding-left: 5px;
		}

		a, a:visited {
			padding: 3px 15px;
			color: #FFFFFF;
			text-decoration: none;
			margin-left: 10px;
		}

		a:hover, a:active {
			color: #000000;
			background-color:rgba(255, 255, 255, 0.7);
		}
		
	</style>
</head>

<body>
	<img src="/xg<?=$animation_id?>" />

	<div id="header_overlay">
		<a href="/">
			<small>go back to the</small> &nbsp;&nbsp;
			GIFy-Box
		</a>
	</div>

	<div id="share_overlay">
		<span class="share">share: </span>
		<a target="_blank" href="mailto:?Subject=Look%20at%20me%20jumping%20around&Body=Check%20out%20my%20GIF%20at%20http%3A//gifbox.ux-lab.xyz/y<?=$animation_id?>">E-Mail</a>
		<a target="_blank" href="http://www.facebook.com/sharer.php?u=http://gifbox.ux-lab.xyz/xg<?=$animation_id?>">Facebook</a>
		<a target="_blank" href="https://twitter.com/share?url=http://gifbox.ux-lab.xyz/y<?=$animation_id?>&amp;text=Look%20at%20my%20GIF&amp;hashtags=animatedgifbox">Twitter</a>
		<a target="_blank" href="/dlg<?=$animation_id?>">download GIF</a>
		<a target="_blank" href="/dlm<?=$animation_id?>">download MP4 <span class="dimmed">(Instagram)</span></a>
	</div>
</body>

</html>