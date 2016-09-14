'use strict';

document.write("<script>log_test('Pass 1 of 2');</script>");

var s = document.createElement('script');
s.textContent = "log_test('Pass 2 of 2');";
document.body.appendChild(s);
