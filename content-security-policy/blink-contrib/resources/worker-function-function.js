var fn = function() {
    postMessage('Function() function blocked');
};
try {
    /* eslint no-new-func: "off" */
    fn = new Function("", "postMessage('Function() function allowed');");
} catch (e) {}
fn();
