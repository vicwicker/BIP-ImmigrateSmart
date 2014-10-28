<?php
	// Start session.
	session_start();
	
	// Set a key, checked in mailer, prevents against spammers trying to hijack the mailer.
	$security_token = $_SESSION['security_token'] = uniqid(rand());
	
	if ( ! isset($_SESSION['formMessage'])) {
		$_SESSION['formMessage'] = '<hr>';	
	}
	
	if ( ! isset($_SESSION['formFooter'])) {
		$_SESSION['formFooter'] = ' <hr>';
	}
	
	if ( ! isset($_SESSION['form'])) {
		$_SESSION['form'] = array();
	}
	
	function check($field, $type = '', $value = '') {
		$string = "";
		if (isset($_SESSION['form'][$field])) {
			switch($type) {
				case 'checkbox':
					$string = 'checked="checked"';
					break;
				case 'radio':
					if($_SESSION['form'][$field] === $value) {
						$string = 'checked="checked"';
					}
					break;
				case 'select':
					if($_SESSION['form'][$field] === $value) {
						$string = 'selected="selected"';
					}
					break;
				default:
					$string = $_SESSION['form'][$field];
			}
		}
		return $string;
	}
?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta name="generator" content="RapidWeaver" />
		
		<title>Contact | Affero</title>
		<link rel="stylesheet" type="text/css" media="all" href="../rw_common/themes/alpha/consolidated-13.css" />
		
		<!--[if IE 6]><link rel="stylesheet" type="text/css" media="screen" href="../rw_common/themes/alpha/ie6.css" />
		<![endif]-->
		
		
		
		<!--[if IE 6]><style type="text/css" media="screen">body {behavior: url(../rw_common/themes/alpha/csshover.htc);}</style><![endif]-->
				
				
		<script type="text/javascript" src="../rw_common/themes/alpha/javascript.js"></script>
		
		<!--[if IE 6]><script type="text/javascript" charset="utf-8">
			var blankSrc = "../rw_common/themes/alpha/png/blank.gif";
		</script>	
		<style type="text/css">
			img.pngfix {
				behavior:	url("../rw_common/themes/alpha/png/pngbehavior.htc");
			}
		</style><![endif]-->
		
		
	</head>
<body>
<div id="bodyGrad">
	<img class="pngfix" src="../rw_common/themes/alpha/images/body_grad.png" alt="" style="width: 3000px; height: 400px;" />
</div>
<div id="container"><!-- Start container -->
	<div id="pageHeader"><!-- Start page header -->
		<div id="grad"><img class="pngfix" src="../rw_common/themes/alpha/images/header_top_grad.png" alt="" style="width: 3000px; height: 72px;" /></div>
		<img src="../rw_common/images/1ld-logo" width="155" height="100" alt="Site logo"/>
		<h1>Affero</h1>
		<h2>Changing the world, one site at a time&hellip;</h2>
	</div><!-- End page header -->
	<div id="navcontainer"><!-- Start Navigation -->
		<ul><li><a href="../" rel="">Home</a></li><li><a href="../blog/" rel="">Blog</a></li><li><a href="../styled/" rel="">Other-Pages</a><ul><li><a href="../styled/photos/" rel="">Album</a></li><li><a href="../styled/downloads/" rel="">File Sharing</a></li><li><a href="../styled/code/" rel="">Sub-Pages</a><ul><li><a href="../styled/code/styled-2/" rel="">Page 1</a></li><li><a href="../styled/code/styled-4/" rel="">Page 2</a></li><li><a href="../styled/code/styled-3/" rel="">Page 3</a></li></ul></li></ul></li><li><a href="./" rel="" id="current">Contact</a></li></ul>
	</div><!-- End navigation -->
	<div class="clearer"></div>
	<div id="sidebarContainer"><!-- Start Sidebar wrapper -->
		<div id="sidebar"><!-- Start sidebar content -->
			<h1 class="sideHeader">Sidebar</h1><!-- Sidebar header -->
			<span style="font-size:14px; color:#909090;">Lorem ipsum dolor sit amet, sapien platea morbi dolor lacus nunc, nunc ullamcorper. Felis aliquet egestas vitae, nibh ante quis quis dolor sed mauris. Erat lectus sem ut lobortis, adipiscing ligula eleifend, sodales fringilla mattis dui nullam. Ac massa aliquet.</span><!-- sidebar content you enter in the page inspector -->
			 <!-- sidebar content such as the blog archive links -->
		</div><!-- End sidebar content -->
	</div><!-- End sidebar wrapper -->
	<div id="contentContainer"><!-- Start main content wrapper -->
		<div id="content"><!-- Start content -->
			
<div class="message-text"><?php echo $_SESSION['formMessage']; unset($_SESSION['formMessage']); ?></div><br />

<form action="./files/mailer.php" method="post" enctype="multipart/form-data">
	 <div>
		<label>Your Name</label> *<br />
		<input class="form-input-field" type="text" value="<?php echo check('element0'); ?>" name="form[element0]" size="40"/><br /><br />

		<label>Your Email</label> *<br />
		<input class="form-input-field" type="text" value="<?php echo check('element1'); ?>" name="form[element1]" size="40"/><br /><br />

		<label>Subject</label> *<br />
		<input class="form-input-field" type="text" value="<?php echo check('element2'); ?>" name="form[element2]" size="40"/><br /><br />

		<label>Message</label> *<br />
		<textarea class="form-input-field" name="form[element3]" rows="8" cols="38"><?php echo check('element3'); ?></textarea><br /><br />

		<div style="display: none;">
			<label>Spam Protection: Please don't fill this in:</label>
			<textarea name="comment" rows="1" cols="1"></textarea>
		</div>
		<input type="hidden" name="form_token" value="<?php echo $security_token; ?>" />
		<input class="form-input-button" type="reset" name="resetButton" value="Reset" />
		<input class="form-input-button" type="submit" name="submitButton" value="Submit" />
	</div>
</form>

<br />
<div class="form-footer"><?php echo $_SESSION['formFooter']; unset($_SESSION['formFooter']); ?></div><br />

<?php unset($_SESSION['form']); ?>
		</div><!-- End content -->
	</div><!-- End main content wrapper -->
	<div class="clearer"></div>
	<div id="footer"><!-- Start Footer -->
		<p>Theme by 1LD </p>
		<div id="breadcrumbcontainer"><!-- Start the breadcrumb wrapper -->
			
		</div><!-- End breadcrumb -->
	</div><!-- End Footer -->
</div><!-- End container -->
</body>
</html>
