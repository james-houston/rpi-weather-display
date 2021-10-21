from PIL import Image

base_image = "img/numbers/temp-base-text.png"

im_map = {
  0: 'img/numbers/0.png',
  1: 'img/numbers/1.png',
  2: 'img/numbers/2.png',
  3: 'img/numbers/3.png',
  4: 'img/numbers/4.png',
  5: 'img/numbers/5.png',
  6: 'img/numbers/6.png',
  7: 'img/numbers/7.png',
  8: 'img/numbers/8.png',
  9: 'img/numbers/9.png',
  'blank': 'img/numbers/blank.png'
}
# 32x32 image for half the 32x64 display
width = 32
height = 32

# input_image_selection is a list of 6 numbers to build the images out of. e.g. a curr/max/min of 15,20,10 becomes [1, 5, 2, 0, 1, 0]
def val_list_to_img(input_image_selection, dynamic_temperature):
  images = []
  for idx, number in enumerate(input_image_selection):
    if (idx == 0 or idx == 2 or idx == 4) and (number == 0):
      # if the most significant digit is zero, use a blank number instead. Looks nicer
      images.append(im_map['blank'])
    else:
      images.append(im_map[number])
  images = [Image.open(x) for x in images]
  # create a new image with the appropriate height and width
  new_img = Image.new('RGB', (width, height))
  # start with base image at 0,0
  new_img.paste(Image.open(base_image), (0,0))
  # hardcoded coordinates for pasting numbers into a 32x32 image
  new_img.paste(images[0], (23, 0))
  new_img.paste(images[1], (28, 0))
  new_img.paste(images[2], (23, 11))
  new_img.paste(images[3], (28, 11))
  new_img.paste(images[4], (23, 22))
  new_img.paste(images[5], (28, 22))
  # save generated image
  new_img.save(dynamic_temperature)

# returns a list of length 6 integers corresponding to curr/max/min
def temps_to_list_celsius(curr, max, min):
  vals = []
  vals.append(int(int(curr) / 10))
  vals.append(int(int(curr) % 10))
  vals.append(int(int(max) / 10))
  vals.append(int(int(max) % 10))
  vals.append(int(int(min) / 10))
  vals.append(int(int(min) % 10))
  return vals

def build_image(min, max, curr, dynamic_temperature):
  vals = temps_to_list_celsius(curr, max, min)
  val_list_to_img(vals, dynamic_temperature)