from PIL import Image
from pathlib import Path
import statistics
import argparse
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')

# 70 levels of grey
gscale1 = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of grey
gscale2 = r'@%#*+=-:. '

result = list()
tmp = ''

parser = argparse.ArgumentParser(description='Converts an image to ASCII art txt file')
parser.add_argument('infile', type=str, help='Which file to convert')
parser.add_argument('columns', metavar='cols', type=int, help='Number of columns in txt file')
parser.add_argument('--levels', dest='levels',
                    help='Choose 1 to use 70 levels of grey or choose 2 to use 10 levels of grey',
                    default=1, type=int, choices=[1, 2])
parser.add_argument('outfile', type=str, help='Name of file to write')

args = parser.parse_args()
input_filename = Path(args.infile)
cols = args.columns
if args.levels == 2:
    gray_scale = gscale2
else:
    gray_scale = gscale1
output_filename = Path(args.outfile)

if input_filename.exists():
    logger.info(f'Input file: {str(input_filename.resolve())}')
    logger.info(f'Output file: {str(output_filename.resolve())}')
    logger.info(f'Using grey pattern: {gray_scale}')
else:
    logger.error(f'File does not exist: {input_filename}')
    exit(1)

with Image.open(input_filename) as image:
    bw_image = image.convert('L')
    width, height = bw_image.size
    if cols > width:
        logger.error(f'The number of cols {cols} is bigger than the width {width} of the picture')
        exit(1)
    scale = width / height
    cropped_width = width / cols
    columns = cols
    rows = int(columns / scale)
    cropped_height = height / rows
    logger.info(f'rows: {rows}, columns: {columns}')
    logger.info(f'Source width: {width}, source height: {height}, source ratio: {scale}')
    for y in range(rows):
        y1 = int(y * cropped_height)
        if y == rows - 1:
            y2 = height
        else:
            y2 = int((y + 1) * cropped_height)
        for x in range(columns):
            x1 = int(x * cropped_width)
            if x == columns - 1:
                x2 = width
            else:
                x2 = int((x + 1) * cropped_width)
            area = (x1, y1, x2, y2)
            cropped_image = bw_image.crop(area)
            cropped_pixels = list(cropped_image.getdata())
            average = statistics.fmean(cropped_pixels)
            tmp += (gray_scale[int(average * (len(gray_scale) - 1) / 255)])
        result.append(tmp)
        tmp = ''
with open(output_filename, 'w') as f:
    for string in result:
        f.write(string+'\n')
exit(0)
