"""Read-only Odoo introspection helper. Loads creds from repo .env; never prints the key."""
import os, sys, xmlrpc.client

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_env(path=os.path.join(REPO, ".env")):
    """Creds from repo .env, falling back to environment variables (CI secrets)."""
    env = {}
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("ODOO_URL", "ODOO_DB", "ODOO_USER", "ODOO_KEY"):
        if not env.get(k) and os.environ.get(k):
            env[k] = os.environ[k]
    missing = [k for k in ("ODOO_URL", "ODOO_DB", "ODOO_USER", "ODOO_KEY") if not env.get(k)]
    if missing:
        print("missing credentials: %s (need .env or env vars)" % ", ".join(missing), file=sys.stderr)
        sys.exit(1)
    return env

def connect():
    e = load_env()
    url, db, user, key = e["ODOO_URL"], e["ODOO_DB"], e["ODOO_USER"], e["ODOO_KEY"]
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, user, key, {})
    if not uid:
        print("AUTH FAILED", file=sys.stderr); sys.exit(1)
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    def call(model, method, *args, **kw):
        return models.execute_kw(db, uid, key, model, method, list(args), kw)
    return uid, call

if __name__ == "__main__":
    uid, call = connect()
    ver = xmlrpc.client.ServerProxy(load_env()["ODOO_URL"] + "/xmlrpc/2/common").version()
    print(f"AUTH OK — uid={uid}, server={ver.get('server_version')}")

    print("\n=== website records ===")
    sites = call("website", "search_read", [], ["id", "name", "domain", "default_lang_id", "theme_id"])
    for s in sites:
        print(s)

    print("\n=== website.page count per site (published pages) ===")
    pages = call("website.page", "search_read", [], ["id", "name", "url", "website_id", "view_id", "is_published"])
    for p in pages:
        print(p)
