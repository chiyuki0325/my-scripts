//Original code: https://gitlab.com/NickCao/experiments/-/blob/master/workers/r.js

addEventListener("fetch", event => {
    event.respondWith(handler(event.request));
});

String.prototype.fixScheme = function () {
    return this.replace(/(?<=^https?:)\/(?!\/)/, '//')
};

async function handler(request) {
    let origin = (new URL(request.url)).origin
    index = `<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0" charset="utf-8"><title>Cloudflare reverse proxy</title></head><style>body{height:100vh;display:flex;flex-direction:column;justify-content:center;}h1{font-size:4.6rem;line-height:1.2;font-weight:400;letter-spacing:-.1rem;margin-bottom:2.0rem;margin-top:0}*,*:after,*:before{box-sizing:inherit}html{box-sizing:border-box;font-size:62.5%}body{color:#606c76;font-family:'Roboto','Helvetica','Arial',sans-serif;font-size:1.6em;font-weight:300;letter-spacing:.01em;line-height:1.6}button{background-color:#9b4dca;border:0.1rem solid #9b4dca;border-radius:.4rem;color:#fff;cursor:pointer;display:inline-block;font-size:1.1rem;font-weight:700;height:3.8rem;letter-spacing:.1rem;line-height:3.8rem;padding:0 3.0rem;text-align:center;text-decoration:none;text-transform:uppercase;white-space:nowrap}button:focus,button:hover{background-color:#a56bc9;border-color:#a56bc9;color:#fff;outline:0}input,textarea,select{-webkit-appearance:none;background-color:transparent;border:0.1rem solid #d1d1d1;border-radius:.4rem;box-shadow:none;box-sizing:inherit;height:3.8rem;padding:.6rem 1.0rem .7rem;width:100%}input:focus,textarea:focus,select:focus{border-color:#9b4dca;outline:0}textarea{min-height:6.5rem}.container{margin:0 auto;max-width:112.0rem;padding:0 2.0rem;position:relative;width:100%}.row{display:flex;flex-direction:row;margin-left:-1.0rem;width:calc(100% + 2.0rem);}.row .column.column-25{flex:0 0 25%;max-width:25%}.row .column.column-75{flex:0 0 75%;max-width:75%}a{color:#9b4dca;text-decoration:none}a:focus,a:hover{color:#a56bc9;}fieldset,input,select,textarea{margin-bottom:1.5rem}.button,button,dd,dt,li{margin-bottom:1.0rem}p{margin-top:0}fieldset{border-width:0;padding:0}label,legend{display:block;font-size:1.6rem;font-weight:700;margin-bottom:.5rem}</style><body><header class="container"><h1 class="title" style="text-align: center;">Cloudflare reverse proxy</h1></header><main class="container"><fieldset><label for="url">Enter real url:</label><div class="row"><input class="column column-75" type="text" placeholder="https://..." id="url"><button class="column column-25 button-primary" type="submit" id="go" onclick="window.location.href=window.location.href+document.getElementById('url').value;">Go!</button></div></fieldset><br><p>Usage: ${origin}/real_url<br>2020-2022 Modified by YidaozhanYa, <a href="https://gitlab.com/NickCao/experiments/-/blob/master/workers/r.js">original code</a> by Nick Cao<br>DO NOT ABUSE!</p></main></body></html>`
    if (request.url == origin + "/") { return new Response(index, { status: 200, headers: { "Content-Type": "text/html" } }) } //index page
    try {
        let real_url = request.url.substr(origin.length + 1).fixScheme()

        response = await fetch(real_url, request);
        if (response.status == 302 || response.status == 301) {
            let target_url = (new URL(response.headers.get("Location"), real_url)).href
            return Response.redirect(origin + '/' + target_url, 302)
        }

        response = new Response(response.body, response)
        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('X-Request-Url', request.url)
        response.headers.set('X-Real-Url', real_url)
        response.headers.set('X-Powered-By', 'YidaozhanYa')
        return response;
    } catch (err) {
        return new Response(index.replace("Cloudflare reverse proxy", "400 Bad Request").replace("Cloudflare reverse proxy", "400 Bad Request"), { status: 400, headers: { "Content-Type": "text/html" } })
    }
}
