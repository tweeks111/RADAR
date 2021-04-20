# Canvas
CANVAS_WIDTH = 700
CANVAS_HEIGHT = 700
PERSON_DIAMETER = 0.5

# Person Speed
MIN_SPEED = 0
MAX_SPEED = 10

# Cluster Radius
MIN_RADIUS = 1
MAX_RADIUS = 3

# Map Dimension
MIN_RECTANGLE = 10
MAX_RECTANGLE = 40

# TX/RX Dimension
RADAR_RADIUS = 0.3
RADAR_RADIUS_PX = 10

# Model Constants
C = 3e8     # Light Speed
f_c = 5e9   # Carrier frequency
BW = 80e6   # Bandwidth
Q = 1024    # Number of OFDM carriers
L = 64      # Number of taps in the channel, corresponding to a duration of L*Delta_tau
N_a = 4     # Number of antennas at the receiver
kappa = 0   # Number of unknown data OFDM
Delta_t = 16e-6

P_TX = 1  # Power of the transmitter
G_TX = 1  # Gain of the transmitter
G_RX = 1  # Gain of the receiver
L_TX = 1  # Losses at the transmitting side
L_RX = 1  # Losses at the receiving sid
N0_dBm = -174  # PSD of noise [dBm/Hz]
N0 = 10 ** (N0_dBm / 10 - 3)  # PSD of noise [W/Hz]
P_noise = N0 * BW

lambda_c = C / f_c      # Wavelength
d_ant = lambda_c / 2    # Distance between each antenna
Ts = 1 / BW             # Sampling time   (Delta_tau) -> fast time interval  (index i)
T = (kappa + 1) * (Q + L) * Ts  # Time between the reception of two symbols  (Delta_t) -> slow time interval (index k)
