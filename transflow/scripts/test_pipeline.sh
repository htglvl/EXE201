

python3 pipeline.py \
    --image transflow/dataset/sample_en \
    --output TEST \
    --device cuda:0 \
    --save-dt-output \
    --ocr-lang en \
    --save-ocr-output \
    --font-path transflow/fonts/AndikaNewBasic-B.ttf \
    --font-size 50 \