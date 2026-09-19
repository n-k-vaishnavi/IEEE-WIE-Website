import os
import cv2
import numpy as np

os.makedirs('scratch/cropped_test', exist_ok=True)

# Face coordinates (center_x, center_y, face_size) determined visually & verified:
# We want face_size to be ~34% to 38% of the final crop width, with eyes at ~33% from top.
# Target aspect ratio: 3:4 (width: 600, height: 800)

FACE_DATA = {
    'gayathri-kamath.jpeg': {'cx': 310, 'cy': 285, 'size': 267},
    'kruthika-d.jpeg': {'cx': 615, 'cy': 522, 'size': 478},
    'shraddha-baidya.jpeg': {'cx': 367, 'cy': 274, 'size': 330},
    'namitha-m-rao.jpeg': {'cx': 592, 'cy': 318, 'size': 282},
    'gonuguntla-srujana.jpeg': {'cx': 377, 'cy': 226, 'size': 253},
    'vaishnavi.jpeg': {'cx': 465, 'cy': 465, 'size': 378},
    't-himaja.jpeg': {'cx': 309, 'cy': 134, 'size': 95},
    'shruti.jpeg': {'cx': 303, 'cy': 374, 'size': 100},
    'varshini-jayanth.jpeg': {'cx': 334, 'cy': 262, 'size': 145},
    'dikshitha.jpeg': {'cx': 662, 'cy': 786, 'size': 160},
    'sahana-h-m.jpeg': {'cx': 482, 'cy': 376, 'size': 290},
    'disha-varanashi.jpeg': {'cx': 150, 'cy': 250, 'size': 105},
    'srushti-reddy.jpeg': {'cx': 633, 'cy': 554, 'size': 260},
    'pratheeksha-v.jpeg': {'cx': 434, 'cy': 611, 'size': 200},
}

for fname, data in FACE_DATA.items():
    src_path = os.path.join('images/members_original', fname)
    img = cv2.imread(src_path)
    h, w = img.shape[:2]
    
    cx = data['cx']
    cy = data['cy']
    fsize = data['size']
    
    # Desired crop width so that face is ~36% of crop width
    target_crop_w = int(fsize / 0.36)
    target_crop_h = int(target_crop_w * 4 / 3)
    
    # Center face horizontally, place face center at 35% from top
    x1 = int(cx - target_crop_w / 2)
    x2 = x1 + target_crop_w
    y1 = int(cy - target_crop_h * 0.35)
    y2 = y1 + target_crop_h
    
    # If crop exceeds bounds, pad with border reflection or edge color
    pad_left = max(0, -x1)
    pad_right = max(0, x2 - w)
    pad_top = max(0, -y1)
    pad_bottom = max(0, y2 - h)
    
    if pad_left > 0 or pad_right > 0 or pad_top > 0 or pad_bottom > 0:
        # Pad image
        # Use edge replicate for natural extension
        img_padded = cv2.copyMakeBorder(
            img, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_REPLICATE
        )
        # Shift coordinates
        x1 += pad_left
        x2 += pad_left
        y1 += pad_top
        y2 += pad_top
        crop = img_padded[y1:y2, x1:x2]
    else:
        crop = img[y1:y2, x1:x2]
        
    # Resize to standard 600x800 for crystal-clear HD display
    final_img = cv2.resize(crop, (600, 800), interpolation=cv2.INTER_LANCZOS4)
    out_path = os.path.join('scratch/cropped_test', fname)
    cv2.imwrite(out_path, final_img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f'Processed {fname} -> 600x800')

print("All 14 images processed in scratch/cropped_test")
