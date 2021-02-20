<!DOCTYPE html>
<html>
  <head>
    <title>CloudComputing-HW1</title>
    <meta charset='utf-8'/>
    <script
      src="https://maps.googleapis.com/maps/api/js?key=%s&callback=initMap&libraries=&v=weekly"
      defer
    ></script>
    <link rel="stylesheet" type="text/css" href="./style.css" />
    <script src="./index.js"></script>
  </head>
  <body>
    <div id="map"></div>
    <div id="dates">
      <div class="date-io">
        <label for="start">Start date:</label>
        <input type="date" id="start" name="trip-start"
              value="2021-02-23"
              min="2021-02-23" max="2021-12-31">
      </div>
      <div class="date-io">
        <label for="end">End date:</label>
        <input type="date" id="end" name="trip-end"
              value="2021-02-23"
              min="2021-02-23" max="2021-12-31">
      </div>
    </div>
  </body>
</html>