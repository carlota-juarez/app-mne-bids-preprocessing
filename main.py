# This file is a MNE python-based brainlife.io App

# Carlota Juárez Alonso

# Set up enviroment

import json
import os
import subprocess
from shutil import copyfile
from distutils.dir_util import copy_tree


# Current path

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Read the parameters from Brainlife 

with open (os.path.join(__location__, 'config.json')) as f:
    config = json.load(f)

# Entry and output paths 

bids_root = str(config['bids'])
deriv_root = os.path.join(__location__, 'out_dir')
html_report_dir = os.path.join(__location__, 'html_report')

# Ensure output directories exist

if not os.path.exists(deriv_root):
    os.makedirs(deriv_root)
if not os.path.exists(html_report_dir):
    os.makedirs(html_report_dir)

# Copy the input folder ('app1_output') in the output folder ('out_dir') to have all the data there

if config['app1_output'] and os.path.exists(config['app1_output']):
    copy_tree(config['app1_output'], deriv_root)

# Rewrite the info in the .json file into a .py file

file_name = os.path.join(__location__, 'pipeline_config.py')

# Inputs from the interface web to MNE variables

with open(file_name, 'w') as f:
    # -- General settings --

    f.write(f"bids_root = '{bids_root}'\n")
    f.write(f"deriv_root = '{deriv_root}'\n")

    if config['process_empty_room']:
        f.write(f"process_empty_room = {config['process_empty_room']}\n")

    if config['process_rest']:
        f.write(f"process_rest = {config['process_rest']}\n")

    if config['eog_channels']:
        f.write(f"eog_channels = {config['eog_channels']}\n")

    if config['eeg_bipolar_channels']:
        f.write(f"eeg_bipolar_channels = {config['eeg_bipolar_channels']}\n")
    
    if config['eeg_template_montage']:
        f.write(f"eeg_template_montage = {config['eeg_template_montage']}\n")

    if config['drop_channels']:
        f.write(f"drop_channels = {config['drop_channels']}\n")
    
    if config['plot_psd_for_runs']:
        f.write(f"plot_psd_for_runs = {config['plot_psd_for_runs']}\n")

    if config['random_state']:
        f.write(f"random_state = {config['random_state']}\n")

    # Break detection

    if config['find_breaks']:
        f.write(f"find_breaks = {config['find_breaks']}\n")
        if config['find_breaks']:
            if config['min_break_duration']:
                f.write(f"min_break_duration  = {config['min_break_duration']}\n")
            if config['t_break_annot_start_after_previous_event']:
                f.write(f"t_break_annot_start_after_previous_event  = {config['t_break_annot_start_after_previous_event']}\n")
            if config['t_break_annot_stop_before_next_event']:
                f.write(f"t_break_annot_stop_before_next_event  = {config['t_break_annot_stop_before_next_event']}\n")

    # Bad channel detection

    if config['find_flat_channels_meg']:
        f.write(f"find_flat_channels_meg = {config['find_flat_channels_meg']}\n")
    
    if config['find_noisy_channels_meg']:   
        f.write(f"find_noisy_channels_meg = {config['find_noisy_channels_meg']}\n")
    
    if config['find_bad_channels_extra_kws']:
        f.write(f"find_bad_channels_extra_kws = {config['find_bad_channels_extra_kws']}\n")

    # Maxwell filter for MEG

    if config['use_maxwell_filter']:
        f.write(f"use_maxwell_filter = {config['use_maxwell_filter']}\n")
        if config['use_maxwell_filter']:
            if config['mf_st_duration']:
                f.write(f"mf_st_duration = {config['mf_st_duration']}\n")
            if config['mf_st_correlation']:
                f.write(f"mf_st_correlation = {config['mf_st_correlation']}\n")
            if config['mf_head_origin']:
                f.write(f"mf_head_origin = {config['mf_head_origin']}\n")
            if config['mf_destination']:
                f.write(f"mf_destination = {config['mf_destination']}\n")
            if config['mf_int_order']:
                f.write(f"mf_int_order = {config['mf_int_order']}\n")
            if config['mft_ext_order']:
                f.write(f"mft_ext_order = {config['mft_ext_order']}\n")
            if config['mf_reference_run']:
                f.write(f"mf_reference_run = {config['mf_reference_run']}\n")
            if config['mf_reference_task']:
                f.write(f"mf_reference_task = {config['mf_reference_task']}\n")
            if config['mf_cal_fname']:
                f.write(f"mf_cal_fname = {config['mf_cal_fname']}\n")
            if config['mf_cal_missing']:
                f.write(f"mf_cal_missing = {config['mf_cal_missing']}\n")
            if config['mf_ctc_fname']:
                f.write(f"mf_ctc_fname = {config['mf_ctc_fname']}\n")
            if config['mf_ctc_missing']:
                f.write(f"mf_ctc_missing = {config['mf_ctc_missing']}\n")
            if config['mf_esss']:
                f.write(f"mf_esss = {config['mf_esss']}\n")
            if config['mf_esss_reject']:
                f.write(f"mf_esss_reject = {config['mf_esss_reject']}\n")
            if config['mf_mc']:
                f.write(f"mf_mc = {config['mf_mc']}\n")
            if config['mf_mc_t_window']:
                f.write(f"mf_mc_t_window = {config['mf_mc_t_window']}\n")
            if config['mf_mc_gof_limit']:
                f.write(f"mf_mc_gof_limit = {config['mf_mc_gof_limit']}\n")
            if config['mf_mc_dist_limit']:
                f.write(f"mf_mc_dist_limit = {config['mf_mc_dist_limit']}\n")
            if config['mf_mc_rotation_velocity_limit']:
                f.write(f"mf_mc_rotation_velocity_limit = {config['mf_mc_rotation_velocity_limit']}\n")
            if config['mf_filter_chpi']:
                f.write(f"mf_filter_chpi = {config['mf_filter_chpi']}\n")
            if config['mf_extra_kws']:
                f.write(f"mf_extra_kws = {config['mf_extra_kws']}\n")

    # Filtering and resampling

    if config['l_freq']:
        f.write(f"l_freq = {config['l_freq']}\n")

    if config['h_freq']:
        f.write(f"h_freq = {config['h_freq']}\n")
    
    if config['l_trans_bandwidth']:
        f.write(f"l_trans_bandwidth = {config['l_trans_bandwidth']}\n")

    if config['h_trans_bandwidth']:
        f.write(f"h_trans_bandwidth = {config['h_trans_bandwidth']}\n")

    if config['notch_freq']:
        f.write(f"notch_freq = {config['notch_freq']}\n")

    if config['notch_trans_bandwidth']:
        f.write(f"notch_trans_bandwidth = {config['notch_trans_bandwidth']}\n")

    if config['notch_widths']:
        f.write(f"notch_widths = {config['notch_widths']}\n")

    if config['zapline_fline']:
        f.write(f"zapline_fline = {config['zapline_fline']}\n")

    if config['zapline_iter']:
        f.write(f"zapline_iter = {config['zapline_iter']}\n")

    if config['notch_extra_kws']:
        f.write(f"notch_extra_kws = {config['notch_extra_kws']}\n")

    if config['bandpass_extra_kws']:
        f.write(f"bandpass_extra_kws = {config['bandpass_extra_kws']}\n")

    if config['raw_resample_sfreq']:
        f.write(f"raw_resample_sfreq = {config['raw_resample_sfreq']}\n")

    if config['epochs_decim']:
        f.write(f"epochs_decim = {config['epochs_decim']}\n")
    
    # Epochs

    if config['rename_events']:
        f.write(f"rename_events = {config['rename_events']}\n")

    if config['on_rename_missing_events']:
        f.write(f"on_rename_missing_events = {config['on_rename_missing_events']}\n")

    if config['event_repeated']:
        f.write(f"event_repeated = {config['event_repeated']}\n")

    if config['epochs_custom_metadata']:
        f.write(f"epochs_custom_metadata = {config['epochs_custom_metadata']}\n")

    if config['epochs_metadata_tmin']:
        f.write(f"epochs_metadata_tmin = {config['epochs_metadata_tmin']}\n")

    if config['epochs_metadata_tmax']:
        f.write(f"epochs_metadata_tmax = {config['epochs_metadata_tmax']}\n")

    if config['epochs_metadata_keep_first']:
        f.write(f"epochs_metadata_keep_first = {config['epochs_metadata_keep_first']}\n")

    if config['epochs_metadata_keep_last']:
        f.write(f"epochs_metadata_keep_last = {config['epochs_metadata_keep_last']}\n")

    if config['epochs_metadata_query']:
        f.write(f"epochs_metadata_query = {config['epochs_metadata_query']}\n")

    if config['epochs_tmin']:
        f.write(f"epochs_tmin = {config['epochs_tmin']}\n")

    if config['epochs_tmax']:
        f.write(f"epochs_tmax = {config['epochs_tmax']}\n")

    if config['rest_epochs_duration']:
        f.write(f"rest_epochs_duration = {config['rest_epochs_duration']}\n")

    if config['rest_epochs_overlap']:
        f.write(f"rest_epochs_overlap = {config['rest_epochs_overlap']}\n")

    if config['baseline']:
        f.write(f"baseline = {config['baseline']}\n")

    # Artifact removal

    if config['fix_stim_artifact']:
        f.write(f"fix_stim_artifact = {config['fix_stim_artifact']}\n")
        if config['fix_stim_artifact']:
            if config['stim_artifact_tmin']:
                f.write(f"stim_artifact_tmin = {config['stim_artifact_tmin']}\n")
            if config['stim_artifact_tmax']:
                f.write(f"stim_artifact_tmax = {config['stim_artifact_tmax']}\n")

    # SSP, ICA and artifact regression

    if config['regress_artifact']:
        f.write(f"regress_artifact = {config['regress_artifact']}\n")

    if config['spatial_filter']:
        f.write(f"spatial_filter = {config['spatial_filter']}\n")

    if config['process_raw_clean']:
        f.write(f"process_raw_clean = {config['process_raw_clean']}\n")

    if config['min_ecg_epochs']:
        f.write(f"min_ecg_epochs = {config['min_ecg_epochs']}\n")

    if config['min_eog_epochs']:
        f.write(f"min_eog_epochs = {config['min_eog_epochs']}\n")

    if config['n_proj_eog']:
        f.write(f"n_proj_eog = {config['n_proj_eog']}\n")

    if config['n_proj_ecg']:
        f.write(f"n_proj_ecg = {config['n_proj_ecg']}\n")

    if config['ecg_proj_from_average']:
        f.write(f"ecg_proj_from_average = {config['ecg_proj_from_average']}\n")

    if config['eog_proj_from_average']:
        f.write(f"eog_proj_from_average = {config['eog_proj_from_average']}\n")

    if config['ssp_meg']:
        f.write(f"ssp_meg = {config['ssp_meg']}\n")

    if config['ssp_reject_ecg']:
        f.write(f"ssp_reject_ecg = {config['ssp_reject_ecg']}\n")

    if config['ssp_reject_eog']:
        f.write(f"ssp_reject_eog = {config['ssp_reject_eog']}\n")

    if config['ssp_ecg_channel']:
        f.write(f"ssp_ecg_channel = {config['ssp_ecg_channel']}\n")

    if config['ica_reject']:
        f.write(f"ica_reject = {config['ica_reject']}\n")

    if config['ica_algorithm']:
        f.write(f"ica_algorithm = '{config['ica_algorithm']}'\n")

    if config['ica_l_freq']:
        f.write(f"ica_l_freq = {config['ica_l_freq']}\n")

    if config['ica_h_freq']:
        f.write(f"ica_h_freq = {config['ica_h_freq']}\n")

    if config['ica_max_iterations']:
        f.write(f"ica_max_iterations = {config['ica_max_iterations']}\n")

    if config['ica_n_components']:
        f.write(f"ica_n_components = {config['ica_n_components']}\n")

    if config['ica_decim']:
        f.write(f"ica_decim = {config['ica_decim']}\n")

    if config['ica_use_ecg_detection']:
        f.write(f"ica_use_ecg_detection = {config['ica_use_ecg_detection']}\n")

    if config['ica_ecg_threshold']:
        f.write(f"ica_ecg_threshold = {config['ica_ecg_threshold']}\n")

    if config['ica_use_eog_detection']:
        f.write(f"ica_use_eog_detection = {config['ica_use_eog_detection']}\n")

    if config['ica_eog_threshold']:
        f.write(f"ica_eog_threshold = {config['ica_eog_threshold']}\n")

    if config['ica_use_icalabel']:
        f.write(f"ica_use_icalabel = {config['ica_use_icalabel']}\n")
        if config['ica_use_icalabel']:
            if config['ica_icalabel_include']:
                f.write(f"ica_icalabel_include = {config['ica_icalabel_include']}\n")   
            if config['ica_exclusion_thresholds']:
                f.write(f"ica_exclusion_thresholds = {config['ica_exclusion_thresholds']}\n") 
            if config['ica_class_thresholds']:
                f.write(f"ica_class_thresholds = {config['ica_class_thresholds']}\n") 

    # Amplitud-based artifact rejection

    if config['reject']:
        f.write(f"reject = {config['reject']}\n")

    if config['reject_tmin']:
        f.write(f"reject_tmin = {config['reject_tmin']}\n")

    if config['reject_tmax']:
        f.write(f"reject_tmax = {config['reject_tmax']}\n")

    if config['autoreject_n_interpolate']:
        f.write(f"autoreject_n_interpolate = {config['autoreject_n_interpolate']}\n")

    f.close()

# Run python script

command = ["mne_bids_pipeline", f"--config={file_name}", "--steps=preprocessing,report"]

try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    raise e

# Find the reports and make a copy in out_html folder

for dirpaths, dirnames, filenames in os.walk(deriv_root):
    for filename in [f for f in filenames if f.endswith(".html")]:
        if not "sub-average" in filename:
            print(filename)
            copyfile(os.path.join(dirpaths, filename), os.path.join(html_report_dir, filename))