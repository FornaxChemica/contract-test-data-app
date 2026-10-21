import json, os, random
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

FIRST = ["Ava", "Liam", "Maya", "Noah", "Zara", "Ethan", "Priya", "Lucas", "Nina", "Omar"]
LAST = ["Sharma", "Johnson", "Patel", "Garcia", "Kim", "Brown", "Singh", "Miller", "Ali", "Davis"]
STREETS = ["1200 S Mill Ave", "450 W University Dr", "88 E Broadway Rd", "231 N College Ave", "19 W Southern Ave"]

def make_contracts(n, seed=42):
    rng = random.Random(seed)
    out = []
    for i in range(1, n + 1):
        rent = rng.choice([950, 1100, 1250, 1400, 1650, 1800])
        out.append({
            "contract_id": f"RC-{1000+i}",
            "tenant": f"{rng.choice(FIRST)} {rng.choice(LAST)}",
            "property": rng.choice(STREETS) + ", Tempe, AZ",
            "monthly_rent": rent,
            "lease_months": rng.choice([6, 12, 12, 18]),
            "deposit": rent,
            "status": rng.choice(["draft", "pending", "signed"])
        })
    return out

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/contracts":
            n = int(parse_qs(parsed.query).get("count", ["5"])[0])
            body = json.dumps(make_contracts(n), indent=2).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        else:
            rows = "".join(
                f"<tr><td>{c['contract_id']}</td><td>{c['tenant']}</td><td>{c['property']}</td>"
                f"<td>${c['monthly_rent']}</td><td>{c['lease_months']} mo</td><td>{c['status']}</td></tr>"
                for c in make_contracts(5))
            page = (
                "<html><head><title>Contract Test Data</title></head><body>"
                "<h1>Rental Contract Test Data Generator</h1>"
                "<p>Sample records for testing the rental-contract portal. "
                "Same data on every machine because it runs in a container.</p>"
                "<table border='1' cellpadding='6'><tr><th>ID</th><th>Tenant</th><th>Property</th>"
                "<th>Rent</th><th>Lease</th><th>Status</th></tr>" + rows + "</table>"
                "<p>JSON API: /api/contracts?count=5</p></body></html>")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(page.encode())
    def log_message(self, fmt, *args):
        print("REQ:", fmt % args, flush=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print(f"Contract test-data app listening on port {port}", flush=True)
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
