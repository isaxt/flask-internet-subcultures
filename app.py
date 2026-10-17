from datetime import datetime
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request
from aesthetics import get_pair

app = Flask(__name__)
CSV_FILE = Path(__file__).parent / "votes.csv"


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        vote = pd.DataFrame([{
            "aesthetic_a": request.form["aesthetic_a"],
            "aesthetic_b": request.form["aesthetic_b"],
            "winner": request.form["winner"],
            "time": datetime.now().isoformat(timespec="seconds"),
        }])

        if CSV_FILE.exists():
            previous_votes = pd.read_csv(CSV_FILE)
            vote = pd.concat([previous_votes, vote], ignore_index=True)

        vote.to_csv(CSV_FILE, index=False)
        message = "Vote saved! Here are two more aesthetics."

    pair = get_pair()
    return render_template("index.html", pair=pair, message=message)


@app.route("/results")
def results():
    rows = []
    if CSV_FILE.exists():
        votes = pd.read_csv(CSV_FILE)
        # Every aesthetic shown in a matchup gets one appearance; the winner also gets one win.
        shown = pd.concat([votes["aesthetic_a"], votes["aesthetic_b"]]).value_counts()
        wins = votes["winner"].value_counts()
        table = pd.DataFrame({"shown": shown, "wins": wins}).fillna(0).astype(int)
        table["win_rate"] = (100 * table["wins"] / table["shown"]).round(0).astype(int)
        table = table.sort_values(["win_rate", "shown"], ascending=False)
        rows = [(name, r.wins, r.shown, r.win_rate) for name, r in table.iterrows()]
    return render_template("results.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
