from src.iCHIP import characterisation
from pathlib import Path
import os

def test_char(tmpdir):

    # Set variables to read
    base_path = (Path(__file__).parents[1])
    filepath_vds = os.path.join(base_path,'tests','test_data','skywater_char_PMOS_5V_vds.raw')  # Vds data path
    filepath_vgs = os.path.join(base_path,'tests','test_data','skywater_char_PMOS_5V_vgs.raw')  # Vgs data path

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
    params_n = characterisation.MOS(vgs_data, vds_data, 300, 50, 2, 50, 0.5,output_file=tmpdir.join("summary_dom.html"), delim='\t').get_params()

    # Store correct parameters
    parameters = (1.9387027797576202, 1.346720709839491e-07, 0.010676349360272895, 0.0010015113476555802, 1.0000464948301007, 3.9197444498287426e-08)

    # Check parameters
    assert(params_n,parameters)

    # Check output HTML file
    output_html = open(tmpdir.join("summary_dom.html"), 'r')
    correct_html = open(os.path.join(base_path,'tests','test_data','summary_skywater_PMOS_5V_p.html'),'r')
    assert(output_html,correct_html)
