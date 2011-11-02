<?php
header('Content-type: application/json');
echo file_get_contents("http://legendof.me:5000/api/1/news");
?>