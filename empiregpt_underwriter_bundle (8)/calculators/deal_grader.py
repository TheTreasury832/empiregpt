def grade_deal(irr, dscr, coc):
    if irr > 0.18 and dscr > 1.5 and coc > 0.12:
        return "A", "Strong"
    elif irr > 0.14 and dscr > 1.25 and coc > 0.08:
        return "B", "Review"
    elif irr > 0.10 and dscr > 1.1 and coc > 0.05:
        return "C", "Weak"
    else:
        return "D", "Reject"