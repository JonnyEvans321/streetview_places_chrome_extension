// Create a new div element to represent the marker
const marker = document.createElement("div");
marker.style.position = "absolute";
marker.style.width = "10px";
marker.style.height = "10px";
marker.style.borderRadius = "50%";
marker.style.backgroundColor = "red";

// Get the container element for the page
const container = document.body;

// Add the marker to the container element
container.appendChild(marker);

// Set the position of the marker
marker.style.left = "50%";
marker.style.top = "50%";
