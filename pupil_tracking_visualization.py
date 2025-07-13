import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

def load_data():
    file_path = 'data/LeftEyeData.tsv'  # Το αρχείο δεδομένων δεν περιλαμβάνεται
    return pd.read_csv(file_path, sep='\t')

def find_global_axis_limits(data_df):
    timestamp_min = data_df['timestamp'].min() / 15.2
    timestamp_max = data_df['timestamp'].max() / 15.2
    deviation_min = (data_df['deviation'].min() / 100) - 0.1
    deviation_max = (data_df['deviation'].max() / 100) + 0.1
    return timestamp_min, timestamp_max, deviation_min, deviation_max

def plot_detailed_deviation(filtered_df, temp_plot_path, test_number, global_x_limits, global_y_limits):
    plt.figure(figsize=(12, 6))
    timestamps_in_sec = filtered_df['timestamp'] / 15.2
    deviation_in_mm = filtered_df['deviation'] / 100
    plt.plot(timestamps_in_sec, deviation_in_mm, label='Deviation', color='green')
    if test_number != '5':
        max_deviation_idx = filtered_df['deviation'].idxmax()
        max_deviation_timestamp_sec = int(filtered_df.loc[max_deviation_idx, 'timestamp'] / 15.2)
        max_deviation_value_mm = deviation_in_mm[max_deviation_idx]
        plt.scatter(max_deviation_timestamp_sec, max_deviation_value_mm, color='red', label='Maximum Deviation')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Deviation (mm)')
    plt.title('Pupil Deviation Over Time')
    plt.legend()
    plt.grid(True)
    plt.xlim(global_x_limits)
    plt.ylim(global_y_limits)
    plt.savefig(temp_plot_path)
    plt.close()

def plot_max_deviation_point(filtered_df, max_timestamp, max_value, temp_plot_path, test_number, global_x_limits, global_y_limits):
    if test_number == '5':
        return
    plt.figure(figsize=(6, 4))
    max_value_mm = max_value / 100
    max_timestamp_sec = int(max_timestamp / 15.2)
    plt.scatter(max_timestamp_sec, max_value_mm, color='red')
    plt.xlim(global_x_limits)
    plt.ylim(global_y_limits)
    plt.title('Maximum Pupil Deviation Point')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Deviation (mm)')
    plt.grid(True)
    plt.annotate(f"Time: {max_timestamp_sec} sec\nDeviation: {max_value_mm:.4f} mm",
                 (max_timestamp_sec, max_value_mm),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center')
    plt.savefig(temp_plot_path)
    plt.close()

def generate_pdf(plot_paths, test_name):
    output_folder = 'results'
    os.makedirs(output_folder, exist_ok=True)
    pdf_output_path = os.path.join(output_folder, f'{test_name}_results.pdf')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Pupil Deviation Analysis Results", ln=True, align='C')
    for plot_path in plot_paths:
        if plot_path:
            pdf.add_page()
            pdf.image(plot_path, x=10, y=30, w=180)
    pdf.output(pdf_output_path)
    print(f"Results saved to: {pdf_output_path}")

def visualize_test(test_choice):
    data_df = load_data()
    mean_pupil_x = data_df['pupil.x'].mean()
    mean_pupil_y = data_df['pupil.y'].mean()
    data_df['deviation'] = np.sqrt((data_df['pupil.x'] - mean_pupil_x)**2 + (data_df['pupil.y'] - mean_pupil_y)**2)

    timestamp_min, timestamp_max, deviation_min, deviation_max = find_global_axis_limits(data_df)
    global_x_limits = (timestamp_min, timestamp_max)
    global_y_limits = (deviation_min, deviation_max)

    filtered_data_df = data_df[data_df['pupil.confidence'] >= 0.6]

    output_folder = 'results'
    os.makedirs(output_folder, exist_ok=True)

    plot_paths = []
    main_plot_path = os.path.join(output_folder, f'test_{test_choice}_main_plot.png')
    plot_detailed_deviation(filtered_data_df, main_plot_path, test_choice, global_x_limits, global_y_limits)
    plot_paths.append(main_plot_path)

    result_string = None
    if test_choice != '5':
        max_deviation_idx = filtered_data_df['deviation'].idxmax()
        max_deviation_timestamp = filtered_data_df.loc[max_deviation_idx, 'timestamp']
        max_deviation_value = filtered_data_df['deviation'][max_deviation_idx]
        max_plot_path = os.path.join(output_folder, f'test_{test_choice}_max_plot.png')
        plot_max_deviation_point(filtered_data_df, max_deviation_timestamp, max_deviation_value, max_plot_path, test_choice, global_x_limits, global_y_limits)
        plot_paths.append(max_plot_path)
        result_string = f"Maximum Deviation occurs at {max_deviation_timestamp/15.2:.2f} sec with deviation {max_deviation_value/100:.4f} mm"

    test_names = {
        '1': 'test1_cover_uncover_33cm',
        '2': 'test2_cover_uncover_4_6m',
        '3': 'test3_alternatingcoverage_33cm',
        '4': 'test3_alternatingcoverage_4_6m',
        '5': 'test_oculomotor_33cm'
    }
    test_name = test_names.get(test_choice, 'test_unknown')

    generate_pdf(plot_paths, test_name)

    if result_string:
        print(result_string)

if __name__ == '__main__':
    continue_testing = True

    while continue_testing:
        test_choice = input("Which test do you want to run (1, 2, 3, 4, 5)? Choose: ")
        if test_choice in ['1', '2', '3', '4', '5']:
            visualize_test(test_choice)
        else:
            print("Invalid test number. Please enter a valid number (1, 2, 3, 4, 5).")

        continue_choice = input("Do you want to continue with another test? (yes/no): ").lower()
        if continue_choice not in ['yes', 'y']:
            continue_testing = False
