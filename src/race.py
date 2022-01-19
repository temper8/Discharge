import operator
from pickletools import read_unicodestring1 
import astra_zip

from zipfile import ZipFile

import matplotlib.pyplot as plt

import radial_data

def get_traj_list(f):
    tmp = 'lhcd/out/traj.'
    with ZipFile('races/'+ f) as zip:
        return [ z.filename for z in zip.filelist if (z.filename.startswith(tmp))]

def float_try(str):
    try:
        return float(str)
    except ValueError:
        return 0.0


class Race:
    zip_file = ""
    astra_config = []
    ray_tracing_parameters = {}
    rt_config = []
    traj_list = []
    radial_data_list = []
    def __init__(self, f):
        self.zip_file = f
        self.astra_config =  astra_zip.get_astra_config(f)
        p = astra_zip.get_rt_parameters(f)
        self.ray_tracing_parameters =  self.glue_rt_parameters(p)
        self.traj_list = get_traj_list(f)
        self.radial_data_list = self.get_radial_data_list()
        self.radial_data_list.sort(key=len)
        #print('init')

    def plot_spectrum(self):
        sp = self.ray_tracing_parameters['LH spectrum']
        fig, ax = plt.subplots(constrained_layout=True, figsize=(5, 2.5))
        ax.plot(sp['Ntor'], sp['Amp'])  

    def glue_rt_parameters(self, parameters):
        g = {}
        for key in parameters.keys():
            if key != 'LH spectrum':
                g.update(parameters[key])
        g.update({'LH spectrum':parameters['LH spectrum']})
        return g

    def get_radial_data_list(self):
        exp_file = self.astra_config['Astra config']['exp_file'][0]
        equ_file = self.astra_config['Astra config']['equ_file'][0]
        tmp = 'dat/{0}.{1}.'.format(exp_file,equ_file)
        #print(tmp)
        with ZipFile('races/'+ self.zip_file) as zip:
            list = [ z.filename for z in zip.filelist if (z.filename.startswith(tmp))]
        num = len(list)
        return [tmp+str(i) for i in range(0,num)]

        

    def rt_summary(self, options):
        lines = []
        title = 'Ray tracing parameters'
        x = (48 - len(title))//2
        lines.append(" {0} {1} {2}".format('='*x, title, '='*x))
        for o in options:
            lines.append(f" {o}:  {self.ray_tracing_parameters[o][0]} ({self.ray_tracing_parameters[o][1]})")
        return lines

    def summary(self):
        lines = []
        title = 'ASTRA summary'
        x = (48 - len(title))//2
        lines.append(" {0} {1} {2}".format('='*x, title, '='*x))
        astra_home = self.astra_config['Astra config']['astra_path']
        exp_file = self.astra_config['Astra config']['exp_file']
        equ_file = self.astra_config['Astra config']['equ_file']
        comp_name = self.astra_config['Astra config']['comp_name']
        lines.append(' {0:12}  {1}'.format(astra_home[1], astra_home[0]))
        lines.append(' {0:12}  {1}'.format(exp_file[1], exp_file[0]))
        lines.append(' {0:12}  {1}'.format(equ_file[1], equ_file[0]))
        lines.append(' {0:12}  {1}'.format(comp_name[1], comp_name[0]))        
        return lines

    def print_summary(self):
        lines = self.summary()
        for l in lines:
            print(l)

    def read_radial_data(self,f):
        with ZipFile('races/'+ self.zip_file) as zip:
            with zip.open(f) as file:
                return radial_data.read_radial_data(file)

    def read_trajectories(self, f):
        with ZipFile('races/'+ self.zip_file) as zip:
            with zip.open(f) as file:
                header = file.readline().decode("utf-8").replace('=', '_').split()

                lines = file.readlines()
                table = [line.decode("utf-8").split() for line in lines]
                table = list(filter(None, table))

                rays = []
                N_traj = 0

                for row in table:
                    if N_traj != int(row[12]):
                        N_traj = int(row[12])
                        ray = dict([ (h, []) for h in header ])
                        rays.append(ray)
                    for index, (p, item) in enumerate(ray.items()):
                        item.append(float_try(row[index]))
        return rays, N_traj

    def plot_trajectories(self, f):
        rays, max_N_traj = self.read_trajectories(f)
        #print("Number of traj "+ str(len(rays)) + "   Max N_traj "+ str(max_N_traj))
        #print(f)
        plt.figure(figsize=(6,6))
        plt.title(f)
        plt.axis('equal')
        #R, Z = read_bounds("out/lcms.dat")
        #plt.plot(R, Z)
        for ray in rays:
            plt.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=1)
        plt.show()

    def plot(self, axis, num):
        f = self.traj_list[num]
        rays, max_N_traj = self.read_trajectories(f)
        #axis.axis('equal')
        for ray in rays:
                axis.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=1)

    def few_plot_trajectories(self, list_of_num):
        #plt.figure(figsize=(6,6))
        fig, axs = plt.subplots(1, len(list_of_num), figsize=(10, 5))
        for index,t in enumerate(list_of_num):
            f = self.traj_list[t]
            rays, max_N_traj = self.read_trajectories(f)
            print("Number of traj "+ str(len(rays)) + "   Max N_traj "+ str(max_N_traj))
            print(f)
        
            #R, Z = read_bounds("out/lcms.dat")
            #plt.plot(R, Z)
            for ray in rays:
                axs[index].plot(ray['R'], ray['Z'], alpha=0.5, linewidth=1)
            #axs[index].show()