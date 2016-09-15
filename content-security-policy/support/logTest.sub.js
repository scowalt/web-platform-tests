(function () {
    'use strict';

    // Note: We rely on wptserve substitution to embed the query parameters of the <script> src URL
    //       used to import this file.  (We do not use the current document, as that would instead
    //       return the query parameters of the test page.)
    //
    // Danger: The query parameters are unencoded, so technically, this constitutes an injection
    //         vulnerability.
    const expected_logs = {{GET[logs]}};

    const t_log = async_test((test) => {
        // This test awaits two conditions:
        //
        //      1) We have observed all expected calls to log_test(...).
        //
        //      2) The suite has called 'log_ready()' to declare that all test steps that might
        //         generate logs have run.
        //
        // The following Promise.all(...) joins these two conditions.  We then  invokes 'test.done()'
        // when the joined Promise completes.
        Promise.all([
            new Promise((accept) => {
                // If no logs are expected, fulfill the promise now as log_test() should never be invoked.
                if (expected_logs.length === 0) {
                    accept();
                }

                // Expose a global 'log_test()' function that is used by the test suite to log test events.
                // Once all expected events have been observed, this Promise is fulfilled. 
                window.log_test = test.step_func((msg) => {
                    // Messages that begin with 'FAIL' are implicitly assumed to always fail the test.
                    assert_true(msg.match(/^FAIL/i) === null,
                        `log_test(): ${msg}`);

                    // Find the given 'msg', remove it from the list of remaining logs we expect, and return.
                    for (var i = 0; i < expected_logs.length; i++) {
                        if (expected_logs[i] === msg) {
                            assert_true(expected_logs[i] === msg);
                            expected_logs.splice(i, 1);

                            // If there are no more expected logs left, fulfill the Promise.
                            if (expected_logs.length === 0) {
                                accept();
                            }
                            return;
                        }
                    }

                    // If we did not early exit from the loop above, the 'msg' was not expected.  Fail the test.
                    assert_unreached(`Unexpected log: '${msg}'.`);
                });
            }),
            new Promise((accept) => {
                let isReady = false;
                
                // Expose a global 'log_ready()' function that signals us that we're ready to complete
                // this test once all expected log entries are arrived.
                //
                // Typically, this is invoked by 'checkReport.sub.js', since we assume that once the
                // violation report has been verified, we have completed running all test stops that
                // might generate failures.
                window.log_ready = () => {
                    assert_false(isReady,
                        "'log_ready()' must only be invoked once.");
                    isReady = true;
                    accept();
                };
            })
        ]).then(test.step_func(() => {
            test.done();
        }));
    }, 'Expecting logs: {{GET[logs]}}');

    // Expose a global function to explicitly set the test to 'NOT RUN' with the given 'reason'.
    // This is used to skip tests for features that are not supported by the user agent.
    window.skip_log_test = (reason) => {
        t_log.set_status(t_log.NOTRUN, reason);
        t_log.phase = t_log.phases.HAS_RESULT;
        t_log.done();
    };
}());