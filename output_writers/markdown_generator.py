def generate_markdown_summary(deal_data):
    return f"""
### Property Summary
**Address:** {deal_data['address']}
**ARV:** ${deal_data['arv']}
**Strategy:** {deal_data['strategy']}

### Financial Highlights
- **Monthly Cash Flow:** ${deal_data['cash_flow']}
- **IRR:** {deal_data['irr']*100:.2f}%
- **Cap Rate:** {deal_data['cap_rate']*100:.2f}%
- **DSCR:** {deal_data['dscr']:.2f}

### Verdict: {deal_data['grade']}
"""