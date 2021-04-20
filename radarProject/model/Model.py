from model.Cluster import Cluster
from model.Point import Point
import numpy as np
import scipy.stats
from scipy.signal import find_peaks
from cmath import *
import math
from Constants import *

bin_i = np.arange(-Ts / 2, (Q + 1 / 2) * Ts, Ts)


class Model:
    # -----
    # INIT
    def __init__(self):
        self.map_dim = [0, 0]
        self.clusters_list = []
        self.points = []
        self.tx_pos = [0, 0]
        self.rx_pos = [0, 0]
        self.d = 0

        self.M = 64  # Number of OFDM symbols used for averaging in channel estimation
        self.N = 64  # Number of channel estimations to obtain one RDM

        self.d_res = 0
        self.f_res = 0
        self.v_res = 0
        self.T_dwell = 0
        self.alpha_res = 0

        self.v1 = None
        self.v2 = None
        self.d_smaller_d_res = False

    def initModel(self, N, M):
        self.computeResolutionParameters(N, M)

        self.v1 = np.arange(0, N * M)
        self.v2 = np.arange(0, N_a)
        self.initClusters()

    # --------------
    # COMPUTATIONS

    def computeResolutionParameters(self, N, M):
        self.d_res = C / (2 * BW)
        self.f_res = 1 / (N * M * Delta_t)
        self.v_res = lambda_c / (2 * N * M * Delta_t)
        self.T_dwell = N * M * Delta_t
        self.alpha_res = 3

    def computeRDM(self, N, M, RL):
        h = np.zeros((Q, N * M, N_a), dtype=np.complex64)  # range slow-time map

        for point in self.points:
            d_tx, d_rx, DoA, f_d = point.computeParameters(self.tx_pos, self.rx_pos)
            tau_n = (d_tx + d_rx) / C
            P_RXn = (P_TX * G_TX * G_RX * (lambda_c / (d_tx * d_rx)) ** 2) / (L_RX * L_TX * (4 * pi) ** 3)

            if not RL:
                idx = (np.searchsorted(bin_i, tau_n, side='right') - 1)
                h[idx, :, :] += sqrt(P_RXn) \
                                     * exp(-1j * 2 * pi * f_c * tau_n) \
                                     * np.outer(np.exp(1j * 2 * pi * self.v1 * f_d * T),
                                                np.exp(1j * 2 * pi * self.v2 * (d_ant / lambda_c) * sin(DoA)))
            else:
                for idx in range(0, Q):
                    h[idx, :, :] += sqrt(P_RXn) \
                                         * exp(-1j * 2 * pi * f_c * tau_n) \
                                         * np.outer(np.exp(1j * 2 * pi * self.v1 * f_d * T),
                                                    np.exp(1j * 2 * pi * self.v2 * (d_ant / lambda_c) * sin(DoA))) \
                                         * np.sinc(BW * (tau_n - idx * Ts))  # range leakage

        rng = np.random.default_rng()
        n = rng.normal(0, scale=np.sqrt(P_noise / 2), size=(Q, M * N, N_a, 2))

        h += n[:, :, :, 0] + n[:, :, :, 1] * 1j
        h2 = np.reshape(h, (Q, N, M, N_a))
        h_avg = np.squeeze(np.mean(h2, axis=2))
        blackman2D = np.tile(np.blackman(N), (Q, 1))
        blackman3D = np.repeat(np.expand_dims(blackman2D, axis=2), repeats=N_a, axis=2)
        h_wdw = np.multiply(h_avg, blackman3D)
        RDM = np.fft.fftshift(np.fft.fft(h_wdw, n=N, axis=1), axes=1)
        return RDM

    def computeNoLeakageDetectionMap(self, interval):
        list = []
        range_vect = np.arange(0, 16 * self.d_res, self.d_res)
        f_vect = interval * self.f_res
        for point in self.points:
            _, d_rx, _, f_d = point.computeParameters(self.tx_pos, self.rx_pos)
            i = (np.searchsorted(range_vect, d_rx, side='right') - 1)
            j = (np.searchsorted(f_vect, f_d, side='right') - 1)
            if [i, j] not in list:
                list.append([i, j])
        return list

    # ----------
    # CLUSTERS

    def initClusters(self):
        self.points.clear()
        for cluster in self.clusters_list:
            if cluster.is_point == 0:
                temp_pos_list = poissonPointProcess(cluster)
            else:
                temp_pos_list = np.array([[cluster.getX()], [cluster.getY()]])
            v = cluster.getSpeed()
            theta = cluster.getAngle()
            color = cluster.getColor()
            for i in range(0, temp_pos_list.shape[1]):
                self.points.append(Point(temp_pos_list[0, i], temp_pos_list[1, i], v, theta, lambda_c, color))

    def addCluster(self, r, x, y, v, theta, lambda0, color, is_point):
        self.clusters_list.append(Cluster(r, x, y, v, theta, lambda0, color, is_point))

    def removeCluster(self, index):
        del self.clusters_list[index]

    def updateClusterSettings(self, r, x, y, v, theta, lambda0, index):
        self.clusters_list[index].updateClusterSettings(r, x, y, v, theta, lambda0)

    def setIsPoint(self, is_point, index):
        self.clusters_list[index].setIsPoint(is_point)

    # ---------
    # SIMULATION

    def updatePointsPosition(self, t):
        pos_list = []
        for point in self.points:
            [new_x, new_y] = point.computeNewPos(t)
            if new_x < 0 or new_x > self.map_dim[0]:
                point.oppositeVX()
            if new_y < 0 or new_y > self.map_dim[1]:
                point.oppositeVY()
            point.updatePos(t)
            pos_list.append(point.getPos())

        return pos_list

    def runSimulation(self, detection_list):
        N, M = detection_list['N'], detection_list['M']
        RL = detection_list['RL']
        RDM = self.computeRDM(N, M, RL)
        ncfar = 0
        guard = 0
        detection_mode = detection_list['detect']
        thresh_angle = detection_list['AoA']

        if detection_mode == "Peak Detection":
            RDAC_reshape = RDM[0:16, int(N / 4):3 * int(N / 4), :]
            no_leak_idx = self.computeNoLeakageDetectionMap(np.arange(-int(N / 4), int(N / 4)))
            x = np.arange(-int(N / 4) * self.v_res, int(N / 4) * self.v_res, self.v_res)
            z = 20 * np.log10(np.abs(RDAC_reshape[:, :, 0]))
        else:
            ncfar = detection_list['NCFAR']
            guard = detection_list['guard']
            RDAC_reshape = RDM[0:int(Q / 2), :, :]
            no_leak_idx = self.computeNoLeakageDetectionMap(np.arange(-int(N / 2), int(N / 2)))
            x = np.arange(-int(N / 2 - ncfar / 2 - guard / 2) * self.v_res,
                          int(N / 2 - ncfar / 2 - guard / 2) * self.v_res, self.v_res)
            z = 20 * np.log10(np.abs(RDAC_reshape[0:16, int(ncfar / 2 + guard / 2):int(N - ncfar / 2 - guard / 2), 0]))
        y = np.arange(0, 16 * self.d_res, self.d_res)

        detection_map, idx_list = detectionMap(np.abs(RDAC_reshape[:, :, 0]), detection_list, N)

        # TODO : avoid the computation on the Q elements
        AoA_list, est_nb_points = computeAllAoA(RDAC_reshape, idx_list, thresh_angle)
        _, no_leak_nb_points = computeAllAoA(RDAC_reshape, no_leak_idx, thresh_angle)

        if detection_mode == "Peak Detection":
            dmap = detection_map
        else:
            dmap = detection_map[0:16, int(ncfar / 2 + guard / 2):int(N - ncfar / 2 - guard / 2)]

        return x, y, z, dmap, AoA_list, est_nb_points, no_leak_nb_points

    # -----------
    # ANALYSIS

    def runAnalysis(self, RDM, detection_list):
        N, M = detection_list['N'], detection_list['M']
        detection_mode = detection_list['detect']
        thresh_angle = detection_list['AoA']

        # TODO: if possible try to find a way to avoid using only 16 samples for the range

        if detection_mode == "Peak Detection":
            RDAC_reshape = RDM[0:16, int(N / 4):3 * int(N / 4), :]
            no_leak_idx = self.computeNoLeakageDetectionMap(np.arange(-int(N / 4), int(N / 4)))
        else:
            RDAC_reshape = RDM[0:int(Q / 2), :, :]
            no_leak_idx = self.computeNoLeakageDetectionMap(np.arange(-int(N / 2), int(N / 2)))
        detection_map, idx_list = detectionMap(np.abs(RDAC_reshape[:, :, 0]), detection_list, N)

        AoA_list, est_nb_points = computeAllAoA(RDAC_reshape[0:16, :, :], idx_list, thresh_angle)
        _, no_leak_nb_points = computeAllAoA(RDAC_reshape[0:16, :, :], no_leak_idx, thresh_angle)

        return est_nb_points, no_leak_nb_points

    # -----
    # GET

    def getClusterSettings(self, index):
        return self.clusters_list[index].getClusterSettings()

    def getPointsPosition(self):
        pos_list = []
        for point in self.points:
            pos_list.append([point.getX(), point.getY()])
        return pos_list

    def getPointsColor(self):
        color_list = []
        for point in self.points:
            color_list.append(point.getColor())
        return color_list

    def getRadarPosition(self):
        return self.tx_pos, self.rx_pos

    def getRadarIsSmaller(self):
        self.d = math.sqrt((self.tx_pos[0] - self.rx_pos[0]) ** 2 + (self.tx_pos[1] - self.rx_pos[1]) ** 2)
        if self.d < self.d_res:
            self.d_smaller_d_res = True
        else:
            self.d_smaller_d_res = False
        return self.d_smaller_d_res

    def getNbPoints(self):
        return len(self.points)

    # -----
    # SET

    def setMapDim(self, map_dim):
        self.map_dim = map_dim

    def setRadarPos(self, tx_pos, rx_pos):
        self.tx_pos = tx_pos
        self.rx_pos = rx_pos


