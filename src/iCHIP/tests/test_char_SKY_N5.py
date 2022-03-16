from src.iCHIP import characterisation
from pathlib import Path
import os

def test_char(tmpdir):

    # Set variables to read
    base_path = (Path(__file__).parents[1])
    filepath_vds = os.path.join(base_path,'tests','test_data','skywater_char_NMOS_5V_vds.raw')  # Vds data path
    filepath_vgs = os.path.join(base_path,'tests','test_data','skywater_char_NMOS_5V_vgs.raw')  # Vgs data path

    char_data = characterisation.ng_data(filepath_vds,filepath_vgs)
    trace_names = char_data.get_trace_names()

    # Get vgs data
    v = char_data.get_trace_data('data_vgs','vgs')
    i_long = char_data.get_trace_data('data_vgs','i(vn_long)')
    i_short = char_data.get_trace_data('data_vgs','i(vn_short)')
    vgs_data = list(zip(v,i_long,i_short))

    # Get vds data
    v = char_data.get_trace_data('data_vds','vds')
    i_long = char_data.get_trace_data('data_vds','i(vn_long)')
    i_short = char_data.get_trace_data('data_vds','i(vn_short)')
    vds_data = list(zip(v,i_long,i_short))

    # Run characterisation
    params_n = characterisation.MOS(vgs_data, vds_data, 300, 10, 2, 10, 0.5,output_file=tmpdir.join("summary_dom.html"), delim='\t').get_params()

    # Store correct parameters
    parameters = (2.281016829049344, 1.9375607776957512e-05, 0.04332317944534455, 0.003573302448059258, 0.7627638368901664, 3.9482935585242906e-07)

    # Check parameters
    assert(params_n,parameters)

    # Check output HTML file
    output_html = open(tmpdir.join("summary_dom.html"), 'r')
    correct_html = open(os.path.join(base_path,'tests','test_data','summary_skywater_NMOS_5V_n.html'),'r')
    assert(output_html,correct_html)
