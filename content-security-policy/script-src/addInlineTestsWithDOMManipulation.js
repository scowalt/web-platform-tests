(function() {
    var dmTest = async_test("DOM manipulation inline tests");
    var attachPoint = document.getElementById('attachHere');
    var inlineScript = document.createElement('script');
    var scriptText = document.createTextNode('dmTest.step(function() {assert_unreached("Unsafe inline script ran - createTextNode.")});');

    inlineScript.appendChild(scriptText);
    attachPoint.appendChild(inlineScript);

    document.getElementById('emptyScript').innerHTML = 'dmTest.step(function() {assert_unreached("Unsafe inline script ran - innerHTML.")});';
    document.getElementById('emptyDiv').outerHTML = '<script id=outerHTMLScript>dmTest.step(function() {assert_unreached("Unsafe inline script ran - outerHTML.")});</script>';

    document.write('<script>dmTest.step(function() {assert_unreached("Unsafe inline script ran - document.write")});</script>');
    document.writeln('<script>dmTest.step(function() {assert_unreached("Unsafe inline script ran - document.writeln")});</script>');

    dmTest.done();
})();
