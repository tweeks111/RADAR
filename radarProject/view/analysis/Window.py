import tkinter as tk
import view.analysis
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np


class Window(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.resizable(False, False)
        self.title("Analysis")

        style = ttk.Style()
        style.configure("mystyle.Treeview", background='white')
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 10, 'bold'), background='lightgray')

        self.thresh_label_frame = tk.LabelFrame(self, text="Threshold :")
        self.thresh_label_frame.grid(row=1, column=0)
        yScroll_1 = tk.Scrollbar(self.thresh_label_frame, orient=tk.VERTICAL)
        self.thresh_tree = ttk.Treeview(self.thresh_label_frame, selectmode='extended', yscrollcommand=yScroll_1.set, style="mystyle.Treeview")
        yScroll_1.config(command=self.thresh_tree.yview)

        self.CACFAR_label_frame = tk.LabelFrame(self, text="CA-CFAR :")
        self.CACFAR_label_frame.grid(row=1, column=2)
        yScroll_3 = tk.Scrollbar(self.CACFAR_label_frame, orient=tk.VERTICAL)
        self.CACFAR_tree = ttk.Treeview(self.CACFAR_label_frame, selectmode='extended', yscrollcommand=yScroll_3.set, style="mystyle.Treeview")
        yScroll_3.config(command=self.CACFAR_tree.yview)

        self.configureTrees()

        self.thresh_tree.grid(row=0, column=0, columnspan=2)
        yScroll_1.grid(row=0, column=2, sticky='ns')
        self.CACFAR_tree.grid(row=0, column=0, columnspan=2)
        yScroll_3.grid(row=0, column=2, sticky='ns')

        self.combo_thresh = tk.ttk.Combobox(self.thresh_label_frame, state="readonly")
        self.combo_thresh['values'] = ('Detection Threshold', 'AoA Threshold')
        self.combo_thresh.current(0)
        self.combo_thresh.current(0)
        self.combo_thresh.grid(row=1, column=0, sticky='nsew')

        self.plot_thresh_btn = tk.Button(self.thresh_label_frame, text="Plot", command=self.plotThresh)
        self.plot_thresh_btn.grid(row=1, column=1, columnspan=2, sticky='nsew')

        self.combo_CACFAR = tk.ttk.Combobox(self.CACFAR_label_frame, state="readonly")
        self.combo_CACFAR['values'] = ('Pfa', 'Ncfar', 'AoA Threshold')
        self.combo_CACFAR.current(0)
        self.combo_CACFAR.grid(row=1, column=0, sticky='nsew')
        self.plot_CACFAR_btn = tk.Button(self.CACFAR_label_frame, text="Plot", command=self.plotCACFAR)
        self.plot_CACFAR_btn.grid(row=1, column=1, columnspan=2, sticky='nsew')

    def setTrees(self, index_param):
        self.thresh_label_frame.grid()
        self.CACFAR_label_frame.grid()

        count = [0, 0]
        for i in range(len(index_param)):
            for j in range(len(index_param[i])):
                if index_param[i][j]['detect'] == "Peak Detection":
                    self.thresh_tree.insert(parent='', index='end', values=(index_param[i][j]['N'], index_param[i][j]['M'], index_param[i][j]['thresh'], index_param[i][j]['AoA'], index_param[i][j]['RL'],\
                                                                            index_param[i][j]['est'], index_param[i][j]['NLest']))
                    count[0] = count[0] + 1
                else:
                    self.CACFAR_tree.insert(parent='', index='end', values=(index_param[i][j]['N'], index_param[i][j]['M'], index_param[i][j]['pfa'], index_param[i][j]['NCFAR'], index_param[i][j]['guard'],\
                                                                            index_param[i][j]['AoA'], index_param[i][j]['RL'], index_param[i][j]['est'], index_param[i][j]['NLest']))
                    count[1] = count[1] + 1
        if count[0] == 0:
            self.thresh_label_frame.grid_remove()
        if count[1] == 0:
            self.CACFAR_label_frame.grid_remove()

    def configureTrees(self):
        # Threshold :
        self.thresh_tree['columns'] = ('N', 'M', 'thresh', 'AoA', 'RL', 'est', 'NLest')
        self.thresh_tree['show'] = 'headings'
        self.thresh_tree['height'] = 7
        self.thresh_tree['selectmode'] = None
        self.thresh_tree.column('N', width=30, anchor='c')
        self.thresh_tree.column('M', width=30, anchor='c')
        self.thresh_tree.column('thresh', width=90, anchor='c')
        self.thresh_tree.column('AoA', width=90, anchor='c')
        self.thresh_tree.column('RL', width=90, anchor='c')
        self.thresh_tree.column('est', width=90, anchor='c')
        self.thresh_tree.column('NLest', width=90, anchor='c')

        self.thresh_tree.heading("N", text="N")
        self.thresh_tree.heading("M", text="M")
        self.thresh_tree.heading("thresh", text="RDM Threshold")
        self.thresh_tree.heading("AoA", text="AoA Threshold")
        self.thresh_tree.heading("RL", text="RL")
        self.thresh_tree.heading('est', text="Detect. Ratio")
        self.thresh_tree.heading('NLest', text="No Leak DR")

        # CA-CFAR
        self.CACFAR_tree['columns'] = ('N', 'M', 'pfa', 'NCFAR', 'guard', 'AoA', 'RL', 'est', 'NLest')
        self.CACFAR_tree['show'] = 'headings'
        self.CACFAR_tree['height'] = 7
        self.CACFAR_tree['selectmode'] = None
        self.CACFAR_tree.column('N', width=30, anchor='c')
        self.CACFAR_tree.column('M', width=30, anchor='c')
        self.CACFAR_tree.column('pfa', width=30, anchor='c')
        self.CACFAR_tree.column('NCFAR', width=40, anchor='c')
        self.CACFAR_tree.column('guard', width=40, anchor='c')
        self.CACFAR_tree.column('AoA', width=90, anchor='c')
        self.CACFAR_tree.column('RL', width=90, anchor='c')
        self.CACFAR_tree.column('est', width=90, anchor='c')
        self.CACFAR_tree.column('NLest', width=90, anchor='c')

        self.CACFAR_tree.heading('N', text='N')
        self.CACFAR_tree.heading('M', text='M')
        self.CACFAR_tree.heading('pfa', text='Pfa')
        self.CACFAR_tree.heading('NCFAR', text='Ncfar')
        self.CACFAR_tree.heading('guard', text='Guard')
        self.CACFAR_tree.heading('AoA', text='AoA Threshold')
        self.CACFAR_tree.heading('RL', text='RL')
        self.CACFAR_tree.heading('est', text='Detect. Ratio')
        self.CACFAR_tree.heading('NLest', text="No Leak DR")

    def clearAnalysis(self):
        self.thresh_tree.delete(*self.thresh_tree.get_children())
        self.CACFAR_tree.delete(*self.CACFAR_tree.get_children())

    def plotThresh(self):
        plot_type = self.combo_thresh.get()
        plot_window = tk.Toplevel(self)
        plot_window.resizable(False, False)
        fig = Figure(figsize=(6, 6))
        a = fig.add_subplot(111)
        fig.subplots_adjust(wspace=0.5)
        a.set_ylabel('Detection Ratio')
        data = self.getAllData(self.thresh_tree)

        if plot_type == "Detection Threshold":
            plot_window.title("Detect. Ratio - Detect. Threshold [dB]")
            a.set_xlabel('Detection Threshold [dB]')

            list_of_config = []
            group_list = []
            for item in data:
                N = item['N']
                M = item['M']
                AoA = item['AoA']
                RL = item['RL']
                config = (N, M, AoA, RL)

                if config in list_of_config:
                    idx = list_of_config.index(config)
                    group_list[idx].append(item)
                else:
                    list_of_config.append(config)
                    group_list.append([item])

            for list in group_list:
                thresh = np.array([float(item['thresh']) for item in list])
                est = np.array([float(item['est']) for item in list])
                sort_idx = np.argsort(thresh)
                thresh = thresh[sort_idx]
                est = est[sort_idx]
                a.plot(thresh, est,
                       label="N=" + list[0]['N'] + " M=" + list[0]['M'] + " AoA=" + list[0]['AoA'] + " RL=" + list[0]['RL'], marker='o')

        elif plot_type == 'AoA Threshold':
            plot_window.title("Detect. Ratio - AoA Threshold[dB]")
            a.set_xlabel('AoAThreshold [dB]')

            list_of_config = []
            group_list = []
            for item in data:
                N = item['N']
                M = item['M']
                thresh = item['thresh']
                RL = item['RL']
                config = (N, M, thresh, RL)

                if config in list_of_config:
                    idx = list_of_config.index(config)
                    group_list[idx].append(item)
                else:
                    list_of_config.append(config)
                    group_list.append([item])

            for list in group_list:
                AoA = np.array([float(item['AoA']) for item in list])
                est = np.array([float(item['est']) for item in list])
                sort_idx = np.argsort(AoA)
                AoA = AoA[sort_idx]
                est = est[sort_idx]
                a.plot(AoA, est,
                       label="N=" + list[0]['N'] + " M=" + list[0]['M'] + " AoA=" + list[0]['AoA'] + " RL=" + list[0][
                           'RL'], marker='o')

        a.legend(loc="upper right", prop={'size': 6})
        canvas = FigureCanvasTkAgg(fig, plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, plot_window).update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, padx=2, pady=2, expand=True)

    def plotCACFAR(self):
        plot_type = self.combo_CACFAR.get()
        plot_window = tk.Toplevel(self)
        plot_window.resizable(False, False)
        fig = Figure(figsize=(6, 6))
        a = fig.add_subplot(111)
        fig.subplots_adjust(wspace=0.5)
        a.set_ylabel('Detection Ratio')
        data = self.getAllData(self.CACFAR_tree)

        if plot_type == "Pfa":
            plot_window.title("Detect. Ratio - Pfa[log10]")
            a.set_xlabel('Pfa[log10]')
            list_of_config = []
            group_list = []
            for item in data:
                N = item['N']
                M = item['M']
                Ncfar = item['NCFAR']
                guard = item['guard']
                AoA = item['AoA']
                RL = item['RL']
                config = (N, M, Ncfar, guard, AoA, RL)

                if config in list_of_config:
                    idx = list_of_config.index(config)
                    group_list[idx].append(item)
                else:
                    list_of_config.append(config)
                    group_list.append([item])

            for list in group_list:
                pfa = np.array([float(item['pfa']) for item in list])
                est = np.array([float(item['est']) for item in list])
                sort_idx = np.argsort(pfa)
                pfa = pfa[sort_idx]
                est = est[sort_idx]
                a.plot(pfa, est, label="N="+list[0]['N']+" M="+list[0]['M']+" NCFAR="+list[0]['NCFAR']+" Guard="+list[0]['guard']+" AoA="+list[0]['AoA']+" RL="+list[0]['RL'], marker='o')

        elif plot_type == "Ncfar":
            plot_window.title("Detect. Ratio - Ncfar")
            a.set_xlabel('NCFAR')
            list_of_config = []
            group_list = []
            for item in data:
                N = item['N']
                M = item['M']
                Pfa = item['pfa']
                guard = item['guard']
                AoA = item['AoA']
                RL = item['RL']
                config = (N, M, Pfa, guard, AoA, RL)

                if config in list_of_config:
                    idx = list_of_config.index(config)
                    group_list[idx].append(item)
                else:
                    list_of_config.append(config)
                    group_list.append([item])

            for list in group_list:
                ncfar = np.array([float(item['NCFAR']) for item in list])
                est = np.array([float(item['est']) for item in list])
                sort_idx = np.argsort(ncfar)
                ncfar = ncfar[sort_idx]
                est = est[sort_idx]
                a.plot(ncfar, est, label="N="+list[0]['N']+" M="+list[0]['M']+" pfa="+list[0]['pfa']+" Guard="+list[0]['guard']+" AoA="+list[0]['AoA']+" RL="+list[0]['RL'], marker='o')

        elif plot_type == "AoA Threshold":
            plot_window.title("Detect. Ratio - AoA Threshold")
            a.set_xlabel('AoA Threshold')
            list_of_config = []
            group_list = []
            for item in data:
                N = item['N']
                M = item['M']
                Pfa = item['pfa']
                guard = item['guard']
                Ncfar = item['NCFAR']
                RL    = item['RL']
                config = (N, M, Pfa, Ncfar, guard, RL)

                if config in list_of_config:
                    idx = list_of_config.index(config)
                    group_list[idx].append(item)
                else:
                    list_of_config.append(config)
                    group_list.append([item])

            for list in group_list:
                AoA = np.array([float(item['AoA']) for item in list])
                est = np.array([float(item['est']) for item in list])
                sort_idx = np.argsort(AoA)
                AoA = AoA[sort_idx]
                est = est[sort_idx]
                a.plot(AoA, est, label="N="+list[0]['N']+" M="+list[0]['M']+" Pfa="+list[0]['pfa']+" Ncfar="+list[0]['NCFAR']+" Guard="+list[0]['guard']+" RL="+list[0]['RL'], marker='o')

        a.legend(loc="upper right", prop={'size': 6})
        canvas = FigureCanvasTkAgg(fig, plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, plot_window).update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, padx=2, pady=2, expand=True)

    def getColumn(self, tree, index):
        col = []
        rows = tree.get_children()
        for row in rows:
            col.append(float(tree.set(row, index)))
        return np.array(col)

    def getAllData(self, tree):
        rows = tree.get_children()
        data = []
        for row_idx in range(len(rows)):
            data.append(tree.set(rows[row_idx]))
        return data
