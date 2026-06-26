# This file is a MNE python-based brainlife.io App

# Carlota Juárez Alonso

# Set up enviroment

import json
from pathlib import Path
import subprocess
from shutil import copyfile, rmtree, copytree
import mne
import mne_bids
import logging

# Logger configuration

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)

# Current path 

__location__ = Path(__file__).resolve().parent

# Read the parameters from Brainlife 

config_path = __location__/'config.json'
if not config_path.exists():
    raise FileNotFoundError(f"The configuration file could not be found in {config_path}")

with open (config_path, 'r') as f:
    config = json.load(f)


#DE PRUEBA
#-- pasar de .edf de los datos que le mando a estructura bids--

#read folders with mne-python
# for MEG: .fif and for EEG: .edf

fname = config.get('edf')
if fname:
    logger.info(".edf file succesfully detected")

#ruta de la carpeta BIDS a crear, carpeta principal del proyecto
bids_root_path = __location__/'bids_input'

#limpiamos por si existieran previas ejecuciones
if bids_root_path.exists():
    rmtree(bids_root_path)
bids_root_path.mkdir(parents = True, exist_ok = True)

#leemos el archivo
raw = mne.io.read_raw_edf(fname, preload = False)

# configuracion de variables BIDS 

subject = '001'
task = '01'
datatype = 'eeg'
#session
#run

#bids_path es el archivo de un solo paciente 
bids_path = mne_bids.BIDSPath(subject = subject, task = task, datatype = datatype, root = bids_root_path)

#escribimos los datos en formato bids
mne_bids.write_raw_bids(raw, bids_path, overwrite = True)
logger.info("BIDS structure successfully created")


# EEG study
'''
ch_types = ['eeg']
if not ch_types:
    raise ValueError("The 'ch_types' parameter is required")
'''

# Output paths

deriv_root = __location__/'out_dir'
html_report_dir = __location__/'html_report'

# Ensure output directories exist

deriv_root.mkdir(parents = True, exist_ok = True)
html_report_dir.mkdir(parents = True, exist_ok = True)

# Rewrite the info in the .json file into a .py file

file_name = __location__/'pipeline_config.py'

# Inputs from the interface web to MNE variables

