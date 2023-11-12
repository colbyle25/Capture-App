var map;
var markers = [];
var currentMarker;
var currentInfoWindow = null;
var admView = false;
var preid = 0;



function initMap() {
    fetch("/amiadmin/").then(response => response.json()).then(data => {admView = data.admin;});
    console.log("initializing");
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
        placeNewMarker(event.latLng);
    });

    // Loads the markers whenever the map is loaded
    LoadMarkers();
}

function placeNewMarker(location) {
    //https://stackoverflow.com/questions/3684274/googlemaps-v3-api-create-only-1-marker-on-click
    if (currentMarker)
    {
        currentMarker.setPosition(location);
        console.log("Marker moved", currentMarker);
        return;

    }
    else{
        currentMarker = new google.maps.Marker({
            position: location,
            map: map,
            draggable: true,  // Allows users to drag and adjust the marker position if desired
            // content: pinUnapproved,
            icon: {url: "https://maps.google.com/mapfiles/kml/shapes/info_circle.png", scaledSize: new google.maps.Size(40, 40) },
        })
        currentMarker.protoid = preid++;
        currentMarker.userMessage = "";
        currentMarker.approved = false;
    }
    var marker = currentMarker;

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

// Method for placing database markers.
function placeMarker(location, message, id, likes, liked, approved) {
    console.log("Placing from db", id);

    var marker = new google.maps.Marker({
        position: location,
        map: map,
        draggable: false,
        // content: approved ? pinApproved : pinUnapproved,
    })
    if (!approved) marker.setIcon({url: "https://maps.google.com/mapfiles/kml/shapes/info_circle.png", scaledSize: new google.maps.Size(40, 40) });

    marker.id = id;
    marker.userMessage = message ? message : "";
    marker.likes = likes;
    marker.liked = liked;
    marker.approved = approved;

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

function Like(id) {
    fetch(`/like/${id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': CSRF_TOKEN
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Message liked:', data);
        var marker = markers.find(marker => marker.id === id);
        marker.likes += 1;
        marker.liked = true;
        if (currentInfoWindow) {
            currentInfoWindow.setContent(generateContentString(marker, marker.getPosition()));
        }
    })
    .catch(error => {
        console.error('Error during like:', error);
    });
}

function Unlike(id) {
    fetch(`/unlike/${id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': CSRF_TOKEN
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Message unliked:', data);
        var marker = markers.find(marker => marker.id === id);
        marker.likes -= 1;
        marker.liked = false;
        if (currentInfoWindow) {
            currentInfoWindow.setContent(generateContentString(marker, marker.getPosition()));
        }
    })
    .catch(error => {
        console.error('Error during unlike:', error);
    });
}

function Approve(id) {
    fetch(`/approve/${id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': CSRF_TOKEN
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Message approved:', data);
        var marker = markers.find(marker => marker.id === id);
        marker.approved = true;
        // marker.content = pinApproved;
        marker.setIcon(null);
        if (currentInfoWindow) {
            currentInfoWindow.setContent(generateContentString(marker, marker.getPosition()));
        }
    })
    .catch(error => {
        console.error('Error during approval:', error);
    });
}

function Unapprove(id) {
    fetch(`/unapprove/${id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': CSRF_TOKEN
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Message unapproved:', data);
        var marker = markers.find(marker => marker.id === id);
        marker.approved = false;
        // marker.content = pinUnapproved;
        marker.setIcon({url: "https://maps.google.com/mapfiles/kml/shapes/info_circle.png", scaledSize: new google.maps.Size(40, 40) });
        if (currentInfoWindow) {
            currentInfoWindow.setContent(generateContentString(marker, marker.getPosition()));
        }
    })
    .catch(error => {
        console.error('Error during approval:', error);
    });
}

function generateContentString(marker) {
    var contentString = '<div class="infoWindowContent">';

    if (marker.userMessage === "") { // If there's no saved message, show textarea
        contentString += 'Write a Message! ' + '<br>';
        contentString += '<textarea id="userMessage_' + marker.protoid + '" class="userMessageTextarea"></textarea><br>';
        contentString += '<input type="button" class="saveButton" onclick="SaveMessage(' + marker.protoid + ');" value="Submit for Approval">';
    } else {
        marker.likes = marker.likes ? marker.likes : 0;
        marker.liked = marker.liked ? marker.liked : false;
        contentString += marker.userMessage + '<br>';
        contentString += marker.likes + " likes -- ";
        if (!marker.liked) {
            contentString += '<input type="button" class="saveButton" onclick="Like(' + marker.id + ');" value="Like">';
        } else {
            contentString += '<input type="button" class="saveButton" onclick="Unlike(' + marker.id + ');" value="Unlike">';
        }
        contentString += '<br>';
        if (admView) {
            if (!marker.approved) {
                contentString += '<input type="button" class="saveButton" onclick="Approve(' + marker.id + ');" value="Approve">';
            } else {
                contentString += '<input type="button" class="saveButton" onclick="Unapprove(' + marker.id + ');" value="Unapprove">';
            }
            contentString += '<br>';
            contentString += '<input type="button" class="deleteButton" onclick="DeleteMarker(' + marker.id + ');" value="Delete">';
            contentString += '<br>';
        }
    }

    // contentString += '<input type="button" class="deleteButton" onclick="DeleteMarker(' + marker.id + ');" value="Delete">';
    // removed delete button for now
    contentString += '</div>';

    return contentString;
}

function SaveMessage(protoid) {
    var marker = markers.find(m => m.protoid === protoid);
    if (marker) {
        var userMessage = document.getElementById('userMessage_' + protoid).value;
        var postData = {
            'latitude': marker.getPosition().lat(),
            'longitude': marker.getPosition().lng(),
            'message': userMessage
        };

        fetch('/save_marker/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                marker.id = data.id;
                marker.userMessage = userMessage;
                marker.approved = false;
                marker.likes = 0;
                marker.liked = false;
                if (currentInfoWindow) {
                    currentInfoWindow.setContent(generateContentString(marker, marker.getPosition()));
                }
            } else {
                console.error('Failed to save marker:', data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    currentMarker = null;
}

function DeleteMarker(id) {
    if (currentMarker) {
        currentMarker.setMap(null);
        currentMarker = null;
        return;
    }
    fetch(`/delete_marker/${id}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': CSRF_TOKEN
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Marker deleted:', data);
        const markerToDelete = markers.find(marker => marker.id === id);
        if (markerToDelete) {
            markerToDelete.setMap(null);
        }
        markers = markers.filter(marker => marker.id !== id);
    })
    .catch(error => {
        console.error('Error during deletion:', error);
    });
}

function LoadMarkers() {
    fetch('/load_markers/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        data.forEach(Message => {
            const position = new google.maps.LatLng(Message.latitude, Message.longitude);
            placeMarker(position, Message.message, Message.id, Message.likes, Message.liked, Message.approved);
        });
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}