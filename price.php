<?php

function price()
{
  $file="./cache.txt";
  //echo $file;
  $current_time = time();
  $expire_time = 30;
  $file_time = filemtime($file);
  if(file_exists($file) && ($current_time - $expire_time < $file_time)) {
    //echo 'returning from cached file';
    return file_get_contents($file);
  }
  else
  {
	$mystring = exec('/home/[user]/pymodules/Python-3.3.3/python /home/[user]/pymodules/Python-3.3.3/bitcoin-wp.py');
	file_put_contents($file,$mystring);
    return $mystring;
  }
}

$im = @imagecreate(460, 100) or die("Cannot Initialize new GD image stream");
$message = price();
header("Content-type: image/png");

if ( $fromprice >99 )
    $image = imagecreatefrompng("background-134x26.png");
else
    $image = imagecreatefrompng("background-130x26.png");
$text_color = imagecolorallocate($image, 255, 0, 0);
imagestring($image, 3, 5, 5, $message, $text_color);
imagepng($image);
imagedestroy($image);

?>
