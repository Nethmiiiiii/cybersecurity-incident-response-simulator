from flask import Flask, render_template
from simulator import simulate_port_scan
from detector import detect_attack
from responder import respond_to_attack

app = Flask(__name__)

attack_count = 0

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/simulate")
def simulate():

    global attack_count

    simulate_port_scan()

    attack = detect_attack()

    response = respond_to_attack(attack)

    attack_count += 1

    # determine threat level
    if attack_count < 3:
        threat = "Low"
    elif attack_count < 6:
        threat = "Medium"
    else:
        threat = "High"

    # log attack
    with open("logs.txt","a") as f:
        f.write(f"Attack: {attack} | Response: {response}\n")

    return render_template(
        "result.html",
        attack=attack,
        response=response,
        count=attack_count,
        threat=threat
    )

if __name__ == "__main__":
    app.run(debug=True)