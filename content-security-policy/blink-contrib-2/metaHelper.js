'use strict';

if (typeof aa !== 'undefined') {
    log_test(aa);
} else {
    log_test("Failed - allowed inline script blocked by meta policy outside head.");
}
