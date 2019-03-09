def yum_yum(message):
    # John contributed anal, butt, and butts
    yum = ['dick', 'dicks', 'penis', 'butthole', 'ass', 'anal', 'butt', 'butts'] 
    if message.content.lower() in yum:
        return {"message": "Yum yum"}
    for name in ['kyle', 'jacob', 'dennis', 'john', 'ryan', 'isaak']:
        if message.content.lower() == name:
            return {"message": f"{name} is a degenerate"}


explicit_eggs = [yum_yum]

