# HabitPeak

#### Video Demo: <https://youtu.be/QX4_BRHCNdg>

#### Description

**HabitPeak** is a user-friendly web application developed using Flask, HTML, CSS, and JavaScript, with Bootstrap enhancing its design, to help users build and track daily habits effortlessly. Created as part of the **CS50 Final Project**, this project reflects my journey through the course, blending practical coding skills with a user-focused approach to foster personal growth and consistency. The inspiration came from my own struggle to maintain routines, prompting me to create a tool that turns aspirations into actionable habits. Built from scratch, HabitPeak offers a sleek, responsive interface that adapts seamlessly across devices—desktops, tablets, and mobiles—thanks to Bootstrap’s robust framework. Users can set specific goals, monitor progress, and stay motivated as they achieve streaks and milestones, all within a rewarding experience.

The development process involved integrating Flask for the backend to manage user authentication with Flask-Login, ensuring secure login and data protection. HTML structured the layout, CSS added stylish transitions and hover effects, and JavaScript enabled interactive features like delete confirmations. Data is persistently stored in an SQLite database, chosen for its simplicity and suitability for a solo project. Designing HabitPeak, I prioritized a minimalistic yet effective design, leveraging Bootstrap to save time on custom styling while ensuring responsiveness. Challenges included resolving template errors (e.g., undefined attributes like `get_current_streak()`) and optimizing the layout to eliminate scrolling, which I tackled through iterative testing and debugging—skills honed in CS50. The project taught me to balance functionality with user experience, a key takeaway from the course.

Future enhancements could include a streak tracking system with a completion log or mobile notifications, but the current version focuses on core features to meet project requirements. HabitPeak not only fulfills CS50’s technical expectations but also serves as a practical tool for personal development, reflecting the course’s impact on my coding abilities.

> HabitPeak empowers users to develop consistency through easy habit tracking, encouraging long-term self-improvement with a simple, effective design.

## Files

- `app.py`: Contains Flask routes, models, and logic.
- `templates/`: HTML templates (e.g., `habits.html`, `base.html`).
- `static/`: CSS and JavaScript files.

## Design Choices

- Used Bootstrap for rapid, responsive design.
- SQLite for lightweight, local data storage.
- Flask-Login for secure, simple authentication.

