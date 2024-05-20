python3 detector.py \
    --image dataset/GarakutayaManta \
    --output TEST \
    --device cuda:0 \
    --dt-weight checkpoints/comic-speech-bubble-detector.pt \
    --save-crop \
    --save-dt-output \