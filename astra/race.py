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
    rt_config = []
    traj_list = []
    radial_data_list = []
    def __init__(self, f):
        self.zip_file = f
        self.astra_config =  astra_zip.get_astra_config(f)
        self.traj_list = get_traj_list(f)
        self.radial_data_list = self.get_radial_data_list()
        self.radial_data_list.sort(key=len)
        print('init')

    def get_radial_data_list(self):
        exp_file = self.astra_config['Astra config']['exp_file'][0]
        equ_file = self.astra_config['Astra config']['equ_file'][0]
        tmp = 'dat/{0}.{1}.'.format(exp_file,equ_file)
        print(tmp)
        with ZipFile('races/'+ self.zip_file) as zip:
            return [ z.filename for z in zip.filelist if (z.filename.startswith(tmp))]

    def print_summary(self):
        print(" ======  ASTRA summary =====")
        astra_home = self.astra_config['Astra config']['astra_path']
        exp_file = self.astra_config['Astra config']['exp_file']
        equ_file = self.astra_config['Astra config']['equ_file']
    
        print('{0:12}  {1}'.format(astra_home[1], astra_home[0]))
        print('{0:12}  {1}'.format(exp_file[1], exp_file[0]))
        print('{0:12}  {1}'.format(equ_file[1], equ_file[0]))

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
        print("Number of traj "+ str(len(rays)) + "   Max N_traj "+ str(max_N_traj))
        print(f)
        plt.figure(figsize=(6,6))
        #R, Z = read_bounds("out/lcms.dat")
        #plt.plot(R, Z)
        for ray in rays:
            plt.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=1)
        plt.show()

    def few_plot_trajectories(self, list_of_num):
        #plt.figure(figsize=(6,6))
        fig, axs = plt.subplots(1, len(list_of_num))
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