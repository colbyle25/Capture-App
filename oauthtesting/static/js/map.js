function initMap() {
    
    var map = new google.maps.Map(document.getElementById('UVA_MAP'), {
        center: {lat: 38.03358840942383, lng: -78.50801849365234}, //default center is central grounds
        zoom: 16,
        styles: [    
            {
                featureType: "poi",
                elementType: "labels",
                stylers: [{ visibility: "off" }]
            }
        ] //hide the default points of interest
    });

    var locationMarker = new google.maps.Marker({
        map: map,
        title: "Your Location",
        icon: {
            //potentially make the icon url the user's profile picture
            url: 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/b91ae6af-3261-4f95-990e-4896507279ad/d5jzig1-3bd05d51-8646-443c-9030-600bd5eaf473.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2I5MWFlNmFmLTMyNjEtNGY5NS05OTBlLTQ4OTY1MDcyNzlhZFwvZDVqemlnMS0zYmQwNWQ1MS04NjQ2LTQ0M2MtOTAzMC02MDBiZDVlYWY0NzMucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.js96fjW1bMXaPF6fzpgHOc6xbsL7CsSqU1Nit2OEGwA',
            scaledSize: new google.maps.Size(50, 50),
        },
        zIndex: 1000 //make sure it renders above a POI marker in the same place
    });
    
    /*update the location: readjust the location/avatar marker and re-center the map*/
    function updateLocation(position) {
        var location = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        locationMarker.setPosition(location);
        map.setCenter(location);
    }

    /*watchPosition should continually call an updatePosition as the user moves around*/
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) { //set the initial position before watching for changes
                updateLocation(position);
                var watchId = navigator.geolocation.watchPosition(updateLocation, 
                    function (error) {
                        console.error('Error getting user location:', error);
                    }
                );
            }, 
            function (error) {
                console.error('Error getting user location:', error);
            },
            {
                timeout: 10000 //10 seconds to find the initial location before throwing error
            }
        );
    } else {
        var errorWindow = new google.maps.InfoWindow();
        errorWindow.setPosition(locationMarker.getPosition());
        errorWindow.setContent('Insufficient location/geolocation permissions.');
        errorWindow.open(map);
    }

    /*render a UVA logo marker for each point of interest in the database. POIs is passed from the template.*/
    pois.forEach(function(poi) {
        console.log(poi.name)
        console.log(poi.points)
        console.log(poi.pid)
        console.log(poi.latitude)

        var marker = new google.maps.Marker({
            position: { lat: parseFloat(poi.latitude), lng: parseFloat(poi.longitude) },
            map: map,
            title: poi.name,
            label: poi.name,
            icon: {
                url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/archive/d/dd/20170128002300%21University_of_Virginia_Rotunda_logo.svg/118px-University_of_Virginia_Rotunda_logo.svg.png',
                scaledSize: new google.maps.Size(50, 50)
            }
        });
    
        var markerWindow = new google.maps.InfoWindow({
            maxWidth: 200,
            content: '<img style = "width: 95%; display: flex; margin: auto;" src= "' + poi.img + '"></img>'
                    +'<div style = "padding-top: 10px; font-family: Lato; text-align: center; color: green; font-size: 1 em;">' + 'points: ' + poi.points + '</div>'
                    +'<div style = "padding-top: 10px; font-family: Lato; text-align: center; color: black; font-size: 1 em;">' + 'last message: ' + poi.time + '</div>'
        });
    
        marker.addListener('click', function () {
            markerWindow.open(map, marker);
        });
    });
}