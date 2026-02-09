import numpy as np
import matplotlib.pyplot as plt

OUT_FILE = "mandelbrot.png"

WIDTH = 1200
HEIGHT = 800
MAX_ITER = 500

X_MIN, X_MAX = -2.5, 1.0
Y_MIN, Y_MAX = -1.2, 1.2

SS = 1
SHOW = True


def mandelbrot_escape_counts(xmin, xmax, ymin, ymax, width, height, max_iter):
    xs = np.linspace(xmin, xmax, width, dtype=np.float64)
    ys = np.linspace(ymin, ymax, height, dtype=np.float64)
    X, Y = np.meshgrid(xs, ys)
    C = X + 1j * Y

    Z = np.zeros_like(C, dtype=np.complex128)
    counts = np.zeros(C.shape, dtype=np.int32)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(1, max_iter + 1):
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        escaped = np.abs(Z) > 2.0
        newly_escaped = escaped & mask
        counts[newly_escaped] = i
        mask &= ~escaped
        if not mask.any():
            break

    counts[counts == 0] = max_iter
    return counts


def render_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter, ss=1):
    ss = int(ss)
    if ss < 1:
        raise ValueError("SS must be >= 1")

    if ss == 1:
        return mandelbrot_escape_counts(xmin, xmax, ymin, ymax, width, height, max_iter)

    w_hi = width * ss
    h_hi = height * ss
    counts_hi = mandelbrot_escape_counts(xmin, xmax, ymin, ymax, w_hi, h_hi, max_iter)

    counts_hi = counts_hi.reshape(height, ss, width, ss)
    counts = counts_hi.mean(axis=(1, 3))
    return counts


def main():
    counts = render_mandelbrot(
        X_MIN, X_MAX, Y_MIN, Y_MAX,
        WIDTH, HEIGHT, MAX_ITER,
        ss=SS
    )

    img = counts.astype(np.float64)
    img = (img - img.min()) / (img.max() - img.min() + 1e-12)

    plt.imsave(OUT_FILE, img, origin="lower")

    if SHOW:
        plt.figure()
        plt.imshow(img, origin="lower")
        plt.title("Mandelbrot")
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    main()
