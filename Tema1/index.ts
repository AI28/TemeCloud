function initMap(){
  const iasi = { lat: 47.158455, lng: 27.601442 };
  const map = new google.maps.Map(
    document.getElementById("map"),
    {
      zoom: 4,
      center: iasi,
    }
  );

  let infoWindow = new google.maps.InfoWindow({
    content: "Apasa pe locul in care vrei sa mergi in vacanta!",
    position: iasi
  });

  infoWindow.open(map);

  map.addListener("click", (mapsMouseEvent) => {
    infoWindow.close();

    infoWindow = new google.maps.InfoWindow({
      position: mapsMouseEvent.latLng
    });

    const request = new XMLHttpRequest();
    const coordinates = infoWindow.position.toUrlValue().split(',');
    request.open("GET",`http://localhost:8000/api/v1/weather?lat=${coordinates[0]}&lon=${coordinates[1]}`); 

    request.onload = function(){
      if(this.status == 200){

        let weatherJson = JSON.parse(this.responseText);

        infoWindow.setContent(JSON.stringify(weatherJson.main), null, 2);

        const marker = new google.maps.InfoWindow({
          position: infoWindow.position,
          map,
        });

        infoWindow.open(map,marker);

      }
      else{
        console.log(this.responseText)
      }
    }
    request.send();


  });

}
