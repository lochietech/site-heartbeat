<?php
$txt = date('Y/m/d H:i:s');
$myfile = fopen("heartbeat/site.txt", "w") or die("Unable to open file!");
fwrite($myfile, $txt);
fclose($myfile);
?>
