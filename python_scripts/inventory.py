import yaml
from pathlib import Path

def load_hosts(site_dir):
    """
    Read inventory.yaml in each application under a site directory.
    Returns a dict mapping each hostname to its tags, application name, and site name.
    """
    hosts = {}
    site = site_dir.name

    for app_dir in site_dir.iterdir():
        if not app_dir.is_dir():
            continue
        inv = app_dir / 'inventory.yaml'
        if not inv.exists():
            continue

        with open(inv) as f:
            data = yaml.safe_load(f) or {}

        for entry in data.get('spec', []):
            hn = entry.get('Hostname')
            tags = entry.get('Tags', [])
            if not hn:
                continue

            # Keep tags that are not full domains
            filtered = {t for t in tags if not t.endswith(
                '.apple.com') and t != '.jmet.apple.com'}

            hosts[hn] = {'tags': filtered, 'app': app_dir.name, 'site': site}
    # print(hosts)

    return hosts


def expected_tags(hn, app, site):
    """
    Compute valid tags for hostname, app, and site per rules.
    """
    exp = {'prod', 'both', app, site}

    # Special prefix rules (5–6,10)
    # prefixes = ['attk', 'eqhk', 'eqtk', 'eqsg']
    # has_pref = any(hn.startswith(p) for p in prefixes)
    # if has_pref:
    #    for p in prefixes:
    #        if hn.startswith(p):
    #            exp.add(p)
    # else:
    #    exp.add('local')
#
    #    # Trailing-digit rules (1–3)
    #    seg = hn.split('-')[-1]
    #    for ch in reversed(seg):
    #        if ch.isdigit():
    #            d = int(ch)
    #            if d == 1:
    #                exp.add('canary')
    #            if d % 2:
    #                exp.add('room1')
    #            else:
    #                exp.add('room2')
    #            break

    # j1p1/j2p1/j1p2 patterns (7)
    if 'j1p1' in hn:
        exp.add('room1')
    if 'j2p1' in hn:
        exp.add('room2')
    if 'j1p2' in hn:
        exp.add('room2')

    # if 'j1p1' in hn:
    # exp.add('room1')
    # if 'j2p1' in hn or 'j1p2' in hn:
    # exp.add('room2')
#
    # jcs inclusion (8)
    if 'jcs' in hn:
        exp.add('jcs')

    # fdr-controller special tags (12,16)
    if app == 'fdr-controller':
        exp.add('fdr-skyline')
        exp.add('fdr-prefetch')
        exp.add('controller')

    if app == 'tatsu':
        exp.add('tatsu-tss-factory')

    if site == 'aprt,apsg,bylg,ccpb,cwcq,eqsg,eqtk,fxbl,fxbz,fxcn,fxlh,fxty,fxzz,hkcl,itbg,itjs,lxkj,lxsz,nldc,pgks,pgpd,qsmc,tehr,tkcl,ussh,winp':
        exp.add('stress')

    # fdr-oracle-healthcheck tags (19–21)
    if app == 'fdr-oracle-healthcheck':
        exp.discard('oraclevm')
        exp.add('ap')
        exp.add('bp')

    # Batch wildcard (17)
    # exp.add('batch')

    # Treecko app tags (18)
    if app.lower() == 'treecko':
        exp.add('treecko-ps')
        exp.add('treecko-receipt-ps')
        
    # Stress tag is not working
    if site == 'aprt,apsg,bylg,ccpb,cwcq,eqsg,eqtk,fxbl,fxbz,fxcn,fxlh,fxty,fxzz,hkcl,itbg,itjs,lxkj,lxsz,nldc,pgks,pgpd,qsmc,tehr,tkcl,ussh,winp':
        exp.add('stress')

    left = hn.split(".", 1)[0]
    print(left)
    exp.add(left)

    return exp


def is_batch(tag):
    """True if tag contains 'batch'."""
    return 'batch' in tag


def audit_sites(root):
    """
    Audit tags for all hosts in each site under root.
    Returns list of {site, app, host, missing, invalid}.
    """
    report = []
    for site_dir in Path(root).iterdir():
        if not site_dir.is_dir():
            continue
        hosts = load_hosts(site_dir)
        for hn, info in hosts.items():
            curr = info['tags']
            exp = expected_tags(hn, info['app'], info['site'])

            # Handle batch wildcard
            wildcard = 'batch' in exp
            if wildcard:
                exp.remove('batch')
            # remove stress tag

            invalid = sorted(t for t in curr if t not in exp and not (
                wildcard and is_batch(t)))
            print("Expected tags : ", exp)
            print("Current tags : ", curr)
            print("----------------------------------------------")
            missing = sorted(exp - curr)
            if wildcard and not any(is_batch(t) for t in curr):
                missing.append('batch1')

            if missing or invalid:
                report.append({
                    'site': info['site'],
                    'app': info['app'],
                    'host': hn,
                    'missing': missing,
                    'invalid': invalid
                })

    return report


if __name__ == '__main__':
    ROOT = '/Users/a20551481/GIT/stark-yamls/inventory/prod/site'
    results = audit_sites(ROOT)
    for r in results:
        print(f"[{r['site']}] {r['app']} {r['host']}")
        if r['missing']:
            print("  Missing tags:", r['missing'])
        if r['invalid']:
            print("  Invalid tags:", r['invalid'])
        print()
