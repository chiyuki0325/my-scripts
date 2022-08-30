// ==UserScript==
// @name         WAP URL Fixes
// @version      0.2
// @description  Redirect some wap pages to PC pagesfor Linux users
// @author       YidaozhanYa
// @match        *://www.bilibili.com/read/mobile?*
// @match        *://*.m.wikipedia.org/*
// @match        *://*.m.wiktionary.org/*
// @icon         https://www.kernel.org/theme/images/logos/favicon.png
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    //bilibili
    var re=/mobile\?id=/;
    var url=window.location.href;
    if (re.test(url)) {
        window.location.href=url.replace('mobile?id=','cv');
    }
    re=/m\.wik/;
    if (re.test(url)) {
        window.location.href=url.replace('m.wik','wik');
    }
    // Your code here...
})();
