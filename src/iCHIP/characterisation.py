from matplotlib import pyplot as plt
import csv
import numpy as np
import math
import mpld3
import dominate
from dominate.tags import *
from dominate.util import raw
import pkg_resources
from pathlib import Path
import os
from spyci import spyci
import pandas as pd
from scipy.signal import find_peaks
import traceback
from scipy.signal import argrelextrema

class ng_data:

    def __init__(self,filepath_vds,filepath_vgs):

        # Load files and fetch trace names
        data_vds = spyci.load_raw((filepath_vds))
        data_vgs = spyci.load_raw((filepath_vgs))

        self.datasets = {"data_vds" : data_vds, "data_vgs" : data_vgs}

        for data in self.datasets.values():
            self.trace_names = [x['name'] for x in data['vars']]

    def get_trace_names(self):
        return(self.trace_names)

    def get_trace_data(self, dataset, trace):
        return(self.datasets[dataset]['values'][trace])

    def write_csv(self, data_folder):

        # Generate CSV save path and create if not exists
        csv_path = os.path.join((Path(__file__).parents[2]), data_folder)

        if not os.path.isdir(csv_path):
            os.mkdir(csv_path)

        # Get data
        data_vds = self.datasets["data_vds"]
        data_vgs = self.datasets["data_vgs"]

        # Write vds data to csv
        with open(os.path.join(csv_path, "vds_data.csv"), 'w', newline='') as csvfile:
            vdswriter = csv.writer(csvfile, delimiter=',')

            vdswriter.writerow([x['name'] for x in data_vds['vars']])

            for line in data_vds['values']:
                vdswriter.writerow(line)

        # Write vgs data to csv
        with open(os.path.join(csv_path, "vgs_data.csv"), 'w', newline='') as csvfile:
            vgswriter = csv.writer(csvfile, delimiter=',')

            vgswriter.writerow([x['name'] for x in data_vgs['vars']])

            for line in data_vgs['values']:
                vgswriter.writerow(line)

