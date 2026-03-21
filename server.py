#!/usr/bin/env python3
"""
Trading Dashboard Server
Serves the dashboard HTML + proxies Yahoo Finance candle data to avoid CORS issues.
"""
import json
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PORT = 8080

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/candles":
            self.handle_candles(parse_qs(parsed.query))
        else:
            super().do_GET()

    def handle_candles(self, params):
        symbol = params.get("symbol", [""])[0].upper()
        from_ts = params.get("from", [""])[0]
        to_ts = params.get("to", [""])[0]

        if not symbol or not from_ts or not to_ts:
            self.send_json(400, {"error": "Missing symbol, from, or to parameter"})
            return

        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            f"?period1={from_ts}&period2={to_ts}&interval=1d&includePrePost=false"
        )

        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=15) as resp:
                raw = json.loads(resp.read())

            result = raw.get("chart", {}).get("result", [])
            if not result:
                self.send_json(404, {"error": f"No data for {symbol}"})
                return

            r = result[0]
            timestamps = r.get("timestamp", [])
            quote = r.get("indicators", {}).get("quote", [{}])[0]
            opens = quote.get("open", [])
            highs = quote.get("high", [])
            lows = quote.get("low", [])
            closes = quote.get("close", [])

            # Filter out any bars with null values
            o, h, l, c, t = [], [], [], [], []
            for i in range(len(timestamps)):
                if (i < len(closes) and closes[i] is not None
                        and highs[i] is not None and lows[i] is not None
                        and opens[i] is not None):
                    o.append(round(opens[i], 4))
                    h.append(round(highs[i], 4))
                    l.append(round(lows[i], 4))
                    c.append(round(closes[i], 4))
                    t.append(timestamps[i])

            if not c:
                self.send_json(404, {"error": f"No valid candle data for {symbol}"})
                return

            self.send_json(200, {"s": "ok", "o": o, "h": h, "l": l, "c": c, "t": t})

        except HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:200]
            self.send_json(e.code, {"error": f"Yahoo Finance: {e.code} {body}"})
        except URLError as e:
            self.send_json(502, {"error": f"Network error: {e.reason}"})
        except Exception as e:
            self.send_json(500, {"error": str(e)})

    def send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Only log API calls and errors, not every static file request
        msg = str(args[0]) if args else ""
        if "/api/" in msg or "404" in msg or "500" in msg:
            super().log_message(format, *args)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    print(f"Dashboard server running on http://localhost:{port}")
    print(f"Open: http://localhost:{port}/trading-dashboard.html")
    print("Press Ctrl+C to stop.\n")
    try:
        HTTPServer(("", port), DashboardHandler).serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
