function extractDataFromUrl(url) {
  const regex = /@(-?\d+\.\d+),(-?\d+\.\d+),(\d+a),(\d+y),(\d+\.\d+)h,(\d+t)/;
  const match = url.match(regex);

  if (match && match[1] && match[2] && match[3] && match[4] && match[5] && match[6]) {
    return {
      latitude: parseFloat(match[1]),
      longitude: parseFloat(match[2]),
      altitude: parseFloat(match[3].slice(0, -1)),
      fov: parseInt(match[4].slice(0, -1)),
      heading: parseFloat(match[5]),
      tilt: parseInt(match[6].slice(0, -1)),
    };
  }

  return null;
}


async function display() {
  console.log("display() function running");
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
          if (response.success) {
            peakDisplayer.innerHTML = JSON.stringify(response.peaks);
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
