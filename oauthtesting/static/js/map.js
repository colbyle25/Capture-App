var map;
var markers = [];
var uniqueID = 0;
var currentInfoWindow = null;
const MAX_MARKERS = 3;


function initMap() {

    account_image = document.images;
    img = 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/b91ae6af-3261-4f95-990e-4896507279ad/d5jzig1-3bd05d51-8646-443c-9030-600bd5eaf473.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2I5MWFlNmFmLTMyNjEtNGY5NS05OTBlLTQ4OTY1MDcyNzlhZFwvZDVqemlnMS0zYmQwNWQ1MS04NjQ2LTQ0M2MtOTAzMC02MDBiZDVlYWY0NzMucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.js96fjW1bMXaPF6fzpgHOc6xbsL7CsSqU1Nit2OEGwA';
    if (account_image[0]) {
        img = account_image[0].src;
    }

    map = new google.maps.Map(document.getElementById('UVA_MAP'), {
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
            url: img,
            //url: 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/b91ae6af-3261-4f95-990e-4896507279ad/d5jzig1-3bd05d51-8646-443c-9030-600bd5eaf473.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2I5MWFlNmFmLTMyNjEtNGY5NS05OTBlLTQ4OTY1MDcyNzlhZFwvZDVqemlnMS0zYmQwNWQ1MS04NjQ2LTQ0M2MtOTAzMC02MDBiZDVlYWY0NzMucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.js96fjW1bMXaPF6fzpgHOc6xbsL7CsSqU1Nit2OEGwA',
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
    google.maps.event.addListener(map, 'click', function(event) {
        placeMarker(event.latLng);
    });
}
function placeMarker(location) {
    if (markers.length >= MAX_MARKERS){
        alert("You can only place " + MAX_MARKERS + " markers at a time.");
        return;
    }

    var marker = new google.maps.Marker({
        position: location,
        map: map,
        draggable: true  // Allows users to drag and adjust the marker position if desired
    })

    marker.id = uniqueID;
    marker.userMessage = "";
    uniqueID += 1;

    google.maps.event.addListener(marker, "click", function (e) {
        var contentString = generateContentString(marker, location);
        var infoWindow = new google.maps.InfoWindow({
            content: contentString
        });
        if (currentInfoWindow) {
        currentInfoWindow.close();
    }
        infoWindow.open(map, marker);
        currentInfoWindow = infoWindow;
    });

    markers.push(marker);
}
function generateContentString(marker, location) {
    var contentString = '<div class="infoWindowContent">';

    if (marker.userMessage === "") { // If there's no saved message, show textarea
        contentString += 'Write a Message! ' + '<br>';
        contentString += '<textarea id="userMessage_' + marker.id + '" class="userMessageTextarea"></textarea><br>';
        contentString += '<input type="button" class="saveButton" onclick="SaveMessage(' + marker.id + ');" value="Save">';
    } else {
        contentString += marker.userMessage + '<br>';
    }

    contentString += '<input type="button" class="deleteButton" onclick="DeleteMarker(' + marker.id + ');" value="Delete">';
    contentString += '</div>';

    return contentString;
}

function SaveMessage(id) {
    var marker = markers.find(m => m.id === id);
    if (marker) {
        marker.userMessage = document.getElementById("userMessage_" + id).value
        if (currentInfoWindow) {
            currentInfoWindow.close();
        }
        var contentString = generateContentString(marker, marker.getPosition());
        var infoWindow = new google.maps.InfoWindow({
            content: contentString
        });
        infoWindow.open(map, marker);
    }
}

function DeleteMarker(id) {
    for (var i = 0; i < markers.length; i++) {
        if (markers[i].id == id) {
            markers[i].setMap(null);
            markers.splice(i, 1);
            return;
        }
    }
}