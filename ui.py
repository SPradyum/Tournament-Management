import customtkinter as ctk
from tkinter import messagebox, filedialog

from models import Tournament, TournamentType, Team, SPORT_PRESETS
from scheduler import generate_round_robin, calculate_league_table
from storage import save_tournament_json, load_tournament_json


class TournamentManagerUI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.tournament = None

        self.pack(fill="both", expand=True, padx=10, pady=10)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Multi-Sport Tournament Manager",
                             font=("Segoe UI", 24, "bold"))
        title.pack(pady=(10, 15))

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(top, text="Tournament Name:").grid(row=0, column=0, sticky="w", padx=10)
        self.name_entry = ctk.CTkEntry(top, placeholder_text="Enter Tournament Name")
        self.name_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(top, text="Sport:").grid(row=0, column=1, sticky="w", padx=10)
        self.sport_var = ctk.StringVar(value="Universal")
        self.sport_menu = ctk.CTkOptionMenu(top, variable=self.sport_var, values=list(SPORT_PRESETS.keys()))
        self.sport_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(top, text="Format:").grid(row=0, column=2, sticky="w", padx=10)
        self.format_var = ctk.StringVar(value="Round Robin")
        self.format_menu = ctk.CTkOptionMenu(top, variable=self.format_var, values=["Round Robin"])
        self.format_menu.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        top.grid_columnconfigure(0, weight=1)

        # main bottom section layout fix
        self.middle = ctk.CTkFrame(self)
        self.middle.pack(fill="both", expand=True)

        self.middle.grid_columnconfigure((0, 1, 2), weight=1)
        self.middle.grid_rowconfigure(0, weight=1)

        self._build_middle_frames()

    def _build_middle_frames(self):
        # teams section
        self.teams_frame = ctk.CTkFrame(self.middle)
        self.teams_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.teams_frame, text="Teams", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 4))
        self.team_entry = ctk.CTkEntry(self.teams_frame, placeholder_text="Team Name")
        self.team_entry.pack(fill="x", padx=10, pady=(5, 5))

        ctk.CTkButton(self.teams_frame, text="Add Team", command=self.add_team).pack(padx=10, pady=(0, 10))

        self.teams_box = ctk.CTkTextbox(self.teams_frame, height=180)
        self.teams_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.teams_box.insert("end", "No teams yet.\n")
        self.teams_box.configure(state="disabled")

        ctk.CTkButton(self.teams_frame, text="Generate Fixtures", fg_color="#2563eb",
                      command=self.generate_fixtures).pack(padx=10, pady=(0, 10))

        # fixtures
        self.fixtures_frame = ctk.CTkFrame(self.middle)
        self.fixtures_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.fixtures_frame, text="Fixtures", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.fixtures_box = ctk.CTkTextbox(self.fixtures_frame)
        self.fixtures_box.pack(fill="both", expand=True, padx=10, pady=5)
        self.fixtures_box.insert("end", "Fixtures not generated yet.\n")
        self.fixtures_box.configure(state="disabled")

        # match result entry
        result = ctk.CTkFrame(self.fixtures_frame)
        result.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(result, text="Enter Result:").grid(row=0, column=0, columnspan=3, pady=4)
        self.match_id_entry = ctk.CTkEntry(result, width=60, placeholder_text="ID")
        self.match_id_entry.grid(row=1, column=0, padx=5)
        self.home_score_entry = ctk.CTkEntry(result, width=60, placeholder_text="Home")
        self.home_score_entry.grid(row=1, column=1, padx=5)
        self.away_score_entry = ctk.CTkEntry(result, width=60, placeholder_text="Away")
        self.away_score_entry.grid(row=1, column=2, padx=5)

        ctk.CTkButton(result, text="Update", command=self.update_result).grid(row=2, column=0, columnspan=3, pady=8)

        # standings
        self.standings_frame = ctk.CTkFrame(self.middle)
        self.standings_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.standings_frame, text="Standings", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.standings_box = ctk.CTkTextbox(self.standings_frame)
        self.standings_box.pack(fill="both", expand=True, padx=10, pady=5)
        self.standings_box.insert("end", "Standings will appear here.\n")
        self.standings_box.configure(state="disabled")

        # save load
        bottom = ctk.CTkFrame(self)
        bottom.pack(fill="x", pady=10)

        ctk.CTkButton(bottom, text="Save", command=self.save_tournament).pack(side="left", padx=10)
        ctk.CTkButton(bottom, text="Load", command=self.load_tournament).pack(side="left")

    # backend logic
    def ensure_tournament(self):
        if self.tournament is None:
            name = self.name_entry.get().strip() or "Untitled Tournament"
            sport = self.sport_var.get()
            self.tournament = Tournament(name, sport, TournamentType.ROUND_ROBIN)
        return self.tournament

    def add_team(self):
        name = self.team_entry.get().strip()
        if not name:
            messagebox.showwarning("Error", "Enter a team name first.")
            return

        t = self.ensure_tournament()

        if any(team.name.lower() == name.lower() for team in t.teams):
            messagebox.showwarning("Duplicate", "Team already exists.")
            return

        t.teams.append(Team(name))
        self.team_entry.delete(0, "end")
        self.refresh_team_list()

    def refresh_team_list(self):
        self.teams_box.configure(state="normal")
        self.teams_box.delete("0.0", "end")
        for i, team in enumerate(self.tournament.teams, start=1):
            self.teams_box.insert("end", f"{i}. {team.name}\n")
        self.teams_box.configure(state="disabled")

    def generate_fixtures(self):
        t = self.ensure_tournament()

        if len(t.teams) < 2:
            messagebox.showwarning("Error", "Add at least 2 teams.")
            return

        t.matches = generate_round_robin(t.teams)

        self.fixtures_box.configure(state="normal")
        self.fixtures_box.delete("0.0", "end")
        for m in t.matches:
            self.fixtures_box.insert("end", f"[ID {m.id}] {m.home.name} vs {m.away.name}  |  -  | {m.status.value}\n")
        self.fixtures_box.configure(state="disabled")

        self.update_standings()

    def update_result(self):
        if self.tournament is None or not self.tournament.matches:
            messagebox.showwarning("Error", "Generate fixtures first.")
            return

        try:
            match_id = int(self.match_id_entry.get().strip())
            hs = int(self.home_score_entry.get().strip())
            as_ = int(self.away_score_entry.get().strip())
        except:
            messagebox.showerror("Error", "Enter valid integers.")
            return

        match = next((m for m in self.tournament.matches if m.id == match_id), None)
        if not match:
            messagebox.showerror("Error", "Invalid match ID.")
            return

        match.set_result(hs, as_)
        self.match_id_entry.delete(0, "end")
        self.home_score_entry.delete(0, "end")
        self.away_score_entry.delete(0, "end")
        self.refresh_fixtures_display()
        self.update_standings()

    def refresh_fixtures_display(self):
        self.fixtures_box.configure(state="normal")
        self.fixtures_box.delete("0.0", "end")
        for m in self.tournament.matches:
            score = f"{m.home_score}-{m.away_score}" if m.home_score is not None else "-"
            self.fixtures_box.insert("end", f"[ID {m.id}] {m.home.name} vs {m.away.name}  |  {score}  | {m.status.value}\n")
        self.fixtures_box.configure(state="disabled")

    def update_standings(self):
        table = calculate_league_table(self.tournament)
        self.standings_box.configure(state="normal")
        self.standings_box.delete("0.0", "end")

        header = f"{'Pos':<4}{'Team':<17}{'P':<4}{'W':<4}{'D':<4}{'L':<4}{'SF':<4}{'SA':<4}{'SD':<4}{'Pts':<4}\n"
        self.standings_box.insert("end", header)
        self.standings_box.insert("end", "-" * len(header) + "\n")

        for i, row in enumerate(table, start=1):
            self.standings_box.insert("end",
                                      f"{i:<4}{row['team']:<17}{row['played']:<4}{row['won']:<4}{row['drawn']:<4}"
                                      f"{row['lost']:<4}{row['sf']:<4}{row['sa']:<4}{row['sd']:<4}{row['points']:<4}\n")

        self.standings_box.configure(state="disabled")

    def save_tournament(self):
        file = filedialog.asksaveasfilename(defaultextension=".json")
        if file:
            save_tournament_json(self.tournament, file)
            messagebox.showinfo("Saved", "Tournament saved successfully!")

    def load_tournament(self):
        file = filedialog.askopenfilename()
        if file:
            self.tournament = load_tournament_json(file)
            self.refresh_team_list()
            self.refresh_fixtures_display()
            self.update_standings()
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, self.tournament.name)
