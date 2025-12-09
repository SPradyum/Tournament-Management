# 🏆 Multi-Sport Tournament Manager

A professional, offline, desktop application built using **Python** and **CustomTkinter** that allows you to manage tournaments across *any sport* (Badminton, Football, Cricket, Basketball, Volleyball, Kabaddi, Universal Scoring etc.).

Supports:
- Team creation
- Round-robin fixture generation
- Score entry & match result updates
- Automatic league standings table
- Multiple sport scoring rules
- Save & load tournaments as JSON files
- Clean modern UI in dark theme

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| Multi-Sport Support | Works for any sport using SF / SA / SD scoring |
| Round Robin Format | Auto generation of fixtures |
| Match Result Input | Update scores by match ID |
| Auto Standings Table | Displays Played, Won, Drawn, Lost, SF, SA, SD, Points |
| Save & Load | Export tournaments to JSON and reload later |
| Minimal & Modern UI | Built with CustomTkinter dark mode |

---

## 🖥 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3 |
| GUI | CustomTkinter |
| Storage | JSON |
| Scheduling | Round-Robin fixture generator script |
| Data Processing | Standings Table Calculator |

---

## 🚀 How to Run

```bash
git clone <your-repo-url>
cd tournament_manager
pip install customtkinter
python main.py
```
---
## 🕹 How to Use

- Enter Tournament Name
- Select Sport & Format
- Add Teams (min. 2)
- Click Generate Fixtures
- Enter Match ID & scores to update standings
- Save tournament anytime to reload later

---
## 🌟 Future Enhancements

- Knockout Tournament Mode (Brackets)
- Export Standings to PDF / Excel
- Player statistics per match
- Live match timer
- Online synchronization & multi-device support

---

📊 Standings Table Example

| Pos | Team             |  P  |  W |  D |  L |  SF |  SA |  SD | Pts |
|:---:|:----------------:|:---:|:--:|:--:|:--:|:---:|:---:|:---:|:---:|
|  1  | Thunder Smashers |  3  |  2 |  1 |  0 |  75 |  60 |  15 |  7  |
|  2  | Volley Kings     |  3  |  2 |  0 |  1 |  70 |  58 |  12 |  6  |


---
## 🤝 Contributing

Pull Requests are welcome.
Feel free to open issues for UI improvements, new features or bug fixes.






