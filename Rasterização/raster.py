import argparse
import importlib
from itertools import product

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def kernel_weight(filter_name: str, dx: float, dy: float) -> float:
    """
    dx, dy: deslocamentos em unidades de pixel, relativos ao centro do pixel.
    Ex.: dx=0 no centro; dx=0.5 é meio pixel à direita.
    """
    if filter_name == "box":
        # Box: peso constante dentro do suporte
        return 1.0

    if filter_name == "hat":
        # Hat (tent) separável: (1-|x|)*(1-|y|) no suporte [-1,1]
        ax = abs(dx)
        ay = abs(dy)
        wx = 1.0 - ax if ax <= 1.0 else 0.0
        wy = 1.0 - ay if ay <= 1.0 else 0.0
        return wx * wy

    if filter_name == "gaussian":
        # Gaussiana (truncada pelo suporte no sampler)
        sigma = 0.5
        r2 = dx * dx + dy * dy
        return float(np.exp(-r2 / (2.0 * sigma * sigma)))

    raise ValueError(f"Unknown filter: {filter_name}")


def filter_support(filter_name: str) -> float:
    """
    Raio do suporte em unidades de pixel para amostrar:
      box: 0.5  (um pixel)
      hat: 1.0  (2x2 pixels de suporte)
      gaussian: 2.0 (truncada)
    """
    if filter_name == "box":
        return 0.5
    if filter_name == "hat":
        return 1.0
    if filter_name == "gaussian":
        return 2.0
    raise ValueError(f"Unknown filter: {filter_name}")


def shade_point(scene, point):
    """
    Mesma regra do raster original:
    - começa com background
    - se cair dentro de um primitivo, usa a cor do primeiro que contiver
    """
    c = np.array(scene.background.as_list(), dtype=float)
    for primitive, color in scene:
        if primitive.in_out(point):
            c = np.array([color.r, color.g, color.b], dtype=float)
            break
    return c


def main(args):
    xmin, xmax, ymin, ymax = args.window
    width, height = args.resolution

    # 3.1 - validação básica
    if args.spp < 1:
        raise ValueError("--spp must be >= 1")

    filt = args.filter.lower().strip()
    support = filter_support(filt)

    # create tensor for image: RGB
    image = np.zeros((height, width, 3), dtype=float)

    # load scene from file args.scene
    scene = importlib.import_module(args.scene).Scene()

    # escala para converter "unidades de pixel" -> mundo
    sx = (xmax - xmin) / float(width)
    sy = (ymax - ymin) / float(height)

    # amostragem estratificada determinística:
    # dividimos o quadrado do suporte em n x n e pegamos o centro de cada célula
    spp = int(args.spp)
    n = int(np.ceil(np.sqrt(spp)))  # n*n >= spp

    for j, i in tqdm(product(range(height), range(width)), total=height * width):
        # caso antigo: 1 amostra no centro
        if spp == 1:
            x = xmin + sx * (i + 0.5)
            y = ymin + sy * (j + 0.5)
            image[j, i] = shade_point(scene, (x, y))
            continue

        acc = np.zeros(3, dtype=float)
        wsum = 0.0
        taken = 0

        # pega spp amostras dentro do suporte do filtro
        for sj in range(n):
            for si in range(n):
                if taken >= spp:
                    break

                # (u,v) no [0,1] dentro da célula; usamos centro da célula
                u = (si + 0.5) / n
                v = (sj + 0.5) / n

                # mapear para [-support, support] em unidades de pixel
                dx = (2.0 * u - 1.0) * support
                dy = (2.0 * v - 1.0) * support

                w = kernel_weight(filt, dx, dy)
                if w > 0.0:
                    x = xmin + sx * (i + 0.5 + dx)
                    y = ymin + sy * (j + 0.5 + dy)
                    c = shade_point(scene, (x, y))

                    acc += w * c
                    wsum += w

                taken += 1
            if taken >= spp:
                break

        # normaliza (média ponderada)
        if wsum > 0.0:
            image[j, i] = acc / wsum
        else:
            # fallback: centro
            x = xmin + sx * (i + 0.5)
            y = ymin + sy * (j + 0.5)
            image[j, i] = shade_point(scene, (x, y))

    # save image as png using matplotlib
    plt.imsave(args.output, image, vmin=0, vmax=1, origin="lower")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Raster module main function")
    parser.add_argument("-s", "--scene", type=str, help="Scene name", default="mickey_scene")
    parser.add_argument(
        "-w",
        "--window",
        type=float,
        nargs=4,
        help="Window: xmin xmax ymin ymax",
        default=[0, 8.0, 0, 6.0],
    )
    parser.add_argument(
        "-r",
        "--resolution",
        type=int,
        nargs=2,
        help="Resolution: width height",
        default=[800, 600],
    )
    parser.add_argument("-o", "--output", type=str, help="Output file name", default="output.png")

    # 3.1 - parâmetros
    parser.add_argument(
        "--filter",
        type=str,
        default="box",
        choices=["box", "hat", "gaussian"],
        help="Anti-aliasing filter kernel: box | hat | gaussian",
    )
    parser.add_argument(
        "--spp",
        type=int,
        default=1,
        help="Samples per pixel (>=1). Use >1 to enable anti-aliasing.",
    )

    args = parser.parse_args()
    main(args)
