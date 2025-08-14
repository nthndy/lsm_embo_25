C, Z, Y, X = data.shape

# --- deskew params ---
angle_deg = 31.8
xy_um = 0.145
z_um = 0.400
px_shift_per_z = (z_um / xy_um) * np.tan(np.deg2rad(angle_deg))

# --- output array (expanded X so nothing is cropped) ---
total_shift_px = int(np.ceil((Z - 1) * px_shift_per_z))
X_expanded = X + abs(total_shift_px)
deskewed = np.zeros((C, Z, Y, X_expanded), dtype=data.dtype)

# --- base offset ---
x0 = max(0, total_shift_px)
sign = +1.0  # flip to +1.0 if it skews the wrong way

# --- deskew loop ---
for c in range(C):
    for z in tqdm(range(Z), leave=False, desc=f"Deskew C{c}"):
        shift_x = sign * z * px_shift_per_z
        canvas = np.zeros((Y, X_expanded), dtype=data.dtype)
        x_start = int(np.floor(x0 + shift_x))
        canvas[:, x_start : x_start + X] = data[c, z]
        frac = (x0 + shift_x) - np.floor(x0 + shift_x)
        if abs(frac) > 1e-6:
            canvas = shift(canvas, shift=(0, frac), order=1, mode="nearest", prefilter=False)
        deskewed[c, z] = canvas
