// ==UserScript==
// @name         Bilibili Linux Read URL Fix
// @version      0.1
// @description  Redirect mobile read page to PC read page
// @author       YidaozhanYa
// @match        *://www.bilibili.com/read/mobile?*
// @icon         https://bilibili.com/favicon.ico
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    var re=/mobile\?id=/;
    var url=window.location.href;
    if (re.test(url)) {
        window.location.href=url.replace('mobile?id=','cv');
    }
    // Your code here...
})();
