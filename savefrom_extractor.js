const fs = require('fs');
const vm = require('vm');
const path = require('path');

let JSDOM = null;
function getJSDOM() {
    if (JSDOM) return JSDOM;
    const possiblePaths = [
        'jsdom',
        path.join(__dirname, 'node_modules', 'jsdom'),
        '/data/data/com.termux/files/usr/lib/node_modules/jsdom',
        '/tmp/node_modules/jsdom'
    ];

    for (const p of possiblePaths) {
        try {
            JSDOM = require(p).JSDOM;
            if (JSDOM) return JSDOM;
        } catch (e) {}
    }

    try {
        const { execSync } = require('child_process');
        const globalRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
        JSDOM = require(path.join(globalRoot, 'jsdom')).JSDOM;
        if (JSDOM) return JSDOM;
    } catch (e) {}

    try {
        const { execSync } = require('child_process');
        execSync('npm install --prefix /tmp jsdom --no-save', { stdio: 'ignore', timeout: 90000 });
        JSDOM = require('/tmp/node_modules/jsdom').JSDOM;
        if (JSDOM) return JSDOM;
    } catch (e) {}

    throw new Error('JSDOM module could not be loaded. Please install jsdom: npm install jsdom');
}

let reqBuilderCode = null;

function loadScripts() {
    if (!reqBuilderCode) {
        const filePath = path.join(__dirname, 'savefrom_assets', 'workerRequestBuilder.js');
        let code = fs.readFileSync(filePath, 'utf8');
        const antiTamper = "if(!new Function(D[H0(a0FD.H,-a0FD.F,a0FD.i,-a0FD.D)])())throw new Error(H0(a0FD.L,a0FD.x,a0FD.w,a0FD.I)+H0(a0FD.q,-a0FD.l,a0FD.z,a0FD.U)+H1(-a0FD.Q,-a0FD.O,-a0FD.W,a0FD.C)+H1(-a0FD.y,-a0FD.N,-a0FD.m,a0FD.n)+H1(-a0FD.b,-a0FD.v,-a0FD.V,a0FD.K)+H0(a0FD.G,a0FD.c,a0FD.s,a0FD.f)+\x27y\x27);";
        if (code.includes(antiTamper)) {
            code = code.replace(antiTamper, '/* bypassed */');
        }
        reqBuilderCode = code;
    }
}