def musicAoa(h_r):
    h_r = np.transpose(h_r)
    R = np.dot(h_r, np.transpose(h_r.conj()))
    [D, V] = np.linalg.eig(R)  # eigenvalue decomposition of R. V = eigenvectors, D = eigenvalues
    I = np.argsort(-np.abs(D))
    D = -np.sort(-np.abs(D))

    V = V[:, I]
    Us = V[:, 0]
    Un = V[:, 1:]
    G = np.dot(Un, np.transpose(Un.conj()))
    angles = np.arange(-90, 90.05, 0.05)
    # Check multiplication of vector
    s = np.sin(angles * pi / 180)
    v = np.exp(1j * 2 * pi * f_c / 3e8 * d_ant * np.dot(np.arange(N_a).reshape(N_a, 1), s.reshape(1, s.size)))

    music_spectrum = np.zeros(angles.size, dtype=complex)
    for k in range(angles.size):
        music_spectrum[k] = 1 / np.dot(np.dot(v[:, k].conj(), G), v[:, k])

    music_spectrum = music_spectrum / np.max(abs(music_spectrum))
    return music_spectrum


def poissonPointProcess(cluster):
    lambda0 = cluster.getLambda0()
    nb_points = 0
    while nb_points == 0:
        nb_points = scipy.stats.poisson(lambda0 * cluster.getArea()).rvs()
    r = cluster.getRadius() * np.random.uniform(0.0, 1.0, nb_points)
    theta = 2 * pi * np.random.uniform(0, 1, nb_points)
    x0 = [math.cos(i) for i in theta]
    y0 = [math.sin(i) for i in theta]
    x1 = np.multiply(r, x0)
    y1 = np.multiply(r, y0)
    x = [i + cluster.getX() for i in x1]
    y = [i + cluster.getY() for i in y1]

    return np.array([x, y])


