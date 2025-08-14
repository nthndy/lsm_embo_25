C, Z, Y, X = image.shape

angle_deg = 31.8
xy_um = 0.145
z_um  = 0.400
px_shift_per_z = (z_um / xy_um) * np.tan(np.deg2rad(angle_deg))

max_shift = int(np.ceil(abs((Z - 1) * px_shift_per_z)))
X_expanded = X + max_shift
deskewed = np.zeros((C, Z, Y, X_expanded), dtype=image.dtype)

x0 = max_shift // 2
sign = +1.0  # positive sign as requested

for c in range(C):
    for z in tqdm(range(Z), leave=False, desc=f"Deskew C{c}"):
        x_pos = x0 + sign * z * px_shift_per_z
        x_int = int(np.floor(x_pos))
        frac  = x_pos - x_int

        x_start = max(0, min(X_expanded - X, x_int))
        canvas = np.zeros((Y, X_expanded), dtype=image.dtype)
        canvas[:, x_start : x_start + X] = image[c, z]

        if abs(frac) > 1e-6:
            canvas = shift(canvas, shift=(0, frac), order=1, mode="nearest", prefilter=False)

        deskewed[c, z] = canvas
