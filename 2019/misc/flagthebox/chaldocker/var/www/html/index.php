<!DOCTYPE html>
<html>
<head>
<style>
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

li a:hover {
  background-color: #111;
}

body {
  background-color: #d0d0d0;
}
</style>
</head>
<body>

<ul>
  <li><a href="/">Home</a></li>
  <li><a href="/?page=about.php">About</a></li>
  <li><a href="/?page=contact.php">Contact</a></li>
  <li><a href="/?page=admin.php">Admin</a></li>
</ul>

<?php
$page = isset($_GET['page']) ? $_GET['page'] : "main.php";

if (strpos($page, "index.php") !== false) {
  $page = "main.php";
}

if (isset($_POST['first_name'])) {
  echo "<p style='color:green'>We've received your message, thanks for your interest.</p>";
}

echo file_get_contents($page);
?>

</body>
</html>