class MOS:
    """
        A class to determine and hold inversion co-efficient paramaters

        Attributes
        ----------
        n_long : float, sub-threshold parameter
        Ispec_sq : Specific current per square
        sigma_d : DIBL parameter
        lambda_d : Velocity saturation parameter (output conductance)
        VT0 : Threshold voltage at zero substrate bias
        Lsat : Velocity saturation parameter (transconductance)

        Methods
        -------
        get_parameters():
            Returns the inversion co-efficient parameters of the chosen device
        """

    def __init__(self, vgs_data, vds_data, temp, width_long, length_long, width_short, length_short, delim=',', output_file=None):

        """
        Initialise the MOS class

                Parameters:
                        vgs_data (2D list): Data from vgs sweep. Format should be Vgs, I(long channel),
                        I(short channel). Short channel is optional, but improves results
                        vds_data (2D list): Data from vgs sweep. Format should be Vgs, I(long channel),
                        I(short channel). Short channel is optional, but improves results
                        temp (float): Temperature for characterisation
                        width_long (float): Width of long transistor in testbench (um)
                        length_long (float): Length of long transistor in testbench (um)
                        width_short (float): Width of short transistor in testbench (um)
                        length_short(float): Length of short transistor in testbench (um)
                        delim (str): Optional. If csv, provide delimiter
                        output_file: File to save HTML summary to. If not supplied, not file is written.

                Returns:
                        None
        """

        # Initialise the output parameters. If they cannot be determined, these results are
        # returned
        self.n_long = -1
        self.Ispec_sq = -1
        self.sigma_d = -1
        self.lambda_d = -1
        self.VT0 = -1
        self.lambda_c = -1
        self.lsat = -1

        # If the incoming data is already a list, store it
        if (isinstance(vds_data, list) and isinstance(vgs_data, list)):
            print("Data is list...")
            Ids_vgs = vgs_data
            Ids_vds = vds_data

        else:
            print("Input data must be list")

        # Calculate Ut constant
        self.Ut = 1.38e-23*temp/1.6e-19

        # Convert data to real. It is supplied as complex, but the complex parts
        # are zero. This suppress later ComplexWarnings about implicit cast
        Ids_vds = [[value.real for value in datapoint] for datapoint in Ids_vds]
        Ids_vgs = [[value.real for value in datapoint] for datapoint in Ids_vgs]

        # Simulation results often have some negative or zero current for very low values of vds
        # or vgs (leakage currents etc). These cause later log analyses to fail, so any negative
        # values are removed. If the short channel data exits, do it for this too.
        Ids_vds = [item for item in Ids_vds[1:] if float(item[1]) > 0]
        Ids_vgs = [item for item in Ids_vgs[1:] if float(item[1]) > 0]

        if (len(Ids_vgs[0])==3):
            Ids_vgs = [item for item in Ids_vgs[1:] if float(item[2]) > 0]

        ### EXTRACT VGS DATA ###

        # Seperate into x and y
        Ids_vgs_x = [float(item[0]) for item in Ids_vgs[1:]]
        Ids_vgs_y_long = [float(item[1]) for item in Ids_vgs[1:]]

        # If the short channel data exists, use it where appropriate, otherwise fall back to the long
        # channel data (and warn the user)
        if (len(Ids_vgs[0])==3):
            Ids_vgs_y_short = [float(item[2]) for item in Ids_vgs[1:]]
        else:
            Ids_vgs_y_short = Ids_vgs_y_long
            print("WARNING: No short channel data detected for Ids vs. Vgs. Proceeding with long"
                  "channel data, but accuracy of results will be reduced")

        ### EXTRACT VDS DATA ###

        # Seperate into x and y
        Ids_vds_x = [float(item[0]) for item in Ids_vds[1:]]
        Ids_vds_y_long = [float(item[1]) for item in Ids_vds[1:]]

        # If the short channel data exists, use it where appropriate, otherwise fall back to the long
        # channel data (and warn the user)
        if (len(Ids_vds[0])==3):
            Ids_vds_y_short = [float(item[2]) for item in Ids_vds[1:]]
        else:
            Ids_vds_y_short = Ids_vgs_y_long
            print("WARNING: No short channel data detected for Ids vs. Vds. Proceeding with long"
                  "channel data, but accuracy of results will be reduced")

        # Sort the data into ascending order (some later code assumes this
        # and slices lists based on that assumption)
        Ids_vgs_x.sort()
        Ids_vgs_y_long.sort()
        Ids_vgs_y_short.sort()
        Ids_vds_x.sort()
        Ids_vds_y_long.sort()
        Ids_vds_y_short.sort()

        # Determine the threshold voltage
        try:
            root_ids = [math.sqrt(item) for item in Ids_vgs_y_long]
            root_ids_grad_max = np.argmax(np.gradient(root_ids)/np.gradient(Ids_vgs_x))
            low_lim = root_ids_grad_max - 3
            m,c = np.polyfit(Ids_vgs_x[low_lim:root_ids_grad_max], root_ids[low_lim:root_ids_grad_max], 1)
            m_old = 0

            while (abs((m-m_old)/m) >=0.1):
                low_lim = low_lim - 1
                m_old = m
                m,c = np.polyfit(Ids_vgs_x[low_lim:root_ids_grad_max], root_ids[low_lim:root_ids_grad_max], 1)

            self.VT0 = -c/m
            fit_data_3 = [m*item+c for item in Ids_vgs_x]

            # Plot Ids vs. Vgs for Vt determination
            fig_Vt = plt.figure()
            plt.title("Sqrt(Ids) vs. Vgs for Vt Determination")
            plt.xlabel("Vgs")
            plt.ylabel("Sqrt (Ids)")
            plt.plot(Ids_vgs_x,fit_data_3)
            plt.plot(Ids_vgs_x,root_ids)
            web_content = [["Vt","Vt Determination", mpld3.fig_to_html(fig_Vt)]]

        except:
            web_content = [["Vt","Vt Determination", mpld3.fig_to_html(fig_Vt)]]

        # Prepare ids, vgs plot
        try:
            fig_vgs_ids = plt.figure()
            plt.plot(Ids_vgs_x,Ids_vgs_y_short,'o',label="Short Channel")
            plt.plot(Ids_vgs_x,Ids_vgs_y_long,'o',label="Long Channel")
            plt.legend()
            plt.title("Ids vs. Vgs for long and short channel devices")
            plt.xlabel("Vgs (V)")
            plt.ylabel("Id (A)")
            web_content.append(["vgsids", "Vgs vs. Ids", mpld3.fig_to_html(fig_vgs_ids)])
        except:
            web_content.append(["vgsids", "Vgs vs. Ids", "FAILED TO GENERATE"])

        # Prepare vds, ids plot
        try:
            fig_vds_ids = plt.figure()
            plt.title ("Ids vs. Vds")
            plt.xlabel("Vds (V)")
            plt.ylabel("Id (A)")
            plt.plot(Ids_vds_x,Ids_vds_y_long,'o',label="Long Channel")
            plt.plot(Ids_vds_x,Ids_vds_y_short,'o',label="Short Channel")
            plt.legend()
            web_content.append(["vids", "Vds vs. Ids", mpld3.fig_to_html(fig_vds_ids)])
        except Exception as e:
            web_content.append(["vids", "Vds vs. Ids", "FAILED TO GENERATE: " + str(e)])

        # Determine gm
        gm_Vgs_long = np.diff(Ids_vgs_y_long)/np.diff(Ids_vgs_x)
        gm_Vgs_short = np.diff(Ids_vgs_y_short)/np.diff(Ids_vgs_x)

        try:
            # Generate gm/Id
            gm_over_Id = gm_Vgs_long/Ids_vgs_y_long[1:]

            # Find the lower limit of good data (based on variance). Data is sometimes
            # very noisy for very low currents and this produces poor results.
            gm_over_Id_series = pd.Series(gm_over_Id)
            gm_over_Id_series_std = gm_over_Id_series.rolling(window=5).std()

            # This code finds the first time the standard deviation dips below the
            # average st dev after rising above it. The standard deviation always peaks
            # then falls, so this helps to exclude erroneous data at the start if the model
            # is of poor quality.
            gm_over_Id_series_std_av = np.mean(gm_over_Id_series_std)
            gm_over_Id_series_std_belowav = [list(gm_over_Id_series_std).index(item) for item in gm_over_Id_series_std if item < gm_over_Id_series_std_av]
            gm_over_Id_series_std_aboveav = [list(gm_over_Id_series_std).index(item) for item in gm_over_Id_series_std if item > gm_over_Id_series_std_av]
            gm_over_Id_series_std_valid = [item for item in gm_over_Id_series_std_belowav if item > gm_over_Id_series_std_aboveav[0]]
            valid_lim_index = gm_over_Id_series_std_valid[0]

            fig_gm_over_id_std_dev = plt.figure()
            plt.plot(Ids_vgs_x[:-1],[gm_over_Id_series_std_av]*len(Ids_vgs_x[:-1]))
            plt.plot(Ids_vgs_x[:-1],gm_over_Id_series_std)
            plt.plot(Ids_vgs_x[valid_lim_index],gm_over_Id_series_std[valid_lim_index],'o')
            plt.title ("gm/Id Standard Deviation vs. Vgs for Data Quality Determination")
            plt.xlabel("Vgs (V)")
            plt.ylabel("gm/Id St. Dev")

            # Add resulting plot as a tab
            web_content.append(["GmIdStdDev", "Data Quality", mpld3.fig_to_html(fig_gm_over_id_std_dev)])

            # Plot gm/Id
            fig_gm_over_id = plt.figure()
            plt.title ("gm/Id vs. Vgs")
            plt.xlabel("Vgs (V)")
            plt.ylabel("gm/Id")
            plt.plot(Ids_vgs_x[1:],gm_over_Id,'o')

            # Add a line indicating the threshold voltage
            plt.plot([self.VT0, self.VT0], [np.min(gm_over_Id), np.max(gm_over_Id)], color='red')

            # Add a line indicating the lower data limit voltage
            plt.plot([Ids_vgs_x[valid_lim_index],Ids_vgs_x[valid_lim_index]], [np.min(gm_over_Id), np.max(gm_over_Id)], color='green')

            # Add resulting plot as a tab
            web_content.append(["GmId", "Gm/Id", mpld3.fig_to_html(fig_gm_over_id)])

            # Restrict data to the limit of the valid data we just calculated. Only apply
            # to raw vgs data, and quantities generated from this data up to now. Save the
            # originals as "raw" so they can be plotted later to the effect of truncating.
            Ids_vgs_x_raw = Ids_vgs_x
            Ids_vgs_y_long_raw = Ids_vgs_y_long
            Ids_vgs_y_short_raw = Ids_vgs_y_short
            gm_Vgs_long_raw = gm_Vgs_long
            gm_Vgs_short_raw = gm_Vgs_short

            Ids_vgs_x = Ids_vgs_x[valid_lim_index:]
            Ids_vgs_y_long = Ids_vgs_y_long[valid_lim_index:]
            Ids_vgs_y_short = Ids_vgs_y_short[valid_lim_index:]
            gm_Vgs_long = gm_Vgs_long[valid_lim_index:]
            gm_Vgs_short = gm_Vgs_short[valid_lim_index:]
            gm_over_Id = gm_over_Id[valid_lim_index:]

        except Exception as e:
            web_content.append(["GmId", "Gm/Id", "FAILED TO GENERATE"+str(e)])
            print(e)

        # Extract n, Ispec and plot
        try:
            # Determine IdoverGmUt_long from good data (and raw version for plotting)
            IdoverGmUt_long = Ids_vgs_y_long[1:] / (self.Ut * gm_Vgs_long)
            IdoverGmUt_short = Ids_vgs_y_short[1:] / (self.Ut * gm_Vgs_short)
            IdoverGmUt_raw_long = Ids_vgs_y_long_raw[1:] / (self.Ut * gm_Vgs_long_raw)
            IdoverGmUt_raw_short = Ids_vgs_y_short_raw[1:] / (self.Ut * gm_Vgs_short_raw)

            lim_low = -3
            m,c = np.polyfit(np.log10(Ids_vgs_y_long[lim_low:]), np.log10(IdoverGmUt_long[lim_low:]), 1)
            m_old = m

            while (abs(m-m_old)/m >=0.1):
                lim_low = lim_low - 1
                m_old = m
                m, c = np.polyfit(np.log10(Ids_vgs_y_long[lim_low:]), np.log10(IdoverGmUt_long[lim_low:]), 1)

            # Determine n and Ispec_sq
            self.n_long = min(abs(IdoverGmUt_long))
            self.n_short = min(abs(IdoverGmUt_short))

            #i_spec_asymptote = IdoverGmUt_long[ispec_index]

            inter = (np.log10(self.n_long) - c) / m
            self.Ispec_sq = (10**inter)/(width_long/length_long)

            # Generate tangents to show how Ispec was calculated
            fit_data_x = [item for item in Ids_vgs_y_long if item > 0.9*10**inter]
            fit_data_y = [10 ** (m * item + c) for item in np.log10(fit_data_x)]

            # Plot Id/GmUt vs. Id
            fig_Id_over_gmut = plt.figure()
            plt.title ("Id/GmUt vs. Id")
            plt.xlabel("Id (A)")
            plt.ylabel("Id/GmUt")
            plt.loglog(Ids_vgs_y_long_raw[1:],IdoverGmUt_raw_long,'o')
            plt.loglog(Ids_vgs_y_short_raw[1:],IdoverGmUt_raw_short,'o')
            plt.loglog(Ids_vgs_y_long[1:],IdoverGmUt_long,'o')
            plt.loglog(fit_data_x,fit_data_y)
            plt.loglog(Ids_vgs_y_long, [self.n_long] * len(Ids_vgs_y_long))
            web_content.append(["IdGmUt","Id/GmUt",mpld3.fig_to_html(fig_Id_over_gmut)])

        except Exception as e:
            web_content.append(["IdGmUt","Id/GmUt","FAILED TO GENERATE GRAPH"+traceback.format_exc()])

        # Plot Normalised Transconductance
        try:
            fig_norm_transconductance = plt.figure()
            plt.title ("Normalised Transconductance vs. IC")
            plt.xlabel("IC")
            plt.ylabel("gm/gm_max")
            IC = Ids_vgs_y_long[1:]/((width_long/length_long)*self.Ispec_sq)
            plt.plot(IC, gm_Vgs_long / max(Ids_vgs_y_long[1:] / (self.n_long * self.Ut)))
            web_content.append(["NT","Normalised Transconductance",mpld3.fig_to_html(fig_norm_transconductance)])

        except:
            web_content.append(["NT","Normalised Transconductance","FAILED TO GENERATE"])

        # Plot Normalised Transconductance Efficiency
        try:
            fig_nte = plt.figure()
            plt.title ("Normalised Transconductance Efficiency vs. IC")
            plt.xlabel("IC")
            plt.ylabel("gm/Id")
            plt.loglog(IC, gm_Vgs_long * self.n_long * self.Ut / Ids_vgs_y_long[1:], 'o')
            web_content.append(["NTE","Normalised Transcoductance Efficiency", mpld3.fig_to_html(fig_nte)])

        except Exception as e:
            web_content.append(["NTE","Normalised Transcoductance Efficiency", "FAILED TO GENERATE: "+ str(e)])

        # Extract lambda_c
        try:
            gm_Vgs_short = np.diff(Ids_vgs_y_short)/np.diff(Ids_vgs_x)
            GmnUt_over_Id = (self.Ut * self.n_short * gm_Vgs_short) / Ids_vgs_y_short[1:]
            IC = Ids_vgs_y_short[1:]/((width_short/length_short)*self.Ispec_sq)

            diff_gmnut = np.gradient(GmnUt_over_Id)/np.gradient(IC)
            c1 = max(GmnUt_over_Id)

            fit_data_1 = [c1 for item in np.log10(IC)]

            high_lim = len(GmnUt_over_Id)
            step = 3
            low_lim = high_lim - step

            while((IC[high_lim-1] - IC[low_lim-1]) < 0.2):
                step = step + 1
                low_lim = high_lim - step

            m2_old = 0
            m2,c2 = np.polyfit(np.log10(IC[low_lim:high_lim]),np.log10(GmnUt_over_Id[low_lim:high_lim]),1)

            while (abs((m2-m2_old)/m2) >=0.1):
                high_lim = high_lim - 1
                low_lim = low_lim - 1
                m2_old = m2
                m2, c2 = np.polyfit(np.log10(IC[low_lim:high_lim]),np.log10(GmnUt_over_Id[low_lim:high_lim]),1)

            x_inter = 10**((np.log10(c1)-c2)/(m2))
            self.lambda_c = 1/x_inter
            self.lsat = length_short*1e-6 * self.lambda_c

            IC_plot = [item for item in IC if item >= 0.9*x_inter]
            fit_data_2 = [m2*item+c2 for item in np.log10(IC_plot)]

            # Plot GmnUt/Id vs. IC
            fig_gmnut_over_id = plt.figure()
            plt.title("GmnUt/Id vs. IC")
            plt.xlabel("IC")
            plt.ylabel("GmnUt/Id")
            plt.loglog(IC,GmnUt_over_Id,'o')
            plt.loglog(IC,[item for item in fit_data_1])
            plt.loglog(IC_plot,[10 ** item for item in fit_data_2])
            web_content.append(["GmnUtId","GmnUt/Id",mpld3.fig_to_html(fig_gmnut_over_id)])

        except Exception as e:
            web_content.append(["GmnUtId","GmnUt/Id","FAILED TO GENERATE: "+str(e)])

        # Extract lambda_d and sigma_d
        try:

            # Calculate gds
            gds = np.diff(Ids_vds_y_long)/np.diff(Ids_vds_x)

            # Calculate sigma_d
            self.sigma_d = gds[0]*self.Ut*self.n_short/(0.5*(Ids_vds_x[1]-Ids_vds_x[0]))

            # Plot gds vs. Vds
            fig_gds = plt.figure()
            plt.title("gds vs. Vds")
            plt.xlabel("Vds")
            plt.ylabel("gds")
            plt.plot(Ids_vds_x[1:],gds,'o')
            plt.plot([Ids_vgs_x[valid_lim_index],Ids_vgs_x[valid_lim_index]], [np.min(gds), np.max(gds)], color='green')
            web_content.append(["gds_vds","gds vs. Vds",mpld3.fig_to_html(fig_gds)])

        except Exception as e:
            web_content.append(["gdsnUtId","gdsnUt/Id","FAILED TO GENERATE: "+str(e)])

        # Normalised Output Conductance
        try:
            gdsmax = max(gds)
            gds_norm = gds/gdsmax
            IC = Ids_vds_y_short[1:]/((width_short/length_short)*self.Ispec_sq)

            high_lim = len(gds_norm)
            step = 1
            low_lim = high_lim - step

            while((IC[high_lim-1] - IC[low_lim-1]) < (0.1*(max(IC)-min(IC)))):
                step = step + 1
                low_lim = high_lim - step

            m2_old = 0
            m2,c2 = np.polyfit(np.log10(IC[low_lim:high_lim]),np.log10(gds_norm[low_lim:high_lim]),1)

            while (abs((m2-m2_old)/m2) >=0.01):
                high_lim = high_lim - 1
                low_lim = low_lim - 1
                m2_old = m2
                m2, c2 = np.polyfit(np.log10(IC[low_lim:high_lim]),np.log10(gds_norm[low_lim:high_lim]),1)

            x_inter = 10**((c2-1)/(-m2))
            self.lambda_d = 1/x_inter

            IC_plot = [item for item in IC if item >= 0.9*x_inter]
            fit_data_2 = [m2*item+c2 for item in np.log10(IC_plot)]

            # Plot normalised output conductance
            fig_noc = plt.figure()
            plt.title("Normalised Output Conductance vs. IC")
            plt.xlabel("IC")
            plt.ylabel("gds/gds_max")
            plt.loglog(IC,gds_norm,'o')
            plt.loglog(IC,[1] * len(IC))
            plt.loglog(IC_plot,[10 ** item for item in fit_data_2])
            web_content.append(["NOC","Normalised Output Transconductance", mpld3.fig_to_html(fig_noc)])

        except Exception as e:
            web_content.append(["NOC","Normalised Output Transconductance", "FAILED TO GENERATE: " + str(e)])

        # Create a summary table and add it as an extra tab
        with table() as html_table:

            with html_table.add(thead()):
                l = tr()
                l.add(th('Parameter'))
                l.add(th('Value'))
                l.add(th('Unit'))

            parameter_names = ['n', raw('Ispec<sub>&#9633;</sub>'), raw('&sigma;<sub>d</sub>'), raw('&lambda;<sub>d</sub>'), raw('V<sub>T0</sub>'), raw('L<sub>sat</sub>')]
            parameters = self.get_params()
            parameter_units = ['-','uA','-','-','V','nm']
            table_data = zip(parameter_names,parameters,parameter_units)

            for index,item in enumerate(table_data):
                l = tr()

                for j in range(3):

                    with l:
                        if j == 1:
                            if index == 1:
                                td(f'{1e6*item[j]:.2f}')
                            elif index == 2:
                                td(f'{item[j]:.4f}')
                            elif index == 5:
                                td(f'{1e9*item[j]:.2f}')
                            else:
                                td(f'{item[j]:.2f}')
                        else:
                            td(item[j])

        html_table['class'] = "table"

        web_content.append(["table","Summary Table", str(html_table)])

        # Read in saved HTML needed for output file
        template_file = (pkg_resources.resource_filename(__name__, 'resources/report_template.txt'))

        with open(template_file, "r") as text_file:
            content = text_file.readlines()

        # Generate the HTML report
        doc = dominate.document(title='Inversion Co-efficient Parameters')
        html_content = content[0] + content[1]

        with doc.head:
            raw(content[0])

        with doc.body:
            tab_list = ul(class_name="nav nav-tabs", id="myTab", role="tablist")

            for index, item in enumerate(web_content):

                if (index == 0):
                    class_type = "nav-link active"
                    aria = "true"
                else:
                    class_type = "nav-link"
                    aria = "false"

                tab_link = a(item[1], class_name=class_type, id=str(item[0]) + "-tab")
                tab_link['data-toggle'] = "tab"
                tab_link['href'] = "#" + str(item[0])
                tab_link['role'] = "tab"
                tab_link['aria-controls'] = item[0]
                tab_link['aria-selected'] = aria
                tab = li(class_name="nav-item")
                tab.add(tab_link)
                tab_list.add(tab)

            content_div = div(class_name="tab-content", id="myTabContent")

            for index, item in enumerate(web_content):

                if (index == 0):
                    class_type = "tab-pane fade active show"
                else:
                    class_type = "tab-pane fade"

                graph_div = div(raw(item[2]), class_name=class_type, id=str(item[0]), role="tabpanel")
                graph_div['aria-labelledby'] = str(item[0]) + "-tab"
                content_div.add(graph_div)

            btrp_script = [script(crossorigin="anonymous")]
            btrp_script[0]['integrity'] = "sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n"
            btrp_script[0]['src'] = "https://code.jquery.com/jquery-3.4.1.slim.min.js"

            btrp_script.append(script(crossorigin="anonymous"))
            btrp_script[1]['integrity'] = "sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
            btrp_script[1]['src'] = "https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"

            btrp_script.append(script(crossorigin="anonymous"))
            btrp_script[2]['integrity'] = "sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6"
            btrp_script[2]['src'] = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"

        if output_file != None:
            dom_file = open(output_file, "w")
            dom_file.write(str(doc))
            dom_file.close()

    def get_params(self):
        return (self.n_long, self.Ispec_sq, self.sigma_d, self.lambda_d, self.VT0, self.lsat)

