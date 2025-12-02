<?php

	$picture_folder = "uploads/";

?>

<!DOCTYPE html>
<html lang="de">

  <head>
  <link rel="icon" type="image/vnd.microsoft.icon" href="pics/favicon.ico"/>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="author" content="inno.space">

    <title>GIFy-Box</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

	<link href="https://fonts.googleapis.com/css?family=Open+Sans:400,600" rel="stylesheet">
	<style type="text/css">
		html, body {
			padding: 0;
			margin: 0;
			min-height: 100%;
			font-family: 'Open Sans', sans-serif;
			background-color: #000;
		}

		.page-header {
			text-align: center;
			color: #ffffff;
			border-bottom: 1px solid #fff;
		}

		.page-footer {
			text-align: center;
			color: #ffffff;
			border-top: 1px solid #fff;
			padding: 15px 0;
		}

		h1 {
			font-weight: 600;
			color: #EB6219;
		}

		.gif {
			cursor: pointer;
			padding: 5px;
		}

		.gif img {
			width: 100%;
			height: auto;
		}

    </style>
    <script>
            setTimeout(function(){
                window.location.reload(1);
            }, 20000);
        </script>
  </head>

  <body>
    <div class="container">

      <div class="page-header">
        <h1>GIFy-Box</h1>
        <h4>All animations are presented by <a href="https://inno-space.de">inno.space</a> Design Factory Mannheim</h4>
      </div>

      <div id="gifline" class="row">
      	<?php

			$files = glob('uploads/*');
			usort($files, function($a, $b) {
			    return filemtime($a) < filemtime($b);
			});

			//$files = scandir($picture_folder);
			foreach($files as $file) {
				if($file == "." || $file == "..") continue;

				?>
					<a class="col-md-4 col-sm-6 col-xs-6 gif" href="/y<?= str_replace("uploads/", "", $file) ?>">
						<img src="/xg<?= str_replace("uploads/", "", $file) ?>">
					</a>
				<?php
			}
      	?>
        
      </div>

      <div class="page-footer">
        one of many projects by <a href="https://inno-space.de">inno-space</a>
      </div>

    </div> <!-- /container -->


    <script src="https://code.jquery.com/jquery-3.1.0.min.js" integrity="sha256-cCueBR6CsyA4/9szpPfrX3s49M9vUU5BgtiJj06wt/s=" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

  </body>
</html>