with open(file_name, 'w') as f:

    f.write(f"bids_root = '{bids_root_path}'\n")
    f.write(f"deriv_root = '{deriv_root}'\n")
    f.write(f"ch_types = ['eeg']\n")

    # Break detection

    find_breaks = config.get('find_breaks', False)
    f.write(f"find_breaks = {find_breaks}\n")
    if find_breaks:
        min_break_duration = config.get('min_break_duration')
        if min_break_duration in [None, ""]:
            min_break_duration = 15.0
        f.write(f"min_break_duration = {min_break_duration}\n")
        
        t_break_annot_start_after_previous_event = config.get('t_break_annot_start_after_previous_event')
        if t_break_annot_start_after_previous_event in [None, ""]:
            t_break_annot_start_after_previous_event = 5.0
        f.write(f"t_break_annot_start_after_previous_event = {t_break_annot_start_after_previous_event}\n")

        t_break_annot_stop_before_next_event = config.get('t_break_annot_stop_before_next_event')
        if t_break_annot_stop_before_next_event in [None, ""]:
            t_break_annot_stop_before_next_event = 5.0
        f.write(f"t_break_annot_stop_before_next_event = {t_break_annot_stop_before_next_event}\n")

    # Bad channel detection for MEG
    '''
    find_flat_channels_meg = config.get('find_flat_channels_meg', False)
    f.write(f"find_flat_channels_meg = {find_flat_channels_meg}\n")
    
    find_noisy_channels_meg = config.get('find_noisy_channels_meg', False)
    f.write(f"find_noisy_channels_meg = {find_noisy_channels_meg}\n")
    
    find_bad_channels_extra_kws = config.get('find_bad_channels_extra_kws', {})
    if find_bad_channels_extra_kws:
        f.write(f"find_bad_channels_extra_kws = {find_bad_channels_extra_kws}\n")
    '''

    # Maxwell filter for MEG
    '''
    use_maxwell_filter = config.get('use_maxwell_filter', False)
    f.write(f"use_maxwell_filter = {use_maxwell_filter}\n")
    if use_maxwell_filter:
        mf_st_duration = config.get('mf_st_duration')
        if mf_st_duration in [None, ""]:
            mf_st_duration = 10.0
        f.write(f"mf_st_duration = {mf_st_duration}\n")
            
        mf_st_correlation = config.get('mf_st_correlation')
        if mf_st_correlation in [None, ""]:
            mf_st_correlation = 0.98
        f.write(f"mf_st_correlation = {mf_st_correlation}\n")
            
        mf_head_origin = config.get('mf_head_origin', 'auto')
        if mf_head_origin:
            if isinstance(mf_head_origin, str):
                f.write(f"mf_head_origin = '{mf_head_origin}'\n")
            else:
                f.write(f"mf_head_origin = {mf_head_origin}\n")
                
        mf_destination = config.get('mf_destination', 'reference_run')
        if mf_destination:
            if isinstance(mf_destination, str):
                f.write(f"mf_destination = '{mf_destination}'\n")
            else:
                f.write(f"mf_destination = {mf_destination}\n")
                
        mf_int_order = config.get('mf_int_order')
        if mf_int_order in [None, ""]:
            mf_int_order = 8
        f.write(f"mf_int_order = {mf_int_order}\n")
            
        mf_ext_order = config.get('mf_ext_order')
        if mf_ext_order in [None, ""]:
            mf_ext_order = 3
        f.write(f"mf_ext_order = {mf_ext_order}\n")
            
        mf_reference_run = config.get('mf_reference_run', None)
        if mf_reference_run:
                f.write(f"mf_reference_run = '{mf_reference_run}'\n")

        mf_reference_task = config.get('mf_reference_task', None)
        if mf_reference_task:
            f.write(f"mf_reference_task = '{mf_reference_task}'\n")
            
        mf_cal_fname = config.get('mf_cal_fname', None)
        if mf_cal_fname:
            f.write(f"mf_cal_fname = '{mf_cal_fname}'\n")
            
        mf_cal_missing = config.get('mf_cal_missing', 'raise')
        if mf_cal_missing:
            f.write(f"mf_cal_missing = '{mf_cal_missing}'\n")
            
        mf_ctc_fname = config.get('mf_ctc_fname', None)
        if mf_ctc_fname:
            f.write(f"mf_ctc_fname = '{mf_ctc_fname}'\n")
            
        mf_ctc_missing = config.get('mf_ctc_missing', 'raise')
        if mf_ctc_missing:
            f.write(f"mf_ctc_missing = '{mf_ctc_missing}'\n")
            
        mf_esss = config.get('mf_esss')
        if mf_esss in [None, ""]:
            mf_esss = 0
        f.write(f"mf_esss = {mf_esss}\n")
            
        mf_esss_reject = config.get('mf_esss_reject', None)
        if mf_esss_reject:
            f.write(f"mf_esss_reject = {mf_esss_reject}\n")
                
        mf_mc = config.get('mf_mc', False)
        f.write(f"mf_mc = {mf_mc}\n")

        mf_mc_t_step_min = config.get('mf_mc_t_step_min')
        if mf_mc_t_step_min in [None, ""]:
            mf_mc_t_step_min = 0.01        
        f.write(f"mf_mc_t_step_min = {mf_mc_t_step_min}\n")        

        mf_mc_t_window = config.get('mf_mc_t_window', 'auto')
        if mf_mc_t_window:
            f.write(f"mf_mc_t_window = {mf_mc_t_window}\n")
            
        mf_mc_gof_limit = config.get('mf_mc_gof_limit')
        if mf_mc_gof_limit in [None, ""]:
            mf_mc_gof_limit = 0.98
        f.write(f"mf_mc_gof_limit = {mf_mc_gof_limit}\n")
            
        mf_mc_dist_limit = config.get('mf_mc_dist_limit')
        if mf_mc_dist_limit in [None, ""]:
            mf_mc_dist_limit = 0.005
        f.write(f"mf_mc_dist_limit = {mf_mc_dist_limit}\n")
            
        mf_mc_rotation_velocity_limit = config.get('mf_mc_rotation_velocity_limit', None)
        if mf_mc_rotation_velocity_limit:
            f.write(f"mf_mc_rotation_velocity_limit = {mf_mc_rotation_velocity_limit}\n")
            
        mf_filter_chpi = config.get('mf_filter_chpi', None)
        if isinstance(mf_filter_chpi, bool):
            f.write(f"mf_filter_chpi = {mf_filter_chpi}\n")
        
        mf_extra_kws = config.get('mf_extra_kws', {})
        if mf_extra_kws:
            f.write(f"mf_extra_kws = {mf_extra_kws}\n")
    '''

    # Filtering and resampling

    l_freq = config.get('l_freq', None)
    if l_freq:
        f.write(f"l_freq = {l_freq}\n")

    h_freq = config.get('h_freq', None)
    if h_freq:
        f.write(f"h_freq = {h_freq}\n")
    
    l_trans_bandwidth = config.get('l_trans_bandwidth', 'auto')
    if l_trans_bandwidth:
        f.write(f"l_trans_bandwidth = {l_trans_bandwidth}\n")

    h_trans_bandwidth = config.get('h_trans_bandwidth', 'auto')
    if h_trans_bandwidth:
        f.write(f"h_trans_bandwidth = {h_trans_bandwidth}\n")

    notch_freq = config.get('notch_freq', None)
    if notch_freq:
        f.write(f"notch_freq = {notch_freq}\n")

    notch_trans_bandwidth = config.get('notch_trans_bandwidth')
    if notch_trans_bandwidth in [None, ""]:
        notch_trans_bandwidth = 1.0
    f.write(f"notch_trans_bandwidth = {notch_trans_bandwidth}\n")

    notch_widths = config.get('notch_widths', None)
    if notch_widths:
        f.write(f"notch_widths = {notch_widths}\n")

    zapline_fline = config.get('zapline_fline', None)
    if zapline_fline:
        f.write(f"zapline_fline = {zapline_fline}\n")

    zapline_iter = config.get('zapline_iter', False)
    f.write(f"zapline_iter = {zapline_iter}\n")

    notch_extra_kws = config.get('notch_extra_kws', {})
    if notch_extra_kws:
        f.write(f"notch_extra_kws = {notch_extra_kws}\n")

    bandpass_extra_kws = config.get('bandpass_extra_kws', {})
    if bandpass_extra_kws:
        f.write(f"bandpass_extra_kws = {bandpass_extra_kws}\n")

    raw_resample_sfreq = config.get('raw_resample_sfreq', None)
    if raw_resample_sfreq:
        f.write(f"raw_resample_sfreq = {raw_resample_sfreq}\n")

    epochs_decim = config.get('epochs_decim')
    if epochs_decim in [None, ""]:
        epochs_decim = 1
    f.write(f"epochs_decim = {epochs_decim}\n")
    
    # Epoching

    rename_events = config.get('rename_events', {})
    if rename_events:
        f.write(f"rename_events = {rename_events}\n")

    on_rename_missing_events = config.get('on_rename_missing_events', 'raise')
    if on_rename_missing_events:
        f.write(f"on_rename_missing_events = '{on_rename_missing_events}'\n")

    event_repeated = config.get('event_repeated', 'error')
    if event_repeated:
        f.write(f"event_repeated = '{event_repeated}'\n")

    epochs_custom_metadata = config.get('epochs_custom_metadata', None)
    if epochs_custom_metadata:
        f.write(f"epochs_custom_metadata = '{epochs_custom_metadata}'\n")

    epochs_metadata_tmin = config.get('epochs_metadata_tmin', None)
    if epochs_metadata_tmin:
        if isinstance(epochs_metadata_tmin, str):
            f.write(f"epochs_metadata_tmin = '{epochs_metadata_tmin}'\n")
        else:
            f.write(f"epochs_metadata_tmin = {epochs_metadata_tmin}\n")

    epochs_metadata_tmax = config.get('epochs_metadata_tmax')
    if epochs_metadata_tmax:
        if isinstance(epochs_metadata_tmax, str):
            f.write(f"epochs_metadata_tmax = '{epochs_metadata_tmax}'\n")
        else:
            f.write(f"epochs_metadata_tmax = {epochs_metadata_tmax}\n")

    epochs_metadata_keep_first = config.get('epochs_metadata_keep_first', None)
    if epochs_metadata_keep_first:
        f.write(f"epochs_metadata_keep_first = {epochs_metadata_keep_first}\n")

    epochs_metadata_keep_last = config.get('epochs_metadata_keep_last', None)
    if epochs_metadata_keep_last:
        f.write(f"epochs_metadata_keep_last = {epochs_metadata_keep_last}\n")

    epochs_metadata_query = config.get('epochs_metadata_query', None)
    if epochs_metadata_query:
        f.write(f"epochs_metadata_query = '{epochs_metadata_query}'\n")
    
    conditions = config.get('conditions', None)
    if conditions:
        f.write(f"conditions = {conditions}\n")

    epochs_tmin = config.get('epochs_tmin')
    if epochs_tmin in [None, ""]:
        epochs_tmin = -0.2
    f.write(f"epochs_tmin = {epochs_tmin}\n")

    epochs_tmax = config.get('epochs_tmax')
    if epochs_tmax in [None, ""]:
        epochs_tmax = 0.5
    f.write(f"epochs_tmax = {epochs_tmax}\n")

    rest_epochs_duration = config.get('rest_epochs_duration', None)
    if rest_epochs_duration:
        f.write(f"rest_epochs_duration = {rest_epochs_duration}\n")

    rest_epochs_overlap = config.get('rest_epochs_overlap', None)
    if rest_epochs_overlap:
        f.write(f"rest_epochs_overlap = {rest_epochs_overlap}\n")

    baseline = config.get('baseline', (None, 0))
    if baseline:
        f.write(f"baseline = {baseline}\n")

    # Artifact removal

    # 1. Stimulation artifact

    fix_stim_artifact = config.get('fix_stim_artifact', False)
    f.write(f"fix_stim_artifact = {fix_stim_artifact}\n")
    if fix_stim_artifact:
        stim_artifact_tmin = config.get('stim_artifact_tmin')
        if stim_artifact_tmin in [None, ""]:
            stim_artifact_tmin = 0.0
        f.write(f"stim_artifact_tmin = {stim_artifact_tmin}\n")

        stim_artifact_tmax = config.get('stim_artifact_tmax')
        if stim_artifact_tmax in [None, ""]:
            stim_artifact_tmax = 0.01
        f.write(f"stim_artifact_tmax = {stim_artifact_tmax}\n")

    # 2. SSP, ICA and artifact regression

    regress_artifact = config.get('regress_artifact', None)
    if regress_artifact:
        f.write(f"regress_artifact = {regress_artifact}\n")

    spatial_filter = config.get('spatial_filter', None)
    if spatial_filter:
        if isinstance(spatial_filter, str):
            f.write(f"spatial_filter = '{spatial_filter}'\n")
        else:
            f.write(f"spatial_filter = {spatial_filter}\n")

    process_raw_clean = config.get('process_raw_clean', True)
    f.write(f"process_raw_clean = {process_raw_clean}\n")

    min_ecg_epochs = config.get('min_ecg_epochs')
    if min_ecg_epochs in [None, ""]:
        min_ecg_epochs = 5
    f.write(f"min_ecg_epochs = {min_ecg_epochs}\n")

    min_eog_epochs = config.get('min_eog_epochs')
    if min_eog_epochs in [None, ""]:
        min_eog_epochs = 5
    f.write(f"min_eog_epochs = {min_eog_epochs}\n")

    f.write("n_proj_eog = {'n_eeg': 1}\n")
    f.write("n_proj_ecg = {'n_eeg': 1}\n")

    ecg_proj_from_average = config.get('ecg_proj_from_average', True)
    f.write(f"ecg_proj_from_average = {ecg_proj_from_average}\n")

    eog_proj_from_average = config.get('eog_proj_from_average', True)
    f.write(f"eog_proj_from_average = {eog_proj_from_average}\n")

    '''
    ssp_meg = config.get('ssp_meg', 'auto')
    if ssp_meg:
            f.write(f"ssp_meg = '{ssp_meg}'\n")
    '''
  
    ssp_reject_ecg = config.get('ssp_reject_ecg', None)
    if ssp_reject_ecg:
        if isinstance(ssp_reject_ecg, str):
            f.write(f"ssp_reject_ecg = '{ssp_reject_ecg}'\n")
        else:
            f.write(f"ssp_reject_ecg = {ssp_reject_ecg}\n")

    ssp_reject_eog = config.get('ssp_reject_eog', None)
    if ssp_reject_eog:
        if isinstance(ssp_reject_eog, str):
            f.write(f"ssp_reject_eog = '{ssp_reject_eog}'\n")
        else:
            f.write(f"ssp_reject_eog = {ssp_reject_eog}\n")

    ssp_ecg_channel = config.get('ssp_ecg_channel', None)
    if ssp_ecg_channel:
        if isinstance(ssp_ecg_channel, str):
            f.write(f"ssp_ecg_channel = '{ssp_ecg_channel}'\n")
        else:
            f.write(f"ssp_ecg_channel = {ssp_ecg_channel}\n")

    ica_reject = config.get('ica_reject', None)
    if ica_reject:
        if isinstance(ica_reject, str):
            f.write(f"ica_reject = '{ica_reject}'\n")
        else:
            f.write(f"ica_reject = {ica_reject}\n")

    ica_algorithm = config.get('ica_algorithm')
    if ica_algorithm:
        f.write(f"ica_algorithm = '{ica_algorithm}'\n")

    ica_l_freq = config.get('ica_l_freq')
    if ica_l_freq in [None, ""]:
        ica_l_freq = 1.0
    f.write(f"ica_l_freq = {ica_l_freq}\n")

    ica_h_freq = config.get('ica_h_freq')
    if ica_h_freq:
        f.write(f"ica_h_freq = {ica_h_freq}\n")

    ica_max_iterations = config.get('ica_max_iterations')
    if ica_max_iterations in [None, ""]:
        ica_max_iterations = 500
    f.write(f"ica_max_iterations = {ica_max_iterations}\n")

    ica_n_components = config.get('ica_n_components', None)
    if ica_n_components:
        f.write(f"ica_n_components = {ica_n_components}\n")

    ica_decim = config.get('ica_decim', None)
    if ica_decim:
        f.write(f"ica_decim = {ica_decim}\n")

    ica_use_ecg_detection = config.get('ica_use_ecg_detection', True)
    f.write(f"ica_use_ecg_detection = {ica_use_ecg_detection}\n")

    ica_ecg_threshold = config.get('ica_ecg_threshold')
    if ica_ecg_threshold in [None, ""]:
        ica_ecg_threshold = 0.1
    f.write(f"ica_ecg_threshold = {ica_ecg_threshold}\n")

    ica_use_eog_detection = config.get('ica_use_eog_detection', True)
    f.write(f"ica_use_eog_detection = {ica_use_eog_detection}\n")

    ica_eog_threshold = config.get('ica_eog_threshold')
    if ica_eog_threshold in [None, ""]:
        ica_eog_threshold = 3.0
    f.write(f"ica_eog_threshold = {ica_eog_threshold}\n")

    ica_use_icalabel = config.get('ica_use_icalabel', False)
    f.write(f"ica_use_icalabel = {ica_use_icalabel}\n")
    if ica_use_icalabel:
        ica_icalabel_include = config.get('ica_icalabel_include', ('brain', 'other'))
        if ica_icalabel_include:
            f.write(f"ica_icalabel_include = {ica_icalabel_include}\n")

        ica_exclusion_thresholds = config.get('ica_exclusion_thresholds')
        if ica_exclusion_thresholds:
            f.write(f"ica_exclusion_thresholds = {ica_exclusion_thresholds}\n")

        ica_class_thresholds = config.get('ica_class_thresholds')
        if ica_class_thresholds:
            f.write(f"ica_class_thresholds = {ica_class_thresholds}\n")

    # 3. Amplitud-based artifact rejection

    reject = config.get('reject', None)
    if reject:
        if isinstance(reject, str):
            f.write(f"reject = '{reject}'\n")
        else:
            f.write(f"reject = {reject}\n")

    reject_tmin = config.get('reject_tmin', None)
    if reject_tmin:
        f.write(f"reject_tmin = {reject_tmin}\n")

    reject_tmax = config.get('reject_tmax', None)
    if reject_tmax:
        f.write(f"reject_tmax = {reject_tmax}\n")

    autoreject_n_interpolate = config.get('autoreject_n_interpolate')
    if autoreject_n_interpolate:
        f.write(f"autoreject_n_interpolate = {autoreject_n_interpolate}\n")

# Run python script

command = ["python3", "-m", "mne_bids_pipeline", f"--config={file_name}", "--steps=init,preprocessing,report"]

try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    raise e

# Find the reports and make a copy in out_html folder

real_deriv_root = deriv_root.resolve()

for path in real_deriv_root.rglob("*.html"):
    if "sub-average" not in path.name:
        logger.info(f"{path.name} copied to the output")
        copyfile(path, html_report_dir/path.name)

