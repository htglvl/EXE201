# Transflow
## Setup & Install
1. Setup environment: `python3 -m venv transflow`
2. Activate environment: `source transflow/bin/activate`
3. Install requirement packages: `pip install -r requirements.txt`
4. Install pretrained weight from [ondrive](https://fptuniversity-my.sharepoint.com/:f:/g/personal/khanhdqhe171671_fpt_edu_vn/Ev5oqZDV_-NCh3Pkv7uCPZYBekVgO5Z2xI1s8fsNguWCVg?e=UN1wZE)
    - [Detect Model](https://fptuniversity-my.sharepoint.com/:u:/g/personal/khanhdqhe171671_fpt_edu_vn/EZcflcRo1SlGpodat_jSDNkB4KWB8UFu1MHfa-FM_FlMRw?e=QqS3Kg)
    - [Segment Model](https://fptuniversity-my.sharepoint.com/:u:/g/personal/khanhdqhe171671_fpt_edu_vn/EckRFiNXJUNEnTGUQF_kiz8BTeKFkUwGLvKiZroOMqDEcg?e=Qsi6w5)
5. Save pretrained weight in `checkpoints` folder
6. Download [Sample Dataset](https://fptuniversity-my.sharepoint.com/:u:/g/personal/khanhdqhe171671_fpt_edu_vn/EXnzZ9LoVhlNlg9Cfum4JkEBhY-kuBzTPIIQSry5DHuGKA?e=mRyKsD) to `dataset` folder

## Detect bubble text
`
python3 bubble_text_detector.py --image path_to_image_or_image_folder
`
## Test Pipeline
![doc/pipeline.png](doc/pipeline.png)

_NOTE: replace inference options in [scripts/test_pipeline.sh](scripts/test_pipeline.sh)_

`
bash scripts/test_pipeline.sh
`