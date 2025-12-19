# 🎛️ AD9833 Waveform Generator using ExpEYES-17

This project demonstrates the generation of **Sine**, **Triangular**, and **Square** waveforms using the **AD9833 Direct Digital Synthesis (DDS) module**, controlled via the **ExpEYES-17** experimental platform using Python.

The program allows **interactive selection of waveform type and frequency** from the command line and outputs the corresponding waveform from the AD9833 module.

---

## 📌 Features

- Generates **Sine**, **Triangular**, and **Square** waves  
- User-selectable frequency via terminal input  
- Uses **SPI communication** through ExpEYES-17  
- Written in **Python 3**  
- Suitable for Physics and Electronics laboratories  

---

## 🧰 Hardware Requirements

- ExpEYES-17 experimental kit  
- AD9833 DDS module  
- Connecting wires  
- Oscilloscope / CRO  

---

## 💻 Software Requirements

- Python 3.x  
- ExpEYES-17 Python library (`eyes17`)  
- Linux / Windows system with ExpEYES-17 drivers  

---

## 🔌 Hardware Connections

| AD9833 Pin | ExpEYES-17 |
|-----------|-----------|
| VCC       | +5V       |
| GND       | GND       |
| FSY    | CS1       |
| CLK     | SCK      |
| DAT    | SDO      |
| OUT      | CRO / Oscilloscope |

---

## 🚀 How to Run

```bash
python AD9833_Sine_Sq_Trang.py
```

---

## 🎮 Program Usage

```
s <frequency>  → Sine wave
t <frequency>  → Triangular wave
q <frequency>  → Square wave
x              → Exit
```

---

## 📈 Output Waveforms

### Sine Wave
<img src="./Sine (5K).jpg" alt="Sine Wave" width="600" title="Sine Wave Generator">

### Triangular Wave
<img src="./Triangular (5K).jpg" alt="Triangular Wave" width="600" title="Triangular Wave Generator">

### Square Wave
<img src="./Square (5K).jpg" alt="Square Wave" width="600" title="Square Wave Generator">

📂 Create an `images/` folder and upload waveform screenshots with the above names.

---

## 📂 Project Structure

```
├── AD9833_Sine_Sq_Trang.py
├── README.md
└── images/
    ├── sine_wave.png
    ├── triangular_wave.png
    └── square_wave.png
```

---

## 👨‍🔬 Author

**Dr. Ujjwal Ghanta**  

---

## 📜 License

MIT License
