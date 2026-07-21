import pandas as pd
import numpy as np

class FeverTranceEngine:
    def __init__(self):
        # Clinical thresholds (Celsius)
        self.FEVER_THRESHOLD = 38.0
        self.NORMAL_THRESHOLD = 37.5
        self.FLUCTUATION_THRESHOLD = 1.0
        
    def preprocess_wearable_data(self, df):
        """
        Converts minute-by-minute wearable data into daily clinical metrics.
        Expects a DataFrame with a DatetimeIndex and a 'temperature' column.
        """
        daily_stats = df.resample('1D').agg(
            temp_max=('temperature', 'max'),
            temp_min=('temperature', 'min'),
            temp_mean=('temperature', 'mean')
        )
        
        # Calculate daily diurnal fluctuation
        daily_stats['fluctuation'] = daily_stats['temp_max'] - daily_stats['temp_min']
        return daily_stats.dropna()

    def classify_pattern(self, daily_stats):
        """
        Analyzes the daily statistics array to recognize the fever pattern.
        """
        if len(daily_stats) < 2:
            return "Insufficient Data (Needs at least 48 hours)"

        max_temps = daily_stats['temp_max'].values
        min_temps = daily_stats['temp_min'].values
        fluctuations = daily_stats['fluctuation'].values
        
        # Check if the patient has a fever at all
        if not any(max_temps >= self.FEVER_THRESHOLD):
            return "Normal / Afebrile"

        days_tracked = len(max_temps)

        # 1. Check for Saddleback (Biphasic)
        # Pattern: High -> Normal/Low -> High over several days
        if days_tracked >= 4:
            for i in range(days_tracked - 3):
                phase1_high = max_temps[i] >= self.FEVER_THRESHOLD or max_temps[i+1] >= self.FEVER_THRESHOLD
                phase2_drop = min_temps[i+1] <= self.NORMAL_THRESHOLD or min_temps[i+2] <= self.NORMAL_THRESHOLD
                phase3_spike = max_temps[i+2] >= self.FEVER_THRESHOLD or max_temps[i+3] >= self.FEVER_THRESHOLD
                
                if phase1_high and phase2_drop and phase3_spike:
                    return "Saddleback (Biphasic)"

        # 2. Check for Stepladder
        # Pattern: Peak temperature increases sequentially over 3+ days
        if days_tracked >= 3:
            is_stepladder = True
            for i in range(1, min(4, days_tracked)):
                if max_temps[i] <= max_temps[i-1]:
                    is_stepladder = False
                    break
            if is_stepladder and max_temps[-1] >= self.FEVER_THRESHOLD:
                return "Stepladder"

        # General daily pattern analysis (looking at the most recent 48-72 hours)
        recent_max = max_temps[-3:]
        recent_min = min_temps[-3:]
        recent_fluc = fluctuations[-3:]
        
        # 3. Intermittent Fever
        # Spikes high but returns to normal base within the same day
        if all(recent_max >= self.FEVER_THRESHOLD) and all(recent_min <= self.NORMAL_THRESHOLD):
            return "Intermittent"
            
        # 4. Continuous (Sustained) Fever
        # Never drops to normal, fluctuation is less than 1°C
        if all(recent_min > self.NORMAL_THRESHOLD) and all(recent_fluc < self.FLUCTUATION_THRESHOLD):
            return "Continuous (Sustained)"
            
        # 5. Remittent Fever
        # Never drops to normal, fluctuation is greater than 1°C
        if all(recent_min > self.NORMAL_THRESHOLD) and all(recent_fluc >= self.FLUCTUATION_THRESHOLD):
            return "Remittent"

        return "Irregular / Undifferentiated Fever"

    def get_diagnostic_guidance(self, pattern):
        """
        Maps recognized fever patterns to likely conditions and next diagnostic steps.
        """
        guidance = {
            "Saddleback (Biphasic)": {
                "Likely Etiology": "Viral infections (Dengue, Colorado tick fever), Leptospirosis.",
                "Next Steps": "Dengue NS1 antigen / IgM, CBC (monitor platelets and hematocrit), hydration assessment."
            },
            "Stepladder": {
                "Likely Etiology": "Enteric fever (Typhoid).",
                "Next Steps": "Blood culture, Widal test, stool culture, CBC."
            },
            "Continuous (Sustained)": {
                "Likely Etiology": "Lobar pneumonia, UTI, Infective endocarditis, Typhus.",
                "Next Steps": "Chest X-ray, Urinalysis and culture, Blood cultures (x3 for endocarditis)."
            },
            "Remittent": {
                "Likely Etiology": "Viral infections, Infective endocarditis, Bronchopneumonia.",
                "Next Steps": "Echocardiogram (if murmur present), CBC with differential, CRP/ESR."
            },
            "Intermittent": {
                "Likely Etiology": "Malaria, Pyogenic abscess, Sepsis, Tuberculosis (typically evening spikes).",
                "Next Steps": "Thick and thin peripheral blood smear (Malaria), blood cultures, Chest X-ray."
            }
        }
        return guidance.get(pattern, {"Likely Etiology": "Varied", "Next Steps": "General clinical evaluation, CBC, CRP."})

    def analyze(self, df):
        daily_stats = self.preprocess_wearable_data(df)
        pattern = self.classify_pattern(daily_stats)
        guidance = self.get_diagnostic_guidance(pattern)
        return pattern, guidance

# ==========================================
# Example Usage with Synthetic Wearable Data
# ==========================================
if __name__ == "__main__":
    # Create 5 days of minute-by-minute data (5 * 24 * 60 = 7200 minutes)
    dates = pd.date_range(start='2026-07-20', periods=7200, freq='1min')
    
    # Simulate a Stepladder pattern: baseline 37.0, rising each day
    temps = []
    for day in range(5):
        base = 37.0 + (day * 0.4) # Base increases each day
        # Add diurnal fluctuation (sine wave) + some noise
        daily_curve = base + 0.8 * np.sin(np.linspace(0, 2 * np.pi, 1440)) + np.random.normal(0, 0.1, 1440)
        temps.extend(daily_curve)
        
    df_stepladder = pd.DataFrame({'temperature': temps}, index=dates)
    
    engine = FeverTranceEngine()
    pattern, guidance = engine.analyze(df_stepladder)
    
    print(f"Detected Pattern: {pattern}")
    print(f"Likely Etiology: {guidance['Likely Etiology']}")
    print(f"Next Steps: {guidance['Next Steps']}")