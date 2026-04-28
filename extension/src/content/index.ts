// Content script: signals to background that user is on a call domain so
// the action icon can be highlighted. Kept tiny to avoid impacting calls.
chrome.runtime.sendMessage({ type: "DETECT_CALL", url: location.href }).catch(() => {});