async function signRequest(targetUrl, customMsec) {
    loadScripts();

    let msec = customMsec || (Date.now() / 1000);
    if (!customMsec) {
        try {
            const msecRes = await fetch('https://en1.savefrom.net/msec', {
                headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' },
                signal: AbortSignal.timeout(4000)
            });
            const msecData = await msecRes.json();
            if (msecData && msecData.msec) {
                msec = msecData.msec;
            }
        } catch (e) {
            // fallback to current time
        }
    }

    const sandbox = {
        window: {
            location: { hostname: 'en1.savefrom.net', href: 'https://en1.savefrom.net/19wr/', origin: 'https://en1.savefrom.net' },
            document: { createElement: () => ({ setAttribute: () => {}, style: {}, appendChild: () => {} }), getElementById: () => null, body: { appendChild: () => {} } },
            navigator: { userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' },
            localStorage: { getItem: () => null, setItem: () => {} },
            Date: Date, Math: Math, TextEncoder: TextEncoder, Uint8Array: Uint8Array, Array: Array,
            crypto: crypto, atob: atob, btoa: btoa, JSON: JSON,
            fetch: async () => ({ json: async () => ({ msec: msec }) }),
            AbortController: AbortController,
            webpackChunksavefrom_net: []
        },
        console: console,
        fetch: async () => ({ json: async () => ({ msec: msec }) }),
        AbortController: AbortController,
        setTimeout: setTimeout, clearTimeout: clearTimeout,
        TextEncoder: TextEncoder, Uint8Array: Uint8Array, Array: Array,
        crypto: crypto, atob: atob, btoa: btoa, Date: Date, Math: Math, JSON: JSON
    };
    sandbox.self = sandbox.window;
    sandbox.window.window = sandbox.window;
    sandbox.document = sandbox.window.document;
    sandbox.location = sandbox.window.location;
    sandbox.navigator = sandbox.window.navigator;
    sandbox.localStorage = sandbox.window.localStorage;
    sandbox.globalThis = sandbox.window;

    vm.createContext(sandbox);
    vm.runInContext(reqBuilderCode, sandbox);

    const allModules = {};
    for (const chunk of sandbox.self.webpackChunksavefrom_net) Object.assign(allModules, chunk[1]);

    // 3769 is Babel interopRequireDefault
    allModules[3769] = function(e) {
        e.exports = function(e) { return e && e.__esModule ? e : { default: e }; };
        e.exports.__esModule = true;
        e.exports.default = e.exports;
    };

    // 1299 is BotD override -> '1' = notABot
    allModules[1299] = (H, F) => {
        F.__esModule = true;
        F.default = async () => '1';
    };

    const installedModules = {};
    function webpackRequire(moduleId) {
        if (installedModules[moduleId]) return installedModules[moduleId].exports;
        if (!allModules[moduleId]) return {};
        const module = installedModules[moduleId] = { exports: {} };
        allModules[moduleId](module, module.exports, webpackRequire);
        return module.exports;
    }
    webpackRequire.d = (exports, definition) => {
        for (let key in definition) {
            if (Object.prototype.hasOwnProperty.call(definition, key) && !Object.prototype.hasOwnProperty.call(exports, key)) {
                Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
            }
        }
    };
    webpackRequire.r = (exports) => {
        if (typeof Symbol !== 'undefined' && Symbol.toStringTag) {
            Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
        }
        Object.defineProperty(exports, '__esModule', { value: true });
    };

    const mod3245 = webpackRequire(3245);
    const signer = await mod3245.default;
    const signed = await signer(targetUrl);
    return signed;
}

function decryptResponse(jsResponse) {
    if (jsResponse.includes('<!DOCTYPE') || jsResponse.includes('<html')) {
        throw new Error('SaveFrom returned HTML/Cloudflare challenge instead of JS response');
    }

    const w = '/*js-response*/';
    const f = jsResponse.indexOf(w);
    const v = jsResponse.indexOf(w, f + 1);
    if (f !== -1 && v !== -1) {
        jsResponse = jsResponse.substring(f + w.length, v);
    }

    // Bypass anti-headless frameElement check in worker response
    const target2 = 'lD=Ez[H5(-0x1b*-0x8e+0x17*-0xb5+0x149,-0x24de+-0x2231+-0x1*-0x470f,d9,dE)+H5(-0x59f*-0x1+-0x7*-0x62+-0x84d*0x1,-0x8*0x24f+-0x1*0x1bf+0x1437,dS,dC)+\x27nt\x27]?Er(lD):';
    const replacement2 = 'lD = Er(lD) ? Er(lD) : ';
    if (jsResponse.includes(target2)) {
        jsResponse = jsResponse.replace(target2, replacement2);
    }

    const JSDOMClass = getJSDOM();
    const dom = new JSDOMClass(`<!DOCTYPE html><html><head></head><body><div id="sf_result">loading</div></body></html>`, {
        url: 'https://en1.savefrom.net/19wr/',
        runScripts: 'dangerously'
    });
    const win = dom.window;
    const fakeFrame = win.document.createElement('iframe');
    Object.defineProperty(win, 'frameElement', { get: () => fakeFrame, configurable: true });
    win.parent = win;

    let capturedVideoResult = null;
    let emptyResult = null;

    win.sf = {
        finishRequest: () => {},
        enableElement: () => {},
        videoResult: {
            show: (data) => {
                capturedVideoResult = data;
            }
        },
        result: {
            showResult: (data) => {
                capturedVideoResult = data;
            },
            showEmptyResult: (data) => {
                emptyResult = data;
            }
        }
    };

    const scriptEl = win.document.createElement('script');
    scriptEl.textContent = jsResponse;
    win.document.body.appendChild(scriptEl);

    if (capturedVideoResult) {
        return capturedVideoResult;
    }
    if (emptyResult) {
        throw new Error(emptyResult.html || 'SaveFrom empty result');
    }
    throw new Error('SaveFrom extraction returned no data');
}

async function extractSaveFrom(targetUrl) {
    const signed = await signRequest(targetUrl);

    const body = new URLSearchParams({
        sf_url: signed.url,
        new: '2',
        lang: 'en',
        app: '',
        'sf-nomad': '1',
        ts: signed.ts,
        _ts: signed._ts,
        _tsc: signed._tsc,
        _s: signed._s,
        _x: signed._x
    });

    const res = await fetch('https://worker.savefrom.net/savefrom.php', {
        method: 'POST',
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Origin': 'https://en1.savefrom.net',
            'Referer': 'https://en1.savefrom.net/19wr/',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: body.toString(),
        signal: AbortSignal.timeout(15000)
    });

    const jsResponse = await res.text();
    return decryptResponse(jsResponse);
}

// CLI usage:
// 1. node savefrom_extractor.js sign <url> [msec]
// 2. node savefrom_extractor.js decrypt <file_path>
// 3. node savefrom_extractor.js <url>
if (require.main === module) {
    const mode = process.argv[2];
    if (mode === 'sign') {
        const url = process.argv[3];
        const msec = process.argv[4] ? parseFloat(process.argv[4]) : null;
        signRequest(url, msec)
            .then(data => console.log(JSON.stringify(data)))
            .catch(err => {
                console.error(JSON.stringify({ error: err.message }));
                process.exit(1);
            });
    } else if (mode === 'decrypt') {
        const filePath = process.argv[3];
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            const data = decryptResponse(content);
            console.log(JSON.stringify(data));
        } catch (err) {
            console.error(JSON.stringify({ error: err.message }));
            process.exit(1);
        }
    } else {
        const url = mode || 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';
        extractSaveFrom(url)
            .then(data => {
                console.log(JSON.stringify(data, null, 2));
            })
            .catch(err => {
                console.error(JSON.stringify({ error: err.message }));
                process.exit(1);
            });
    }
}

module.exports = { extractSaveFrom, signRequest, decryptResponse };
