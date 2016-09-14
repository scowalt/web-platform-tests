'use strict';

window.wildcardHostTestRan = false;

onload = function() {
    test(function() {
        assert_true(window.wildcardHostTestRan, 'Script should have ran.');
    }, "Wildcard host matching works.");
};
