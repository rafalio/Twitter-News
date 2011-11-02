<?php
$cutoffLength = 100;
if(isset($_GET['id'])){
	$id = $_GET['id'];
	$news_json = json_decode(file_get_contents("http://legendof.me:5000/api/1/story/$id/short"), true);
//	print_r($news_json);
	$truncated = $news_json['short_summary'];
	if(strlen($truncated) > $cutoffLength){
		$truncated = substr($truncated, 0, strpos($truncated, ' ', $cutoffLength)) . "...";
	}
	echo '<div><h1>' . $news_json['title'] . '</h1><p>' . $truncated . '</p></div>';
}
?>