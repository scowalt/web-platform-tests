(function () {
    'use strict';

    window.setup_frame_test = (test, numFrames) => {
        return new Promise((accept) => {
            const startTest = () => {
                window.addEventListener('message', (event) => {
                    log_test(event.data);
                });

                // Because 'by-design' we have little visibility into the state of the cross-origin <iframe>,
                // we must rely on a timeout for negative tests.  This one second delay gives nested <iframes>
                // that were unintentionally loaded a time frame in which they can 'postMessage' and fail the
                // test case.
                setTimeout(test.step_func(() => {
                    // Because 'frame-ancestors' tests do not include 'checkReport.sub.js', we need to manually notify
                    // 'logTest.sub.js' that we're ready to verify the log. 
                    window.log_ready();

                    // Finally, let the caller know it's safe to begin sending messages to child <iframe>s.
                    accept();
                }), 1000);
            };

            if (numFrames > 0) {
                let numReceived = 0;

                const listener = test.step_func(() => {
                    assert_equals(event.data, 'start test',
                        `Must receive 'start test' from all ${numFrames} <iframes> prior to other messages.`);

                    numReceived++;
                    if (numReceived === numFrames) {
                        window.removeEventListener('message', listener);
                        startTest();
                    }
                });
                    
                window.addEventListener("message", listener, false);
            } else {
                startTest();
            }
        });
    }
}());