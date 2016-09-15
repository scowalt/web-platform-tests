(function() {
    'use strict';

    // Note: We rely on wptserve substitution to embed the query parameters of the <script> src URL
    //       used to import this file.  (We do not use the current document, as that would instead
    //       return the query parameters of the test page.)
    //
    // Danger: The query parameters are unencoded, so technically, this constitutes an injection
    //         vulnerability.

    const reportField = "{{GET[reportField]}}";
    const reportValue = "{{GET[reportValue]}}";
    const reportExists = "{{GET[reportExists]}}" !== 'false';
    const noCookies = "{{GET[noCookies]}}";

    const location = window.location;
    const timeout = document.querySelector("meta[name=timeout][content=long]") ? 50 : 5;

    let reportID;

    const thisTestName = location.pathname.split('/')[location.pathname.split('/').length - 1].split('.')[0];
    const cookiePath = document.location.pathname.substring(0, document.location.pathname.lastIndexOf('/') + 1);
    const cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        const nameValuePair = cookies[i].split('='); 
        const cookieName = nameValuePair[0].trim();
        const cookieValue = nameValuePair[1].trim();

        if (cookieName === thisTestName) {
            const cookieToDelete = cookieName + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=" + cookiePath;
            document.cookie = cookieToDelete;
            reportID = cookieValue;
            break;
        }
    }

    const reportLocation = location.protocol + "//" + location.host + "/content-security-policy/support/report.py?op=take&timeout=" + timeout + "&reportID=" + reportID;

    async_test((test) => {
        // If 'logTest.sub.js' was loaded, it implicitly awaits the violation report results before
        // completing log_tests.  Ensure that 'logTest.sub.js' will be notified that we've verified
        // the log, and that it should go ahead and complete.
        test.add_cleanup(() => {
            if (typeof window.log_ready !== 'undefined') {
                window.log_ready();
            }
        });

        const report = new XMLHttpRequest();
        report.onload = test.step_func(() => {
            const data = JSON.parse(report.responseText);

            if (data.error) {
                assert_false(reportExists, `Test Error: '/support/report.py' must return expected violation report. (Error: '${data.error}')`);
                test.done();
                return;
            } 

            assert_true(reportExists, 'User agent must not report a policy violation when none was exected.');

            // Firefox expands 'self' or origins in a policy to the actual origin value
            // so "www.example.com" becomes "http://www.example.com:80".
            // Accomodate this by just testing that the correct directive name
            // is reported, not the details...

            if (data["csp-report"] !== undefined && data["csp-report"][reportField] !== undefined) {
                assert_true(data["csp-report"][reportField].indexOf(reportValue.split(" ")[0]) !== -1,
                reportField + " value of  \"" + data["csp-report"][reportField] + "\" did not match " +
                reportValue.split(" ")[0] + ".");
            }

            test.done();
        });

        report.open("GET", reportLocation, true);
        report.send();
    }, reportExists
        ? `User agent must report expected ${reportField}: '${reportValue}'.`
        : 'User agent must not report a policy violation.');

    if (noCookies) {
        async_test((test) => {
            const cookieReport = new XMLHttpRequest();
            cookieReport.onload = test.step_func(() => {
                const data = JSON.parse(cookieReport.responseText);
                assert_equals(data.reportCookies, "None");
                test.done();
            });

            const cReportLocation = location.protocol + "//" + location.host + "/content-security-policy/support/report.py?op=cookies&timeout=" + timeout + "&reportID=" + reportID;
            cookieReport.open("GET", cReportLocation, true);
            cookieReport.send();
        }, "No cookies sent with report.");
    }
}());