#!/usr/bin/env python3
"""Gera inputs.npz para o M4IA a partir de um frame do vídeo de exemplo.

Aplica letterbox: preserva o aspect ratio do frame, escalando-o para caber
dentro do tamanho esperado pelo modelo, e preenchendo o resto com cinza.

Uso:
    python gen_yunet_input.py video5.webm inputs_yunet.npz
    python gen_yunet_input.py video5.webm inputs_yunet.npz --frame 42
    python gen_yunet_input.py video5.webm inputs_yunet.npz --mode 01
"""

import argparse
import os

import cv2
import numpy as np


INPUT_SIZE = (320, 320)        # (W, H) — YuNet espera 320x320
INPUT_NAME = "input"           # nome do tensor de entrada
PAD_VALUE = (128, 128, 128)    # cinza YOLO-style (BGR antes da conversão)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video", help="caminho do vídeo de entrada")
    p.add_argument("out", help="caminho do .npz a ser salvo")
    p.add_argument("--frame", type=int, default=0,
                   help="índice do frame a extrair (padrão: 0)")
    p.add_argument("--mode", choices=["255", "01", "imagenet"],
                   default="255",
                   help="normalização: '255'=[0,255], '01'=[0,1], "
                        "'imagenet'=mean/std (padrão: 255)")
    p.add_argument("--model-size", nargs=2, type=int,
                   default=list(INPUT_SIZE),
                   metavar=("W", "H"),
                   help="tamanho esperado pelo modelo (padrão: 320 320)")
    p.add_argument("--pad", nargs=3, type=int, default=list(PAD_VALUE),
                   metavar=("B", "G", "R"),
                   help="cor do padding em BGR (padrão: 128 128 128)")
    return p.parse_args()


def extract_frame(video_path, frame_index):
    if not os.path.isfile(video_path):
        raise SystemExit(f"erro: vídeo não encontrado: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise SystemExit(f"erro: não consegui abrir o vídeo: {video_path}")

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ok, frame = cap.read()
    cap.release()
    if not ok:
        raise SystemExit(f"erro: não consegui ler o frame {frame_index}")
    return frame


def letterbox(frame, size_wh, pad_color=(128, 128, 128)):
    """Escala preservando proporção e cola num canvas do tamanho alvo.

    Retorna (imagem_letterboxed, scale, pad_left, pad_top).
    scale e offsets permitem mapear coordenadas de volta para o frame
    original, se necessário.
    """
    target_w, target_h = size_wh
    src_h, src_w = frame.shape[:2]

    scale = min(target_w / src_w, target_h / src_h)
    new_w = int(round(src_w * scale))
    new_h = int(round(src_h * scale))

    resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    canvas = np.full((target_h, target_w, 3), pad_color, dtype=frame.dtype)
    pad_left = (target_w - new_w) // 2
    pad_top  = (target_h - new_h) // 2
    canvas[pad_top:pad_top + new_h, pad_left:pad_left + new_w] = resized

    return canvas, scale, pad_left, pad_top


def prepare_nchw(frame, size_wh, mode, pad_color):
    # BGR uint8 -> RGB uint8, com letterbox
    # Nota: letterbox opera em BGR, depois convertemos para RGB.
    boxed_bgr, scale, pad_left, pad_top = letterbox(frame, size_wh, pad_color)

    rgb = cv2.cvtColor(boxed_bgr, cv2.COLOR_BGR2RGB)
    x = rgb.astype(np.float32)

    if mode == "255":
        pass
    elif mode == "01":
        x /= 255.0
    elif mode == "imagenet":
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32) * 255.0
        std  = np.array([0.229, 0.224, 0.225], dtype=np.float32) * 255.0
        x = (x - mean) / std

    x = np.transpose(x, (2, 0, 1))
    x = np.expand_dims(x, axis=0)
    return x, scale, pad_left, pad_top


def main():
    args = parse_args()
    frame = extract_frame(args.video, args.frame)
    print(f"[INFO] frame {args.frame} lido: shape={frame.shape}, "
          f"dtype={frame.dtype}")

    x, scale, pad_left, pad_top = prepare_nchw(
        frame,
        tuple(args.model_size),
        args.mode,
        tuple(args.pad),
    )

    target_w, target_h = args.model_size
    src_h, src_w = frame.shape[:2]
    new_w = int(round(src_w * scale))
    new_h = int(round(src_h * scale))

    print(f"[INFO] letterbox: {src_w}x{src_h} -> {new_w}x{new_h} "
          f"(scale={scale:.4f}) dentro de {target_w}x{target_h}")
    print(f"[INFO] padding: left={pad_left}, top={pad_top}, "
          f"color={tuple(args.pad)} (BGR)")
    print(f"[INFO] input preparado: shape={x.shape}, dtype={x.dtype}, "
          f"mode='{args.mode}'")
    print(f"[INFO] valor: min={x.min():.3f} max={x.max():.3f} "
          f"mean={x.mean():.3f} std={x.std():.3f}")
    print(f"[INFO] tamanho: {x.nbytes / 1024:.0f} KiB "
          f"({x.nbytes / 1024 / 1024:.2f} MiB)")

    np.savez(args.out, **{INPUT_NAME: x})
    print(f"[INFO] salvo: {args.out}")


if __name__ == "__main__":
    main()
