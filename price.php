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
	$mystring = exec('/home/[USER]/pymodules/Python-3.3.3/python /home/[USER]/pymodules/Python-3.3.3/bitcoin-wp.py');
	file_put_contents($file,$mystring);
    return $mystring;
  }
}

echo price();

?>
