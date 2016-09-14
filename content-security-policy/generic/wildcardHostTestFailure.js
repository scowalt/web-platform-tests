'use strict';

window.wildcardHostTestRan = false;

onload = function() {
    test(function() {
        assert_false(window.wildcardHostTestRan, 'Script should not have ran.');
    }, "Wildcard host matching works.");
};
