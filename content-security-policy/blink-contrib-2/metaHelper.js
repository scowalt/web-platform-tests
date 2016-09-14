'use strict';

if (typeof aa !== 'undefined') {
    log(aa);
} else {
    log("Failed - allowed inline script blocked by meta policy outside head.");
}
