from src.iCHIP import characterisation
from pathlib import Path
import os

def test_char(tmpdir):

    # Set variables to read
    base_path = (Path(__file__).parents[1])
    filepath_vds = os.path.join(base_path,'tests','test_data','skywater_char_NMOS_1V8_vds.raw')  # Vds data path
    filepath_vgs = os.path.join(base_path,'tests','test_data','skywater_char_NMOS_1V8_vgs.raw')  # Vgs data path

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
    params_n = characterisation.MOS(vgs_data, vds_data, 300, 10, 2, 10, 0.15,output_file=tmpdir.join("summary_dom.html"), delim='\t').get_params()

    # Store correct parameters
    parameters = (1.6505308962852658, 3.17056116525344e-06, 0.011318680078314934, 0.055066575985261705, 0.5394141464229076, 1.0397946053854577e-07)

    # Check parameters
    assert(params_n,parameters)

    # Check output HTML file
    output_html = open(tmpdir.join("summary_dom.html"), 'r')
    correct_html = open(os.path.join(base_path,'tests','test_data','summary_skywater_NMOS_1V8_n.html'),'r')
    assert(output_html,correct_html)
