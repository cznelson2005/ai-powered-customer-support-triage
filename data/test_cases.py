test_cases = [

    # ── Severity 1: Routine inquiry ──────────────────────────
    ("What payment methods do you accept?",                          1, False),
    ("How do I update my billing address?",                          1, False),
    ("Could you remind me how to change my billing cycle?",          1, False),
    ("I tried to update my address but the button didn't work, "
     "I'll try again later",                                         1, False),

    # ── Severity 2: Minor issue ───────────────────────────────
    ("My order is delayed by 2 days",                                2, False),
    ("I haven't received my invoice yet",                            2, False),
    ("My order was supposed to arrive yesterday, "
     "not a huge deal but wanted to flag it",                        2, False),
    # Conflicting signal: angry tone but minor issue
    ("This is SO annoying, why can't I just change "
     "my email address easily??",                                     2, False),

    # ── Severity 3: Moderate issue ────────────────────────────
    ("I've been waiting 3 days longer than estimated, "
     "can someone look into this?",                                  3, False),
    ("The refund was supposed to take 3-5 days "
     "and it's been 6 days now",                                     3, False),
    ("I was overcharged by $5 on my last invoice, "
     "not a huge amount but please fix it",                          3, False),
    # Repeat contact but moderate severity
    ("I contacted support last week about a missing item "
     "and nobody followed up. Still waiting.",                       3, False),

    # ── Severity 4: Serious issue ─────────────────────────────
    ("I was charged TWICE and nobody is helping me. "
     "This is absolutely unacceptable!",                             4, True),
    ("My account has been locked for 2 days and "
     "I can't access any of my orders",                              4, True),
    # Conflicting signal: calm tone but serious issue
    ("I noticed a duplicate charge on my account. "
     "Could you please look into this when you get a chance?",       4, True),
    # Repeat contact escalation
    ("Hi, following up on my ticket from last week "
     "about the wrong item delivered. Still not resolved.",          4, True),

    # ── Severity 5: Critical issue ────────────────────────────
    ("This is completely unacceptable. I have contacted your "
     "support team THREE times about my account being wrongly "
     "suspended and NOBODY has resolved it. I am considering "
     "legal action if this is not resolved TODAY.",                  5, True),
    ("I have been charged incorrectly three months in a row. "
     "I need this resolved immediately or I'm cancelling.",          5, True),
    ("My business account has been suspended without notice "
     "and I'm losing money every hour this isn't fixed.",            5, True),
    # Calm tone but critical financial issue
    ("I noticed what appears to be an unauthorised charge "
     "of $200 on my account. Could you please investigate?",         4, True),
]