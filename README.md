# 🃏 Solitaire (Klondike) — Python & Pygame

A fully playable **Solitaire (Klondike)** game built from scratch using **Python** and **Pygame**.  
It features drag-and-drop mechanics, realistic pile behavior, and smooth visuals — a great demonstration of object-oriented design and event-driven programming in Python.

---

## 🎮 Gameplay Preview

> Classic Solitaire experience with smooth animations and modern visuals.  
> Play using your mouse — drag cards, flip through the stock, and build your foundations to win!

---

## ✨ Features

- 🧩 **Classic Solitaire (Klondike)** rules  
- 🎨 **Custom assets** for background and cards  
- 🖱️ **Smooth drag-and-drop** card movement  
- 🧠 **Automatic win detection** with restart option  
- 🧰 **Object-Oriented Design** for easy modification  
- ♻️ **Stock**, **Waste**, **Tableau**, and **Foundation** piles fully implemented  

---

## 🛠️ Tech Stack

- **Language:** Python 3.x  
- **Library:** [Pygame](https://www.pygame.org/)  
- **Paradigm:** Object-Oriented Programming (OOP)

---

## 🚀 Installation & Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/<your-username>/solitaire-pygame.git
   cd solitaire-pygame
2. **Install dependencies**
   ```bash
   pip install pygame
3. **Run the game**
   ```bash
   python main.py

---

## 🗂️ Folder Structure
  📁 solitaire-pygame
   ┣ 📂 assets/
   ┃ ┣ 📂 cards/
   ┃ ┣ 🖼️ background.png
   ┃ ┗ 🖼️ card_back.png
   ┣ 📜 card.py
   ┣ 📜 utils.py
   ┣ 📜 main.py
   ┗ 📜 README.md

---

## 🏆 How to Play
   - Click on the stock pile to draw cards to the waste pile.
   - Drag cards between tableau columns following alternating color and descending order.
   - Place cards on foundations from Ace → King (same suit).
   - Empty tableau? Only Kings can be placed there.
   - Once all cards reach the foundations — you win! 🎉
   - Press R to restart the game after winning.

---

## 💡 Future Enhancements
   - 🧮 Add score tracking and move counter
   - 🔙 Implement undo functionality
   - 🔊 Add sound effects and animations
   - 💻 Add a main menu and settings options

---

Built with ❤️ using Python and Pygame
