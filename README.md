Here is a comprehensive and structured README for the rules-based FeverTrance Engine. It is formatted for clarity, making it ready to be dropped directly into a `README.md` file on GitHub or your project repository.

---

# FeverTrance Engine 🌡️

The **FeverTrance Engine** is an algorithmic expert system designed to analyze high-frequency, continuous temperature data from wearable biosensors. By compressing minute-by-minute readings into daily clinical metrics, the engine identifies established medical fever patterns and provides automated diagnostic guidance for clinicians.

---

## 🎯 Key Features

* **Continuous Data Processing:** Downsamples minute-level wearable data into reliable 24-hour diurnal metrics (daily maximums, minimums, and fluctuations).
* **Clinical Pattern Recognition:** Automatically classifies temperature timelines into one of five classic medical fever profiles.
* **Diagnostic Routing:** Maps identified patterns to likely etiologies and recommends the standard next-step laboratory or imaging tests.

---

## 🔬 Recognized Fever Patterns

The engine evaluates data against the following clinical thresholds (Fever $> 38.0$°C, Normal $< 37.5$°C) to detect:

1. **Saddleback (Biphasic):** An initial fever that drops to normal for 1-2 days before spiking again.
2. **Stepladder:** A gradual, sequential daily increase in peak body temperature over several days.
3. **Intermittent:** Sharp fever spikes that return to a normal baseline within the same 24-hour period.
4. **Continuous (Sustained):** Persistently elevated temperature that never drops to normal, with daily fluctuations of less than 1°C.
5. **Remittent:** Persistently elevated temperature that never drops to normal, but fluctuates by more than 1°C daily.

---

## 🚀 Installation & Requirements

The engine is lightweight and relies entirely on standard data manipulation libraries.

**Requirements:**

* Python 3.7+
* `pandas`
* `numpy`

**Installation:**

```bash
pip install pandas numpy

```

---

## 💻 Quick Start Guide

The engine expects a pandas DataFrame with a `DatetimeIndex` and a `temperature` column representing minute-by-minute readings in Celsius.

```python
import pandas as pd
from fever_trance_engine import FeverTranceEngine

# 1. Load or simulate your wearable data
# df must have a DatetimeIndex and a 'temperature' column
df = pd.read_csv('patient_wearable_data.csv', index_col='timestamp', parse_dates=True)

# 2. Initialize the engine
engine = FeverTranceEngine()

# 3. Analyze the data
pattern, guidance = engine.analyze(df)

# 4. Review results
print(f"Detected Pattern: {pattern}")
print(f"Likely Etiology: {guidance['Likely Etiology']}")
print(f"Next Steps: {guidance['Next Steps']}")

```

---

## 📊 Diagnostic Mapping Matrix

The engine uses the following clinical logic to route patterns to diagnostic suggestions:

| Detected Pattern | Core Characteristics | Classic Associated Pathogens | Suggested Next Tests |
| --- | --- | --- | --- |
| **Saddleback** | Initial fever $\rightarrow$ 1-2 day remission $\rightarrow$ spike | Dengue, Leptospirosis, Tick Fever | Dengue NS1, Platelet count, Hematocrit |
| **Stepladder** | Peak temperature rises incrementally over 3-5 days | *Salmonella typhi* (Typhoid) | Blood culture, Widal test, Stool culture |
| **Intermittent** | Sharp spikes separated by a return to normal temp | Malaria, Tuberculosis, Sepsis | Peripheral blood smear, Chest X-ray |
| **Continuous** | Elevated >38°C; diurnal variation < 1°C | Lobar Pneumonia, Typhoid, UTI | Chest X-ray, Urinalysis |
| **Remittent** | Elevated >38°C; diurnal variation > 1°C | Endocarditis, Bronchopneumonia | Blood cultures, Echocardiogram, CBC |

---

## ⚠️ Medical Disclaimer

**Intended for Research and Triage Only.**
The FeverTrance Engine is an informatics tool designed to assist healthcare professionals by standardizing wearable data. It is **not** a standalone diagnostic medical device. Algorithm outputs must always be reviewed by a licensed clinician in the context of a patient's complete medical history and physical presentation. Environmental factors, sensor placement, and hardware malfunctions can result in false readings.