if (__name__ == '__main__'):

    # This __main__ section allows the object to be run as a simple script for the
    # skywater process. To do this, fill in the device you would like to characterise
    # below and the results html file will be generated

    # Choose whether to use the raw data directly or generate csv files and use those. Here
    # this is only for testing it works with csv files since the raw data is available anyway.
    mode = "CSV"

    # Select the type you wish to characterise
    type = 'NMOS'   # NMOS or PMOS
    foundry = 'skywater'
    flavour = ''    # i.e. _lvt, _hvt, etc, etc. For the standard vt, use ''
    voltage = '3V'

    # Set the lengths to match the tests
    if voltage == '3V':
        if type == 'PMOS':
            length_short = 0.35
        else:
            length_short = 0.15

    elif voltage =='5V':
        if type == 'PMOS':
            length_short = 0.5
        else:
            length_short = 2.0

    device = type[0].lower() + str(flavour)

    # Set variables to read
    base_path = (Path(__file__).parents[0])
    filepath_vds = os.path.join(base_path,'tests','test_data',str(foundry)+'_char_'+str(type)+'_'+str(voltage)+'_vds.raw')  # Vds data path
    filepath_vgs = os.path.join(base_path,'tests','test_data',str(foundry)+'_char_'+str(type)+'_'+str(voltage)+'_vgs.raw')  # Vgs data path

    char_data = ng_data(filepath_vds,filepath_vgs)
    trace_names = char_data.get_trace_names()

    # Print available traces
    print("--------------------------")
    print("------ TRACE NAMES -------")
    print("--------------------------")

    for item in trace_names:
        print(item)

    # Get vgs data
    v = char_data.get_trace_data('data_vgs','vgs')
    i_long = char_data.get_trace_data('data_vgs','i(v'+str(device)+'_long)')
    i_short = char_data.get_trace_data('data_vgs','i(v'+str(device)+'_short)')
    vgs_data = list(zip(v,i_long,i_short))

    # Get vds data
    v = char_data.get_trace_data('data_vds','vds')
    i_long = char_data.get_trace_data('data_vds','i(v'+str(device)+'_long)')
    i_short = char_data.get_trace_data('data_vds','i(v'+str(device)+'_short)')
    vds_data = list(zip(v,i_long,i_short))

    # Run characterisation
    print("--------------------------")
    print("----- IC Parameters ------")
    print("--------------------------")
    output_file = os.path.join(Path(__file__).parents[2],"outputs","summary_"+str(foundry)+"_"+str(type)+'_'+str(voltage)+'_'+str(device)+".html")
    params_n = MOS(vgs_data, vds_data, 300, 10, 2, 10, length_short,output_file=output_file, delim='\t').get_params()
    print(params_n)