def detectionMap(RDM, detection_list, N):
    detection_map = np.zeros(RDM.shape)
    idx_list = []
    detection_mode = detection_list['detect']
    if detection_mode != "Peak Detection":
        ncfar = int(detection_list['NCFAR'])
        guard = int(detection_list['guard'])
        min_j = int(ncfar / 2 + guard / 2)
        # max_j = int(N - ncfar / 2 - guard / 2)
        RDM_zeropad = np.zeros((RDM.shape[0] + ncfar + guard, RDM.shape[1] + ncfar + guard))
        RDM_zeropad[min_j:-min_j, min_j:-min_j] = RDM
        RDM_counter = np.zeros((RDM.shape[0] + ncfar + guard, RDM.shape[1] + ncfar + guard))
        RDM_counter[min_j:-min_j, min_j:-min_j] = 1
        pfa = detection_list['pfa']

        for i in range(min_j, RDM_zeropad.shape[0] - min_j):
            for j in range(min_j, N + min_j):
                sum_RDM = np.sum(np.square(RDM_zeropad[i - min_j:i + min_j + 1, j - min_j:j + min_j + 1])) \
                          - np.sum(np.square(
                    RDM_zeropad[i - int(guard / 2):i + int(guard / 2 + 1), j - int(guard / 2):j + int(guard / 2 + 1)]))
                div = np.sum(RDM_counter[i - min_j:i + min_j + 1, j - min_j:j + min_j + 1]) - np.sum(
                    RDM_counter[i - int(guard / 2):i + int(guard / 2 + 1), j - int(guard / 2):j + int(guard / 2 + 1)])
                Pn = sum_RDM / div

                alpha = N * ((10 ** pfa) ** (-1 / ncfar) - 1)
                T = alpha * Pn
                if RDM[i - min_j, j - min_j] > np.sqrt(T):
                    detection_map[i - min_j, j - min_j] = 1
                    idx_list.append([i - min_j, j - min_j])

    else:
        thresh_detection = int(detection_list['thresh'])
        for i in range(RDM.shape[0]):
            idx, _ = find_peaks(RDM[i, :], height=10 ** (thresh_detection / 20))
            for j in range(len(idx)):
                detection_map[i, idx[j]] = 1
                idx_list.append([i, idx[j]])

    return detection_map, idx_list


def computeAllAoA(RDM, idx_list, thresh_angle):
    AoA_list = []
    est_nb_points = 0
    h_r = np.zeros((len(idx_list), N_a), dtype=complex)
    for i in range(len(idx_list)):
        for j in range(N_a):
            h_r[i, j] = RDM[idx_list[i][0], idx_list[i][1], j]
        AoA_list.append(10 * np.log10(np.abs(musicAoa(np.array(h_r[i, :])[np.newaxis]))))
        peaks, _ = find_peaks(AoA_list[i], height=thresh_angle)
        est_nb_points = est_nb_points + len(peaks)
    return AoA_list, est_nb_points
