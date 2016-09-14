'use strict';

window.wildcardPortTestRan = false;

onload = function() {
    test(function() {
        assert_true(window.wildcardPortTestRan, 'Script should have ran.');
    }, "Wildcard port matching works.");
};