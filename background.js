chrome.webRequest.onCompleted.addListener(async (request) => {
    // Your existing webRequest listener code here
  }, {urls: ['<all_urls>']});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
if (request.action === "fetchPeaks") {
    const { latitude, longitude, fov, tilt } = request;
    fetch(
        `http://127.0.0.1:5000/get_peaks?latitude=${latitude}&longitude=${longitude}&fov=${fov}&tilt=${tilt}`
    )
    .then((response) => {
        console.log('Response from Flask API:', response);
        return response.json();
    })
    .then((peaks) => {
        sendResponse({ success: true, peaks });
    })
    .catch((error) => {
        console.error("Failed to fetch data from the Flask API:", error);
        sendResponse({ success: false });
    });
    

    return true;
}
});