# judgedice.com — Brand & Growth Roadmap

The vision: judgedice.com is Judge's personal brand — an editorial, print-flavored home for
**Offerings** (consulting services, starting with tribute writing) and **Entries** (writing:
sample tributes, opinion, and review pieces). The site runs on Odoo, which also powers
marketing, forms, the customer portal, and payments.

**The core funnel:** a reader lands on an Entry or the Offerings page → books a paid
consultation ($50, credited toward the final quote, couponable to free for early customers)
→ intake call → custom quote → draft → revision → delivered tribute → testimonial + referral.

Detailed, dated tracking lives in the private **judgedice.com Roadmap** GitHub Project.
This file is the public summary of the phases.

---

## Phase 0 — Go-live plumbing

Get the site reachable, secure, and measurable.

- Actions secrets so GitOps deploys go live
- DNS/SSL for www.judgedice.com (+ halfa.glass), apex → www redirects
- Favicon + social/OG meta, analytics, mobile nav styling

## Phase 1 — The Offer & the Entries

Content that earns the booking.

- `/offerings`: tribute-writing offer page — the four tribute types (eulogies & memorials,
  celebration speeches, professional tributes, written keepsakes), how it works, pricing, CTA
- `/blog` as **Entries**: styled to the design system; seeded with anonymized sample
  tributes plus opinion/review pieces; steady publishing cadence, every entry ends in a CTA
- Homepage rewrite: brand story → Offerings

## Phase 2 — Pay-to-book checkout

The transaction core: pay to play.

- Odoo eCommerce + coupon apps; Stripe (test mode → live)
- "Tribute Consultation" as a $50 product; checkout styled to the design system
- Checkout finishes with booking the consult (Appointments, Google-Calendar synced)
- Founding-customer coupon codes (100% off, limited quantity)

## Phase 3 — Customer portal

Logged-in service that makes the process feel premium.

- Invoices & receipts, self-serve reschedule/cancel
- Structured intake questionnaire after booking
- Draft review & final-piece delivery through the portal (comments, downloads, archive)
- Quote → e-sign → pay online for the full engagement

## Phase 4 — Marketing engine

Turn the funnel on.

- CRM for inbound leads; email list + monthly Entries digest
- SEO pass targeting tribute/speech-writing queries
- Distribution: LinkedIn (professional tributes), local partners (funeral homes, wedding
  planners, HR), testimonials on Offerings, referral codes for past customers

## Phase 5 — Scale

Once the funnel converts.

- Gift cards and printed keepsake products in the store
- Tiered packages (standard / delivery coaching / rush)
- Marketing automation drips; reviews/Google Business Profile
