def respond_to_attack(attack):

    if attack == "Port Scan":
        return "Blocking suspicious IP and logging event"

    return "Monitoring traffic"