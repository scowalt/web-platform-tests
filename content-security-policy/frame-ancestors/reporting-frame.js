(function () {
    'use strict';

    const log = document.createElement('pre');
    document.body.appendChild(log);

    // Display any received messages in the above <pre>, and echo them to the parent
    // who will confirm they match the test's expectations.
    window.addEventListener("message",
        (event) => {
            log.textContent += event.data + '\n'; 
            window.parent.postMessage(event.data, "*");
        }, false);
}());