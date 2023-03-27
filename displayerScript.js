function extractDataFromUrl(url) {
  console.log(url);
  const regex = /@(-?\d+\.\d+),(-?\d+\.\d+),(\d+\.?\d*)[az]?,(\d+\.?\d*)[ay]?,(\d+\.?\d*)h?,(\d+\.?\d*)t?.*data=([^&]+)/;
  const match = url.match(regex);
  console.log(match);

  if (match && match[1] && match[2] && match[3] && match[4] && match[5]) {
    return {
      latitude: parseFloat(match[1]),
      longitude: parseFloat(match[2]),
      fov: parseInt(match[3]),
      heading: parseFloat(match[4]),
      tilt: parseFloat(match[5]),
    };
  }

  return null;
}
async function display() {
  const coordDisplayer = document.querySelector("#coordDisplayer");
  const peakDisplayer = document.querySelector("#peakDisplayer");

  // Fetch the current URL and extract the data from it
  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const url = tabs[0].url;
    const data = extractDataFromUrl(url);

    if (data !== null) {
      const { latitude, longitude, fov, heading, tilt } = data;

      coordDisplayer.innerHTML = JSON.stringify([latitude, longitude]);

      const headingDisplayer = document.querySelector("#headingDisplayer");
      headingDisplayer.innerHTML = JSON.stringify(heading);
      console.log("Orientation:", heading);

      // Request data from the background script
      chrome.runtime.sendMessage(
        { action: "fetchPeaks", latitude, longitude, fov, tilt },
        (response) => {
          console.log(response);
          if (response.success) {
            try {
              const peaks = response.peaks;
              peakDisplayer.innerHTML = JSON.stringify(peaks);
              console.log("Peaks:", peaks);
              console.log('First peak', peaks[0]);

              // Place a red marker on the user's screen for each peak
              for (let peak of peaks) {
                const { latitude: peakLat, longitude: peakLon, altitude } = peak;
                const markerUrl = chrome.runtime.getURL("marker.png");
                const markerSize = 40;
                const x = window.innerWidth / 2;
                const y = window.innerHeight / 2;
                const markerStyle = `position: absolute; left: ${x - markerSize / 2}px; top: ${y - markerSize / 2}px; width: ${markerSize}px; height: ${markerSize}px; background-image: url(${markerUrl}); background-size: contain; z-index: 999999;`;
                const marker = document.createElement("div");
                marker.style = markerStyle;
                // document.body.appendChild(marker);
              }
            } catch (error) {
              console.error("Failed to parse JSON data from the Flask API:", error);
            }
          } else {
            console.error("Failed to fetch nearby mountain peaks/summits.");
          }
        }
      );
    } else {
      console.error("Data not found in the URL.");
    }
  });
}

display();
