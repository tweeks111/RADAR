import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
import scipy.special as sp
import numpy as np


class RightPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.map_dim = [0, 0]
        self.param_frame = tk.LabelFrame(self, text="Parameters")
        self.param_frame.configure(padx=5, pady=5)
        self.param_frame.grid_columnconfigure(1, weight=1)
        self.param_frame.pack(fill=tk.X)
        tk.Label(self.param_frame, text="M :").grid(row=2, column=0, sticky='sw')
        self.m_scale = tk.Scale(self.param_frame, from_=16, to=128, orient=tk.HORIZONTAL, resolution=16)
        self.m_scale.grid(row=2, column=1, sticky='nsew')
        self.m_scale.set(64)
        tk.Label(self.param_frame, text="N :").grid(row=3, column=0, sticky='sw')
        self.n_scale = tk.Scale(self.param_frame, from_=16, to=128, orient=tk.HORIZONTAL, resolution=16)
        self.n_scale.grid(row=3, column=1, sticky='nsew')
        self.n_scale.set(64)
        tk.Label(self.param_frame, text="Detection :").grid(row=4, column=0, sticky='sw')
        self.combo_detect = tk.ttk.Combobox(self.param_frame, state="readonly")
        self.combo_detect['values'] = ('Peak Detection', 'CA-CFAR') #'OS-CFAR'
        self.combo_detect.current(0)
        self.combo_detect.grid(row=4, column=1, sticky='nsew')
        self.combo_detect.bind("<<ComboboxSelected>>", self.detectionEvent)
        self.label_thresh = tk.Label(self.param_frame, text="Detection\nThreshold :")
        self.label_thresh.grid(row=5, column=0, sticky='sw')
        self.detect_thresh = tk.Scale(self.param_frame, orient=tk.HORIZONTAL, from_=-50, to=-150, resolution=10)
        self.detect_thresh.grid(row=5, column=1, sticky='nsew')
        self.detect_thresh.set(-90)
        self.proba_label = tk.Label(self.param_frame, text="Pᶠᵃ [log10]:")
        self.proba_label.grid(row=6, column=0, sticky='sw')
        self.proba_label.grid_remove()
        self.proba_scale = tk.Scale(self.param_frame, orient=tk.HORIZONTAL, from_=-1, to=-10, resolution=1)
        self.proba_scale.grid(row=6, column=1, sticky='nsew')
        self.proba_scale.set(-9)
        self.proba_scale.grid_remove()
        self.proba_btn = tk.Button(self.param_frame, text="\u2193")
        self.proba_btn.grid(row=6, column=2, sticky='s')
        self.proba_btn.grid_remove()
        self.NCFAR_label = tk.Label(self.param_frame, text="Nᶜᶠᵃʳ :")
        self.NCFAR_label.grid(row=7, column=0, sticky='sw')
        self.NCFAR_label.grid_remove()
        self.NCFAR_scale = tk.Scale(self.param_frame, orient=tk.HORIZONTAL, from_=10, to=50, resolution=10)
        self.NCFAR_scale.grid(row=7, column=1, sticky='nsew')
        self.NCFAR_scale.set(20)
        self.NCFAR_scale.grid_remove()
        self.NCFAR_btn = tk.Button(self.param_frame, text="\u2193")
        self.NCFAR_btn.grid(row=7, column=2, sticky='s')
        self.NCFAR_btn.grid_remove()
        self.guard_label = tk.Label(self.param_frame, text="Guard Cells :")
        self.guard_label.grid(row=8, column=0, sticky='sw')
        self.guard_label.grid_remove()
        self.guard_scale = tk.Scale(self.param_frame, orient=tk.HORIZONTAL, from_=0, to=6, resolution=2)
        self.guard_scale.grid(row=8, column=1, sticky='nsew')
        self.guard_scale.set(2)
        self.guard_scale.grid_remove()
        self.guard_btn = tk.Button(self.param_frame, text="\u2193")
        self.guard_btn.grid(row=8, column=2, sticky='s')
        self.guard_btn.grid_remove()

        self.pfa_var = tk.StringVar()
        self.pfa_label = tk.Label(self.param_frame, textvariable=self.pfa_var)
        self.pfa_label.grid(row=11, column=1, sticky='nsew')
        self.pfa_label.grid_remove()
        tk.Label(self.param_frame, text="AoA\nThreshold :").grid(row=12, column=0, sticky='sw')
        self.aoa_thresh = tk.Scale(self.param_frame, orient=tk.HORIZONTAL, from_=0, to=-10, resolution=1)
        self.aoa_thresh.grid(row=12, column=1, sticky='nsew')
        self.aoa_thresh.set(-6)
        self.aoa_btn = tk.Button(self.param_frame, text="\u2193")
        self.aoa_btn.grid(row=12, column=2, sticky='e')
        self.range_check = tk.IntVar()
        self.range_check.set(1)
        self.range_btn = tk.Checkbutton(self.param_frame, text="Range leakage", variable=self.range_check, onvalue=1, offvalue=0)
        self.range_btn.grid(row=13, column=1, sticky='e')

        self.sim_frame = tk.LabelFrame(self, text="Time simulation")
        self.sim_frame.configure(padx=5, pady=5)
        self.sim_frame.grid_columnconfigure(1, weight=1)
        self.sim_frame.pack(fill=tk.X)
        tk.Label(self.sim_frame, text="Duration [s]:").grid(row=0, column=0, sticky='sw')
        self.time_scale = tk.Scale(self.sim_frame, from_=1, to=20, orient=tk.HORIZONTAL, resolution=1)
        self.time_scale.grid(row=0, column=1, sticky='nsew')
        self.time_scale.set(10)

        tk.Label(self.sim_frame, text="RDM Freq. [Hz]:").grid(row=1, column=0, sticky='sw')
        self.rdm_scale = tk.Scale(self.sim_frame, from_=1, to=4, orient=tk.HORIZONTAL, resolution=1)
        self.rdm_scale.grid(row=1, column=1, sticky='nsew')
        self.rdm_scale.set(2)

        self.run_btn = tk.Button(self.sim_frame, text="Run Simulation")
        self.run_btn['state'] = 'disabled'
        self.run_btn.grid(row=2, column=1, columnspan=3)

        self.analysis_frame = tk.LabelFrame(self, text="Instant analysis")
        self.analysis_frame.configure(padx=5, pady=5)
        self.analysis_frame.pack(fill=tk.Y)
        self.analysis_frame.grid_columnconfigure(1, weight=1)

        style = ttk.Style()
        style.configure("mystyle.Treeview", background='white')
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 10, 'bold'), background='lightgray')

        self.yScroll_1 = tk.Scrollbar(self.analysis_frame, orient=tk.VERTICAL)
        self.thresh_tree = ttk.Treeview(self.analysis_frame, selectmode='extended', yscrollcommand=self.yScroll_1.set,
                                        style="mystyle.Treeview")
        self.yScroll_1.config(command=self.thresh_tree.yview)

        self.thresh_tree.grid(row=1, column=0, columnspan=2)
        self.yScroll_1.grid(row=1, column=2, sticky='ns')

        self.yScroll_2 = tk.Scrollbar(self.analysis_frame, orient=tk.VERTICAL)
        self.CACFAR_tree = ttk.Treeview(self.analysis_frame, selectmode='extended', yscrollcommand=self.yScroll_2.set,
                                        style="mystyle.Treeview")
        self.yScroll_2.config(command=self.CACFAR_tree.yview)
        self.CACFAR_tree.grid(row=1, column=0, columnspan=2)
        self.yScroll_2.grid(row=1, column=2, stick='ns')

        self.CACFAR_tree.grid_remove()
        self.yScroll_2.grid_remove()

        self.configureTrees()

        self.add_btn = tk.Button(self.analysis_frame, text="Add")
        self.add_btn.grid(row=2, column=2)
        self.remove_btn = tk.Button(self.analysis_frame, text="Remove")
        self.remove_btn['state'] = 'disabled'
        self.remove_btn.grid(row=2, column=1, sticky='e')
        self.clear_btn = tk.Button(self.analysis_frame, text="Clear")
        self.clear_btn.grid(row=2, column=0, sticky='w')

        tk.Label(self.analysis_frame, text="Nb. of iteration for\neach parameter :").grid(row=3, column=0, sticky='sw')
        self.run_scale = tk.Scale(self.analysis_frame, from_=10, to=1000, orient=tk.HORIZONTAL, resolution=10)
        self.run_scale.grid(row=3, column=1, sticky='nsew')
        self.run_scale.set(50)
        self.analysis_btn = tk.Button(self.analysis_frame, text="Run Analysis")
        self.analysis_btn['state'] = 'disabled'
        self.analysis_btn.grid(row=4, column=0, columnspan=2)

        self.progress_bar = Progressbar(self, orient=tk.HORIZONTAL, mode='determinate')
        self.progress_bar.pack(fill=tk.X)

    def configureTrees(self):
        # Threshold :
        self.thresh_tree['columns'] = ('N', 'M', 'thresh', 'AoA', 'RL')
        self.thresh_tree['show'] = 'headings'
        self.thresh_tree['height'] = 7
        self.thresh_tree['selectmode'] = None
        self.thresh_tree.column('N', width=30, anchor='c', stretch=False)
        self.thresh_tree.column('M', width=30, anchor='c', stretch=False)
        self.thresh_tree.column('thresh', width=90, anchor='c', stretch=False)
        self.thresh_tree.column('AoA', width=80, anchor='c', stretch=False)
        self.thresh_tree.column('RL', width=80, anchor='c', stretch=False)

        self.thresh_tree.heading("N", text="N")
        self.thresh_tree.heading("M", text="M")
        self.thresh_tree.heading("thresh", text="Detec. Thresh.")
        self.thresh_tree.heading("AoA", text="AoA Thresh.")
        self.thresh_tree.heading('RL', text="Range Leak.")

        # CA-CFAR
        self.CACFAR_tree['columns'] = ('N', 'M', 'pfa', 'NCFAR', 'guard', 'AoA', 'RL')
        self.CACFAR_tree['show'] = 'headings'
        self.CACFAR_tree['height'] = 7
        self.CACFAR_tree['selectmode'] = None
        self.CACFAR_tree.column('N', width=30, anchor='c')
        self.CACFAR_tree.column('M', width=30, anchor='c')
        self.CACFAR_tree.column('pfa', width=30, anchor='c')
        self.CACFAR_tree.column('NCFAR', width=40, anchor='c')
        self.CACFAR_tree.column('guard', width=40, anchor='c')
        self.CACFAR_tree.column('AoA', width=80, anchor='c')
        self.CACFAR_tree.column('RL', width=80, anchor='c')

        self.CACFAR_tree.heading('N', text='N')
        self.CACFAR_tree.heading('M', text='M')
        self.CACFAR_tree.heading('pfa', text='Pfa')
        self.CACFAR_tree.heading('NCFAR', text='Ncfar')
        self.CACFAR_tree.heading('guard', text='Guard')
        self.CACFAR_tree.heading('AoA', text='AoA Thresh.')
        self.CACFAR_tree.heading('RL', text='Range Leak.')

    def setMapDim(self, map_dim):
        self.map_dim = map_dim

    def bar(self, value):
        self.progress_bar['value'] = round(100 * value / self.time_scale.get())
        self.progress_bar.update_idletasks()

    def barAnalysis(self, value):
        self.progress_bar['value'] = round(100 * value / self.run_scale.get())
        self.progress_bar.update_idletasks()

    def addParam(self, param):
        if param['detect'] == "Peak Detection":
            self.thresh_tree.insert(parent='', index='end', iid=param['idx'], values=(param['N'], param['M'], param['thresh'], param['AoA'], param['RL']))
        else:
            self.CACFAR_tree.insert(parent='', index='end', iid=param['idx'], values=(param['N'], param['M'], param['pfa'], param['NCFAR'], param['guard'], param['AoA'], param['RL']))

        self.remove_btn['state'] = "normal"

    def removeParam(self, items):
        detection_type = self.combo_detect.get()
        if detection_type == "Peak Detection":
            for item in items:
                self.thresh_tree.delete(item)
            if len(self.thresh_tree.get_children()) == 0:
                self.remove_btn['state'] = "disabled"
        else:
            for item in items:
                self.CACFAR_tree.delete(item)
            if len(self.CACFAR_tree.get_children()) == 0:
                self.remove_btn['state'] = "disabled"

    def detectionEvent(self, event):
        event.widget.master.focus_set()
        self.changeDetectionMode()

    def changeDetectionMode(self):
        if self.combo_detect.get() == "Peak Detection":
            if len(self.thresh_tree.get_children()) > 0:
                self.remove_btn['state'] = "normal"
            else:
                self.remove_btn['state'] = "disabled"

            self.yScroll_2.grid_remove()
            self.CACFAR_tree.grid_remove()
            self.yScroll_1.grid()
            self.thresh_tree.grid()

            self.proba_label.grid_remove()
            self.proba_scale.grid_remove()
            self.proba_btn.grid_remove()
            self.NCFAR_label.grid_remove()
            self.NCFAR_scale.grid_remove()
            self.NCFAR_btn.grid_remove()
            self.guard_label.grid_remove()
            self.guard_scale.grid_remove()
            self.guard_btn.grid_remove()
            self.pfa_label.grid_remove()
            self.label_thresh.grid()
            self.detect_thresh.grid()

        else:
            if len(self.CACFAR_tree.get_children()) > 0:
                self.remove_btn['state'] = "normal"
            else:
                self.remove_btn['state'] = "disabled"

            self.yScroll_1.grid_remove()
            self.thresh_tree.grid_remove()
            self.yScroll_2.grid()
            self.CACFAR_tree.grid()

            self.label_thresh.grid_remove()
            self.detect_thresh.grid_remove()
            self.pfa_label.grid_remove()
            self.guard_label.grid()
            self.guard_scale.grid()
            self.guard_btn.grid()
            self.proba_label.grid()
            self.proba_scale.grid()
            self.proba_btn.grid()
            self.NCFAR_label.grid()
            self.NCFAR_scale.grid()
            self.NCFAR_btn.grid()

    def updateNScale(self, N):
        if N == 16:
            self.NCFAR_scale.configure(from_=10, to=10)
            self.guard_scale.configure(from_=0, to=2)
        elif N == 32:
            self.NCFAR_scale.configure(from_=10, to=20)
            self.guard_scale.configure(from_=0, to=6)
        elif N == 48:
            self.NCFAR_scale.configure(from_=10, to=30)
            self.guard_scale.configure(from_=0, to=6)
        else:
            self.NCFAR_scale.configure(from_=10, to=50)
            self.guard_scale.configure(from_=0, to=6)

    # ------
    # GET

    def getNM(self):
        return self.n_scale.get(), self.m_scale.get()

    def getDetectionMode(self):
        return self.combo_detect.get()

    def getDetectionThreshold(self):
        return self.detect_thresh.get()

    def getPfa(self):
        return self.proba_scale.get()

    def getNCFAR(self):
        return self.NCFAR_scale.get()

    def getGuardCells(self):
        return self.guard_scale.get()

    def getAngleThreshold(self):
        return self.aoa_thresh.get()

    def getRangeLeak(self):
        return self.range_check.get() == 1
