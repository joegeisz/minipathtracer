import numpy as np
import cv2
import matplotlib.pyplot as plt

im = np.load("image1.npy")
renderedim=im*255
renderedim = np.clip(renderedim, a_min=0, a_max=255).astype(np.uint8)
h=3
hcol=3
key = -1
tws = 7
sws = 21

while key != 13:
    showimg = cv2.fastNlMeansDenoisingColored(renderedim, h=h, hColor=hcol, templateWindowSize = tws, searchWindowSize = sws)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "h={:}, hcol={:}, tws={:}, sws={:}".format(h,hcol,tws,sws)
    font_scale = 0.5
    #color = (255, 255, 255)  # White color
    color = (150,150,255)  # White color
    thickness = 1

    # Calculate text size
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_width, text_height = text_size

    # Calculate position for bottom-left alignment
    height, width, _ = showimg.shape
    x = 0
    y = height - text_height

    # Add text to the image
    showimg = cv2.putText(showimg, text, (x, y), font, font_scale, color, thickness)
    cv2.imshow("Image", showimg)
    key = cv2.waitKey(0)
    if key == 102: h+=1
    if key == 100: h-=1
    if key == 106: hcol+=1
    if key == 107: hcol -=1
    if key == 114: tws += 2
    if key == 101: tws -=2
    if key == 117: sws += 2
    if key == 105: sws -= 2 
    if key == 49: 
        h = hcol = 0
        tws = 7
        sws = 21
    else:
        print(key)
cv2.destroyAllWindows()


# plt.figure()
# plt.imshow(renderedim)

# for h in [3,10,20,30]:
#     denoised = cv2.fastNlMeansDenoisingColored(renderedim,h=h)
#     plt.figure()
#     plt.imshow(denoised)

# for hcol in [3,10,20,30]:
#     denoised = cv2.fastNlMeansDenoisingColored(renderedim,hColor=hcol)
#     plt.figure()
#     plt.imshow(denoised)

# for h in [3,10,20,30]:
#     denoised = cv2.fastNlMeansDenoisingColored(renderedim,h=h,hColor=h)
#     plt.figure()
#     plt.imshow(denoised)

# plt.show()