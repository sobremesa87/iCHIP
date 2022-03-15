from src.iCHIP import characterisation
from pathlib import Path
import os

def test_char(tmpdir):

    # Set variables to read
    base_path = (Path(__file__).parents[1])
    filepath_vds = os.path.join(base_path,'tests','test_data','skywater_char_PMOS_3V_vds.raw')  # Vds data path
    filepath_vgs = os.path.join(base_path,'tests','test_data','skywater_char_PMOS_3V_vgs.raw')  # Vgs data path

    char_data = characterisation.ng_data(filepath_vds,filepath_vgs)
    trace_names = char_data.get_trace_names()

    # Get vgs data
    v = char_data.get_trace_data('data_vgs','vgs')
    i_long = char_data.get_trace_data('data_vgs','i(vp_long)')
    i_short = char_data.get_trace_data('data_vgs','i(vp_short)')
    vgs_data = list(zip(v,i_long,i_short))

    # Get vds data
    v = char_data.get_trace_data('data_vds','vds')
    i_long = char_data.get_trace_data('data_vds','i(vp_long)')
    i_short = char_data.get_trace_data('data_vds','i(vp_short)')
    vds_data = list(zip(v,i_long,i_short))

    # Run characterisation
    params_n = characterisation.MOS(vgs_data, vds_data, 300, 10, 2, 10, 0.15,output_file=tmpdir.join("summary_dom.html"), delim='\t').get_params()

    # Store correct parameters
    parameters = (1.400054689636316, 2.4682469552188534e-07, 0.002206231839745038, 0.015409204194842626, 1.0153757720807803, 1.5616410593504047e-07)

    # Check parameters
    assert(params_n,parameters)

    # Check output HTML file
    output_html = open(tmpdir.join("summary_dom.html"), 'r')
    correct_html = open(os.path.join(base_path,'tests','test_data','summary_skywater_PMOS_3V_p.html'),'r')
    assert(output_html,correct_html)
