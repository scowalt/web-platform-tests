'use strict';

// This script block will trigger a violation report.
var i = document.createElement('img');
i.src = '/images/red.png';
document.body.appendChild(i);
log_test("TEST COMPLETE");
