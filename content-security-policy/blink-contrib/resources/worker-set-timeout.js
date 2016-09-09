'use strict';

var id = 0;
try {
    /* eslint no-implied-eval: "off" */
    id = setTimeout("postMessage('handler invoked')", 100);
} catch (e) {}
postMessage(id === 0 ? "setTimeout blocked" : "setTimeout allowed");
