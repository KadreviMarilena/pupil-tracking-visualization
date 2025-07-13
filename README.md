# Pupil Tracking Data Visualization

This repository contains custom **Python scripts** for parsing and visualizing **pupil tracking data**.

---

## Description

This project was developed as a **data visualization module** for analyzing pupil tracking data captured via [EyeRecToo](https://github.com/tcsantini/EyeRecToo) — an open-source eye tracking framework.

The scripts process `.tsv` data files and generate visual outputs to support research and analysis.

---

## Features

- Parses `.tsv` files exported from EyeRecToo (e.g. `LeftEyeData.tsv`, `RightEyeData.tsv`)
- Extracts pupil coordinates and tracking metadata
- Generates plots and statistics with `matplotlib` and `pandas`
- Modular Python scripts for different light conditions or test cases

---

## Dependencies

- Python 3.x
- `pandas`
- `matplotlib`

---

##  How It Works

1. **Collect Data:** Use EyeRecToo to record and export pupil tracking data (`.tsv` files).
2. **Run Scripts:** Use the Python scripts to parse the files and generate plots.
3. **Analyze:** The results can help in visual analysis of pupil behavior in different conditions.

---

## Data Privacy

- **No real measurement data** or visual output is included in this repository to protect privacy.

---

## License 
EyeRecToo is licensed under GPL.



