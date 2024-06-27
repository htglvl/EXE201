from transflow.modules.detector.detector import *
from transflow.modules.ocr.ocr import *
from transflow.modules.translate.translate import *
from transflow.modules.detector.text_segment import *
from transflow.modules.render.render import *
from transflow.modules.utils import *

def main(args):
    # Get model
    ocr_model, sg_model = get_model(args)
    print('Model loaded')
    sg_output = segment_text(args, sg_model)
    print('Text segmented')
    ocr_output = get_text_from_bubble(args, ocr_model, sg_output)
    print('Text extracted')
    trs_output = translate(args, ocr_output)
    print('Text translated')
    trs_path = args.output + '/output_trs.pkl'
    render(args, trs_output)


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)