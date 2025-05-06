import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# npz folder
folder = "/mnt/HDD3/miayan/omega/CUT3R/output/rl2_zoom_in/camera"

files  = sorted(glob.glob(os.path.join(folder, "*.npz")))

traj = []
poses = []
for f in files:
    data = np.load(f)
    if "pose" in data:
        P = data["pose"]
    elif "R" in data and "t" in data:
        P = np.eye(4)
        P[:3,:3] = data["R"]
        P[:3,3]  = data["t"]
    else:
        raise KeyError(f"{f} missing 'pose' or 'R'+'t'")
    poses.append(P)
    traj.append(P[:3,3])
traj = np.stack(traj, axis=0)  # shape (N,3)

N = len(traj)
norm   = plt.Normalize(0, N-1)
cmap   = plt.get_cmap('viridis')
colors = [cmap(norm(i)) for i in range(N)]

fig = plt.figure(figsize=(7,7))
ax  = fig.add_subplot(111, projection="3d")

for i in range(N-1):
    xs = traj[i:i+2, 0]
    ys = traj[i:i+2, 2]  # depth
    zs = traj[i:i+2, 1]  # height
    ax.plot(xs, ys, zs,
            linewidth=3,
            color=colors[i])


ax.set_xlabel("X")
ax.set_ylabel("Z")
ax.set_zlabel("Y")
ax.set_title("Camera Trajectory")
ax.grid(True)
plt.tight_layout()

output_path = "camera_trajectory_rl2_zoom_in.png"
plt.savefig(output_path, dpi=300)
print(f"Saved: {output_path}")