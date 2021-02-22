function formatDate(date)
{

    formated_date = date.split("-").reverse();
    /*
    aux = formated_date[0]
    formated_date[0] = formated_date[1]
    formated_date[0] = aux
    */
    formated_date = formated_date.join("/");

    return formated_date;
}

function getElementValue(element_id)
{

    return document.getElementById(element_id).value;
}

function initMap()
{
  const iasi = { lat: 47.158455, lng: 27.601442 };
  const map = new google.maps.Map(
    document.getElementById("map"),
    {
      zoom: 4,
      center: iasi,
      mapTypeId: 'satellite'
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
    request.open("POST","http://172.17.4.60:8000/api/v1/prices"); 

    request.onload = function(){
      if(this.status == 200){

        let response_json = JSON.parse(this.responseText);

        infoWindow.setContent(JSON.stringify(response_json), null, 2);

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
    let start_date = getElementValue("start");
    let end_date = getElementValue("end");

    start_date = formatDate(start_date)
    end_date = formatDate(end_date)

    request_payload = {"lat": coordinates[0], "lon": coordinates[1], "from":start_date, "until":end_date}
    request.send(JSON.stringify(request_payload));

  });
}
