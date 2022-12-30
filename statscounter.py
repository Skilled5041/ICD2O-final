def input_game(player_hand: List[Card], dealer_hand: List[Card], player_score: int, dealer_score: int, result: str):
  # code to input the game into the stats counter
  pass
import json

stats = {
  "games_played": 0,
  "wins": 0,
  "losses": 0,
  "winrate": 0,
  "total_time": 0
}

def input_game(player_hand: List[Card], dealer_hand: List[Card], player_score: int, dealer_score: int, result: str):
  global stats
  stats["games_played"] += 1
  if result == "win":
    stats["wins"] += 1
  elif result == "loss":
    stats["losses"] += 1
  stats["winrate"] = stats["wins"] / stats["games_played"]
  with open("stats.json", "w") as f:
    json.dump(stats, f)

hit_button.bind_click(window, lambda _: hit(window, deck, player_hand, money, bet))
stand_button.bind_click(window, lambda _: stand(window, deck, player_hand, dealer_hand, money, bet))
double_button.bind_click(window, lambda _: double_down(window, deck, player_hand, money, bet))
split_button.bind_click(window, lambda _: split(window, deck, player_hand, money, bet))
quit_button.bind_click(window, lambda _: sys.exit())


