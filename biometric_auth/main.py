import customtkinter as ctk
from auth_engine import authenticate, register_user
from database import init_db, get_audit_logs, get_users_list, delete_user
import csv
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BiometricApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔐 Biometric Auth System")
        self.geometry("520x620")
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        # Header
        ctk.CTkLabel(self, text="🔐 Biometric Login",
                     font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(30, 4))
        ctk.CTkLabel(self, text="Secure face-based authentication system",
                     font=ctk.CTkFont(size=13),
                     text_color="gray").pack()

        # Username input
        ctk.CTkLabel(self, text="Username",
                     font=ctk.CTkFont(size=13)).pack(pady=(24, 4))
        self.username_entry = ctk.CTkEntry(
            self, placeholder_text="Enter your username",
            width=320, height=44, corner_radius=10)
        self.username_entry.pack()

        # Main buttons
        ctk.CTkButton(
            self, text="🔍  Authenticate", width=320, height=44,
            corner_radius=10, command=self.do_auth).pack(pady=(20, 8))

        ctk.CTkButton(
            self, text="➕  Register Face", width=320, height=44,
            corner_radius=10, fg_color="transparent",
            border_width=1, command=self.do_register).pack()

        # Status
        self.status_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=16)

        # Divider
        ctk.CTkFrame(self, height=1, width=320,
                     fg_color="gray").pack(pady=8)

        # Bottom buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=8)

        ctk.CTkButton(
            btn_frame, text="📋  Audit Log", width=150, height=36,
            corner_radius=8, fg_color="transparent", border_width=1,
            command=self.open_audit_log).grid(row=0, column=0, padx=6)

        ctk.CTkButton(
            btn_frame, text="👤  Admin Panel", width=150, height=36,
            corner_radius=8, fg_color="transparent", border_width=1,
            command=self.open_admin_panel).grid(row=0, column=1, padx=6)

        # Footer
        ctk.CTkLabel(
            self, text="Powered by NK · Netm",
            font=ctk.CTkFont(size=11),
            text_color="gray").pack(side="bottom", pady=12)

    def do_auth(self):
        self.status_label.configure(
            text="⏳ Scanning face...", text_color="orange")
        self.update()
        user, result = authenticate()
        if result == "success":
            self.status_label.configure(
                text=f"✅  Welcome, {user}!", text_color="#00d26a")
        elif result == "no_face":
            self.status_label.configure(
                text="⚠️  No face detected", text_color="orange")
        else:
            self.status_label.configure(
                text="❌  Access denied", text_color="#ff4b4b")

    def do_register(self):
        name = self.username_entry.get().strip()
        if not name:
            self.status_label.configure(
                text="⚠️  Please enter a username first",
                text_color="orange")
            return
        self.status_label.configure(
            text="📸 Capturing 3 face samples...", text_color="cyan")
        self.update()
        ok, result = register_user(name)
        if ok:
            self.status_label.configure(
                text=f"✅  {name} registered with 3 samples!",
                text_color="#00d26a")
        elif result == "duplicate":
            self.status_label.configure(
                text="⚠️  Username already exists",
                text_color="orange")
        else:
            self.status_label.configure(
                text="❌  Face capture incomplete",
                text_color="#ff4b4b")

    def open_audit_log(self):
        win = ctk.CTkToplevel(self)
        win.title("📋 Audit Log")
        win.geometry("540x480")

        ctk.CTkLabel(win, text="📋 Audit Log",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 4))

        frame = ctk.CTkScrollableFrame(win, width=500, height=320)
        frame.pack(pady=10, padx=16)

        logs = get_audit_logs()
        if not logs:
            ctk.CTkLabel(frame, text="No logs yet.",
                         text_color="gray").pack(pady=20)
        else:
            for username, event, timestamp in logs:
                row = ctk.CTkFrame(frame, corner_radius=8)
                row.pack(fill="x", pady=3, padx=4)
                ctk.CTkLabel(row, text=f"👤 {username}",
                             font=ctk.CTkFont(size=12, weight="bold"),
                             width=100).pack(side="left", padx=8, pady=6)
                ctk.CTkLabel(row, text=event,
                             font=ctk.CTkFont(size=12),
                             text_color="cyan").pack(side="left", padx=4)
                ctk.CTkLabel(row, text=timestamp,
                             font=ctk.CTkFont(size=11),
                             text_color="gray").pack(side="right", padx=8)

        ctk.CTkButton(
            win, text="💾  Export to CSV", width=200, height=38,
            corner_radius=8, command=self.export_csv).pack(pady=12)

    def open_admin_panel(self):
        win = ctk.CTkToplevel(self)
        win.title("👤 Admin Panel")
        win.geometry("480x440")

        ctk.CTkLabel(win, text="👤 Admin Panel",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 4))
        ctk.CTkLabel(win, text="Registered users",
                     font=ctk.CTkFont(size=13),
                     text_color="gray").pack()

        frame = ctk.CTkScrollableFrame(win, width=440, height=280)
        frame.pack(pady=10, padx=16)

        users = get_users_list()
        if not users:
            ctk.CTkLabel(frame, text="No users registered yet.",
                         text_color="gray").pack(pady=20)
        else:
            for username, created_at in users:
                row = ctk.CTkFrame(frame, corner_radius=8)
                row.pack(fill="x", pady=3, padx=4)
                ctk.CTkLabel(row, text=f"👤 {username}",
                             font=ctk.CTkFont(size=13, weight="bold")).pack(
                                 side="left", padx=10, pady=8)
                ctk.CTkLabel(row, text=created_at,
                             font=ctk.CTkFont(size=11),
                             text_color="gray").pack(side="left", padx=4)
                ctk.CTkButton(
                    row, text="🗑 Delete", width=80, height=28,
                    corner_radius=6, fg_color="#ff4b4b", hover_color="#cc0000",
                    command=lambda u=username, w=win: self.delete_user_action(u, w)
                ).pack(side="right", padx=8, pady=6)

    def delete_user_action(self, username, win):
        delete_user(username)
        win.destroy()
        self.open_admin_panel()
        self.status_label.configure(
            text=f"🗑  {username} deleted", text_color="orange")

    def export_csv(self):
        logs = get_audit_logs()
        path = "data/audit_log.csv"
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Username", "Event", "Timestamp"])
            writer.writerows(logs)
        self.status_label.configure(
            text=f"💾  Exported to {path}", text_color="#00d26a")

if __name__ == "__main__":
    init_db()
    app = BiometricApp()
    app.mainloop()