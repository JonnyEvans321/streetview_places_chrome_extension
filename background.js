chrome.webRequest.onCompleted.addListener(async (request) => {
    // Your existing webRequest listener code here
  }, {urls: ['<all_urls>']});
  
//   chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
//     if (request.action === 'fetchPeaks') {
//       const { latitude, longitude } = request;
//       fetch(`http://127.0.0.1:5000/get_peaks?latitude=${latitude}&longitude=${longitude}`)
//         .then((response) => {
//           if (response.ok) {
//             return response.json();
//           } else {
//             throw new Error("Failed to fetch nearby mountain peaks/summits.");
//           }
//         })
//         .then((peaks) => {
//           sendResponse({ success: true, peaks });
//         })
//         .catch((error) => {
//           console.error(error);
//           sendResponse({ success: false });
//         });
  
//       return true; // This line is important, it keeps the message channel open for asynchronous response
//     }
//   });
  


chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
if (request.action === "fetchPeaks") {
    const { latitude, longitude, fov, tilt } = request;
    fetch(
    `http://127.0.0.1:5000/get_peaks?latitude=${latitude}&longitude=${longitude}&fov=${fov}&tilt=${tilt}`
    )
    .then((response) => response.json())
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