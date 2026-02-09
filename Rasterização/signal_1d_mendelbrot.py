import numpy as np
import matplotlib.pyplot as plt

OUT_FILE = "amostragem_mandelbrot_sinal.png"

N_HR = 8192
MAX_ITER = 500

X_MIN, X_MAX = -2.5, 1.0
Y0 = 0.60

T_END = 16.0
FS = 16.0

F_PLOT_MIN = -120.0
F_PLOT_MAX = 120.0

SHOW = True


def mandelbrot_escape_1d(xs, y0, max_iter):
    C = xs + 1j * y0
    Z = np.zeros_like(C, dtype=np.complex128)

    inside = np.ones(C.shape, dtype=bool)
    counts = np.zeros(C.shape, dtype=np.int32)

    for i in range(1, max_iter + 1):
        Z[inside] = Z[inside] * Z[inside] + C[inside]
        escaped = np.abs(Z) > 2.0
        newly = escaped & inside
        counts[newly] = i
        inside &= ~escaped
        if not inside.any():
            break

    counts[counts == 0] = max_iter
    return counts, inside


def normalize_signal(counts, inside, max_iter):
    s = counts.astype(np.float64) / float(max_iter)
    s[inside] = 0.0
    s = np.clip(s, 0.0, 1.0)
    return s


def fft_mag(x, dt):
    X = np.fft.fftshift(np.fft.fft(x)) * dt
    f = np.fft.fftshift(np.fft.fftfreq(x.size, d=dt))
    return f, np.abs(X)


def main():
    t = np.linspace(0.0, T_END, N_HR, endpoint=False)
    dt = t[1] - t[0]
    FS_HR = 1.0 / dt

    xs = np.linspace(X_MIN, X_MAX, N_HR, endpoint=False)

    counts, inside = mandelbrot_escape_1d(xs, Y0, MAX_ITER)
    s = normalize_signal(counts, inside, MAX_ITER)

    Ts = 1.0 / FS
    n = np.arange(0.0, T_END + 1e-12, Ts)

    idx = np.clip(np.round(n / dt).astype(int), 0, N_HR - 1)
    s_n = s[idx]

    impulse_train = np.zeros_like(s)
    impulse_train[idx] = 1.0 / dt

    s_s = s * impulse_train

    f_s, Smag = fft_mag(s, dt)
    f_p, Pmag = fft_mag(impulse_train, dt)
    f_ss, SSmag = fft_mag(s_s, dt)

    def crop(f, m):
        sel = (f >= F_PLOT_MIN) & (f <= F_PLOT_MAX)
        return f[sel], m[sel]

    f1, m1 = crop(f_s, Smag)
    f2, m2 = crop(f_p, Pmag)
    f3, m3 = crop(f_ss, SSmag)

    m1 = m1 / (m1.max() + 1e-12)
    m2 = m2 / (m2.max() + 1e-12)
    m3 = m3 / (m3.max() + 1e-12)

    fig = plt.figure(figsize=(16, 8))
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.25)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])

    ax4 = fig.add_subplot(gs[1, 0])
    ax5 = fig.add_subplot(gs[1, 1])
    ax6 = fig.add_subplot(gs[1, 2])

    ax1.plot(t, s)
    ax1.set_title("Mandelbrot 1D Slice (Signal)")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, alpha=0.3)

    ax2.vlines(n, 0.0, 1.0, linewidth=1.0)
    ax2.set_ylim(0.0, 1.05)
    ax2.set_title("Impulse Train Sampling")
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True, alpha=0.3)

    ax3.plot(t, s, alpha=0.25)
    ax3.vlines(n, 0.0, s_n, linewidth=1.0)
    ax3.plot(n, s_n, marker="o", linestyle="None", markersize=3)
    ax3.set_title("Sampled Signal")
    ax3.set_xlabel("Time [s]")
    ax3.set_ylabel("Amplitude")
    ax3.grid(True, alpha=0.3)

    ax4.plot(f1, m1)
    ax4.set_title("Spectrum of Original Signal")
    ax4.set_xlabel("Frequency [Hz]")
    ax4.set_ylabel("Magnitude (norm)")
    ax4.grid(True, alpha=0.3)

    ax5.plot(f2, m2)
    ax5.set_title("Spectrum of Impulse Train")
    ax5.set_xlabel("Frequency [Hz]")
    ax5.set_ylabel("Magnitude (norm)")
    ax5.grid(True, alpha=0.3)

    ax6.plot(f3, m3)
    ax6.set_title("Spectrum of Sampled Signal")
    ax6.set_xlabel("Frequency [Hz]")
    ax6.set_ylabel("Magnitude (norm)")
    ax6.grid(True, alpha=0.3)

    fig.suptitle(
        f"Amostragem usando um sinal derivado do Mandelbrot (y0={Y0}, FS={FS} Hz, FS_HR≈{FS_HR:.1f} Hz)",
        fontsize=18
    )

    plt.savefig(OUT_FILE, dpi=200, bbox_inches="tight")

    if SHOW:
        plt.show()

    print(f"Saved: {OUT_FILE}")


if __name__ == "__main__":
    main()
